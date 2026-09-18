from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter(prefix="/api/v1/authority-seo", tags=["Authority SEO"])

class UnlinkedMentionRequest(BaseModel):
    brand_name: str = "Mohsin AI Freelancer Assistant"
    domain: Optional[str] = "mohsinshahzad.vercel.app"
    target_domain: Optional[str] = None
    source_urls: Optional[List[str]] = None

class LinkGapRequest(BaseModel):
    target_domain: str = "mohsinshahzad.vercel.app"
    competitor_domain: str = "competitor-seo.com"
    target_backlinks: Optional[List[str]] = None
    competitor_backlinks_map: Optional[Dict[str, List[str]]] = None

class BacklinkGapAnalysisRequest(BaseModel):
    target_domain: Optional[str] = "mohsinshahzad.vercel.app"
    competitor_domain: Optional[str] = "competitor-seo.com"
    target_backlinks: Optional[List[str]] = ["https://siteA.com/ref1"]
    competitor_backlinks_map: Optional[Dict[str, List[str]]] = None

@router.post("/mentions/scan-unlinked")
async def scan_unlinked_mentions(req: UnlinkedMentionRequest):
    eff_target = req.target_domain or req.domain or "mohsinshahzad.vercel.app"
    eff_sources = req.source_urls if req.source_urls else [
        "https://techblog.example.com/ai-freelance-tools-review",
        f"https://devdigest.io/mentioning-{req.brand_name.lower().replace(' ', '-')}"
    ]
    mentions = [
        {
            "source_url": src,
            "mentioned_text": req.brand_name,
            "has_link": False,
            "suggested_anchor": f"{req.brand_name} Platform",
            "target_url": f"https://{eff_target}"
        }
        for src in eff_sources
    ]
    return {
        "status": "success",
        "action": "unlinked_brand_mention_scanner",
        "brand_name": req.brand_name,
        "target_domain": eff_target,
        "total_scanned_sources": len(eff_sources),
        "unlinked_count": len(mentions),
        "mentions": mentions,
        "simulation": True
    }

@router.post("/links/gap")
async def analyze_link_gap(req: LinkGapRequest):
    t_links = req.target_backlinks or ["https://siteA.com/ref1"]
    c_map = req.competitor_backlinks_map or {
        req.competitor_domain: [
            "https://siteA.com/ref1",
            "https://authoritative-site.org/ai-freelance-tools"
        ]
    }
    competitor_all_links = set()
    for urls in c_map.values():
        if isinstance(urls, list):
            competitor_all_links.update(urls)
    target_set = set(t_links)
    gap_links = list(competitor_all_links - target_set)
    return {
        "status": "success",
        "action": "competitor_link_gap_analysis",
        "target_domain": req.target_domain,
        "competitor_domain": req.competitor_domain,
        "link_gap_count": len(gap_links),
        "missing_opportunity_links": gap_links,
        "simulation": True
    }

@router.post("/backlinks/gap-analysis")
async def backlink_gap_analysis(req: BacklinkGapAnalysisRequest):
    t_dom = req.target_domain or "mohsinshahzad.vercel.app"
    c_dom = req.competitor_domain or "competitor-seo.com"
    t_links = req.target_backlinks or ["https://siteA.com/ref1"]
    c_map = req.competitor_backlinks_map or {
        c_dom: [
            "https://siteA.com/ref1",
            "https://authoritative-site.org/ai-freelance-tools"
        ]
    }
    competitor_all_links = set()
    for urls in c_map.values():
        if isinstance(urls, list):
            competitor_all_links.update(urls)
    target_set = set(t_links)
    gap_links = list(competitor_all_links - target_set)
    return {
        "status": "success",
        "action": "competitor_backlink_gap_analysis",
        "target_domain": t_dom,
        "competitor_domain": c_dom,
        "link_gap_count": len(gap_links),
        "missing_opportunity_links": gap_links,
        "simulation": True
    }