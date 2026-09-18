from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from modules.brand_mention_detector import UnlinkedBrandMentionDetector
from modules.backlink_gap_analyzer import CompetitorBacklinkGapAnalyzer

router = APIRouter(prefix="/api/v1/authority-seo", tags=["Phase 5: Off-Page & Authority Automation"])

class MentionScanRequest(BaseModel):
    brand_name: str
    target_domain: str
    source_urls: List[str]

class BacklinkGapRequest(BaseModel):
    target_backlinks: List[Dict[str, Any]]
    competitor_backlinks_map: Dict[str, List[Dict[str, Any]]]

@router.post("/mentions/scan-unlinked")
async def scan_unlinked_mentions(req: MentionScanRequest):
    detector = UnlinkedBrandMentionDetector(brand_name=req.brand_name, target_domain=req.target_domain)
    alerts = []
    for url in req.source_urls:
        res = await detector.scan_url_for_unlinked_mentions(url)
        if res:
            alerts.append(res)
    return {
        "status": "success",
        "brand": req.brand_name,
        "scanned_count": len(req.source_urls),
        "unlinked_alerts_count": len(alerts),
        "alerts": alerts
    }

@router.post("/backlinks/gap-analysis")
async def analyze_backlink_gaps(req: BacklinkGapRequest):
    analyzer = CompetitorBacklinkGapAnalyzer()
    gaps = analyzer.analyze_gaps(req.target_backlinks, req.competitor_backlinks_map)
    return {"status": "success", "data": gaps}