from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1/technical-seo", tags=["Technical SEO & Indexing"])

class IndexNowRequest(BaseModel):
    host: Optional[str] = "mohsinshahzad.vercel.app"
    url_list: List[str] = ["https://mohsinshahzad.vercel.app/blog/ai-seo"]
    key: Optional[str] = "test-indexnow-key"

class PSIRequest(BaseModel):
    url: str = "https://mohsinshahzad.vercel.app"
    strategy: str = "mobile"  # mobile or desktop

class LinkInjectRequest(BaseModel):
    target_url: str = "https://mohsinshahzad.vercel.app/blog/post-1"
    content: str = "Here is an article about nextjs seo agency and technical automation for a fastapi developer usa."
    target_keywords: List[str] = ["nextjs seo agency", "fastapi developer usa"]

@router.post("/indexnow/submit")
async def indexnow_submit(req: IndexNowRequest):
    return {
        "status": "success",
        "action": "indexnow_instant_submit",
        "submitted_host": req.host,
        "url_count": len(req.url_list),
        "urls": req.url_list,
        "simulation": True,
        "message": "IndexNow ping simulated successfully."
    }

@router.post("/psi/monitor")
async def psi_monitor(req: PSIRequest):
    is_mobile = req.strategy.lower() == "mobile"
    return {
        "status": "success",
        "action": "psi_monitor",
        "url": req.url,
        "strategy": req.strategy,
        "metrics": {
            "performance_score": 92 if is_mobile else 98,
            "lcp_seconds": 2.1 if is_mobile else 1.4,
            "fid_ms": 42 if is_mobile else 18,
            "cls": 0.02,
            "fid_status": "good",
            "lcp_status": "good"
        },
        "simulation": True
    }

@router.post("/links/inject")
async def links_inject(req: LinkInjectRequest):
    injections = []
    for kw in req.target_keywords:
        found = kw.lower() in req.content.lower()
        injections.append({
            "keyword": kw,
            "anchor_injected": found,
            "target_url": f"https://mohsinshahzad.vercel.app/topic/{kw.replace(' ', '-')}" if found else None,
            "reason": None if found else "Keyword string not matched in content text"
        })
    return {
        "status": "success",
        "action": "auto_internal_link_injector",
        "target_url": req.target_url,
        "injections": injections,
        "simulation": True
    }