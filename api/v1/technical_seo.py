from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from modules.indexnow import IndexNowConnector
from modules.psi_monitor import CoreWebVitalsMonitor
from modules.link_injector import AutoInternalLinkInjector

router = APIRouter(prefix="/api/v1/technical-seo", tags=["Phase 3: Technical SEO & Indexing"])

class IndexNowRequest(BaseModel):
    host: str
    key: str
    urls: List[str]
    key_location: Optional[str] = None

class PSIRequest(BaseModel):
    url: str
    api_key: Optional[str] = None
    strategy: str = "mobile"

class LinkInjectRequest(BaseModel):
    html_content: str
    keyword_map: Dict[str, str]
    max_injections: int = 1

@router.post("/indexnow/submit")
async def submit_indexnow(req: IndexNowRequest):
    connector = IndexNowConnector()
    result = await connector.submit_urls(req.host, req.key, req.urls, req.key_location)
    return {"status": "success" if result["success"] else "error", "details": result}

@router.post("/psi/monitor")
async def monitor_cwv(req: PSIRequest):
    monitor = CoreWebVitalsMonitor(api_key=req.api_key)
    result = await monitor.check_vitals(req.url, strategy=req.strategy)
    return {"status": "success", "data": result}

@router.post("/links/inject")
async def inject_internal_links(req: LinkInjectRequest):
    injector = AutoInternalLinkInjector(keyword_link_map=req.keyword_map)
    modified_html, injected = injector.inject_links(req.html_content, max_injections_per_keyword=req.max_injections)
    return {
        "status": "success",
        "injected_keywords": injected,
        "modified_html": modified_html
    }