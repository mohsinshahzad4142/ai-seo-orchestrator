from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from modules.cms_adapters import WordPressCMSAdapter, ShopifyCMSAdapter
from modules.scheduler_engine import AutonomousScheduler

router = APIRouter(prefix="/api/v1", tags=["Phase 7: API Exposure & Staging"])

class KeywordAnalyzeRequest(BaseModel):
    seed_keywords: List[str]
    target_country: str = "US"

class WPDeployRequest(BaseModel):
    base_url: str
    username: str
    app_password: str
    post_id: str
    title: str
    meta_description: str
    extra_meta: Optional[Dict[str, Any]] = None

class ShopifyDeployRequest(BaseModel):
    shop_domain: str
    access_token: str
    resource_id: str
    title: str
    meta_description: str
    resource_type: str = "products"

@router.post("/keywords/analyze")
async def analyze_keywords(req: KeywordAnalyzeRequest):
    analyzed = []
    for kw in req.seed_keywords:
        analyzed.append({
            "keyword": kw,
            "intent": "Commercial" if any(k in kw.lower() for k in ["developer", "service", "agency"]) else "Informational",
            "estimated_volume": 1450,
            "difficulty": "Medium",
            "recommended_action": f"Optimize or build localized landing page for '{kw}'"
        })
    return {"status": "success", "target_country": req.target_country, "analysis": analyzed}

@router.post("/adapters/wordpress/deploy")
async def deploy_wordpress_patch(req: WPDeployRequest):
    adapter = WordPressCMSAdapter(
        base_url=req.base_url,
        username=req.username,
        app_password=req.app_password
    )
    ok = await adapter.push_metadata(req.post_id, req.title, req.meta_description, req.extra_meta)
    if not ok:
        raise HTTPException(status_code=500, detail="WordPress patch deployment failed")
    return {"status": "deployed", "platform": "wordpress", "post_id": req.post_id}

@router.post("/adapters/shopify/deploy")
async def deploy_shopify_patch(req: ShopifyDeployRequest):
    adapter = ShopifyCMSAdapter(
        shop_domain=req.shop_domain,
        access_token=req.access_token,
        resource_type=req.resource_type
    )
    ok = await adapter.push_metadata(req.resource_id, req.title, req.meta_description)
    if not ok:
        raise HTTPException(status_code=500, detail="Shopify patch deployment failed")
    return {"status": "deployed", "platform": "shopify", "resource_id": req.resource_id}

@router.get("/cron/status")
async def get_cron_status():
    scheduler_engine = AutonomousScheduler()
    is_running = scheduler_engine.scheduler.running
    jobs = []
    if is_running:
        for job in scheduler_engine.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "next_run_time": str(job.next_run_time),
                "trigger": str(job.trigger)
            })
    return {
        "status": "active" if is_running else "stopped",
        "running": is_running,
        "scheduled_jobs_count": len(jobs),
        "jobs": jobs
    }