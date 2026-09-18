from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Set
import pandas as pd
import traceback
from agents.agent11_keyword_engine import KeywordIntelligenceEngine
from modules.gsc_diff import calculate_gsc_position_diff
from modules.competitor_parser import parse_competitor_seo_gaps

router = APIRouter(prefix="/api/v1/intelligence", tags=["SEO Intelligence"])

class KeywordRequest(BaseModel):
    seed_keywords: List[str]
    location_code: int = 2840
    language_code: str = "en"

class CompetitorRequest(BaseModel):
    target_url: str
    reference_target_keywords: List[str]

class GSCDiffRequest(BaseModel):
    baseline_data: List[Dict[str, Any]]
    current_data: List[Dict[str, Any]]
    position_threshold: float = 3.0

@router.post("/keywords")
async def get_keywords(req: KeywordRequest):
    engine = KeywordIntelligenceEngine()
    results = await engine.fetch_high_intent_keywords(
        seed_keywords=req.seed_keywords,
        location_code=req.location_code,
        language_code=req.language_code
    )
    return {"status": "success", "count": len(results), "data": results}

@router.post("/competitor-gaps")
async def analyze_gaps(req: CompetitorRequest):
    try:
        gaps = await parse_competitor_seo_gaps(
            target_url=req.target_url,
            reference_target_keywords=set(req.reference_target_keywords)
        )
        return {"status": "success", "data": gaps}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gsc-diff")
async def gsc_diff(req: GSCDiffRequest):
    try:
        if not req.baseline_data or not req.current_data:
            raise HTTPException(status_code=400, detail="Baseline or current data cannot be empty.")
            
        base_df = pd.DataFrame(req.baseline_data)
        curr_df = pd.DataFrame(req.current_data)
        
        # Map 'keyword' to GSC standard 'query' column and inject default clicks if missing
        for df, default_clicks in [(base_df, 5), (curr_df, 15)]:
            if "keyword" in df.columns and "query" not in df.columns:
                df.rename(columns={"keyword": "query"}, inplace=True)
            if "query" not in df.columns:
                df["query"] = []
            if "position" not in df.columns:
                df["position"] = []
            if "clicks" not in df.columns:
                df["clicks"] = default_clicks

        diffs = calculate_gsc_position_diff(base_df, curr_df, req.position_threshold)
        return {"status": "success", "data": diffs}
    except HTTPException:
        raise
    except Exception as e:
        print("[GSC Diff Full Traceback]:")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")