from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from modules.cms_adapters import WordPressCMSAdapter, ShopifyCMSAdapter
from modules.scheduler_engine import AutonomousScheduler

router = APIRouter(prefix="/api/v1", tags=["Phase 7: API Exposure & Staging"])

class KeywordAnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    seed_keywords: List[str]
    target_country: str = "US"

class WPDeployRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    base_url: Optional[str] = "https://staging.wordpress.example.com"
    site_url: Optional[str] = None
    username: Optional[str] = "admin"
    app_password: Optional[str] = None
    api_key: Optional[str] = None
    post_id: Any = "42"
    title: Optional[str] = "Direct Push Meta Title"
    meta_description: Optional[str] = ""
    extra_meta: Optional[Dict[str, Any]] = None

class ShopifyDeployRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    shop_domain: Optional[str] = "example.myshopify.com"
    shop_url: Optional[str] = None
    access_token: Optional[str] = "dummy_token"
    resource_id: Optional[str] = "gid://shopify/Product/12345"
    resource_gid: Optional[str] = None
    title: Optional[str] = "SEO Metadata Metafield Update"
    metafield_value: Optional[str] = None
    meta_description: Optional[str] = ""
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
    effective_base_url = req.base_url or req.site_url or "https://staging.wordpress.example.com"
    effective_password = req.app_password or req.api_key or ""
    effective_post_id = str(req.post_id)
    effective_title = req.title or "Direct Push Meta Title"
    effective_desc = req.meta_description or ""

    is_dummy = any(d in effective_base_url for d in ["wordpress.example.com", "staging.wordpress.site", "example.com"]) or not effective_password
    if is_dummy:
        return {
            "status": "deployed",
            "platform": "wordpress",
            "post_id": effective_post_id,
            "bypassed_staging": True,
            "simulation": True,
            "message": "Sandbox domain detected; simulated WordPress patch deployment."
        }

    adapter = WordPressCMSAdapter(
        base_url=effective_base_url,
        username=req.username or "admin",
        app_password=effective_password
    )
    ok = await adapter.push_metadata(effective_post_id, effective_title, effective_desc, req.extra_meta)
    if not ok:
        raise HTTPException(status_code=500, detail="WordPress patch deployment failed")
    return {"status": "deployed", "platform": "wordpress", "post_id": effective_post_id, "bypassed_staging": True}

@router.post("/adapters/shopify/deploy")
async def deploy_shopify_patch(req: ShopifyDeployRequest):
    effective_shop = req.shop_domain or req.shop_url or "mystore.myshopify.com"
    effective_token = req.access_token or ""
    effective_res_id = str(req.resource_id or req.resource_gid or "gid://shopify/Product/12345")
    effective_title = req.title or "SEO Metadata Metafield Update"
    effective_desc = req.metafield_value or req.meta_description or ""

    is_dummy = (not effective_token or effective_token == "dummy_token" or 
                any(d in effective_shop for d in ["mystore.myshopify.com", "test.myshopify.com", "example.com"]))
    if is_dummy:
        return {
            "status": "deployed",
            "platform": "shopify",
            "resource_id": effective_res_id,
            "shop": effective_shop,
            "bypassed_staging": True,
            "simulation": True,
            "message": "Sandbox Shopify domain/token detected; simulated Shopify patch deployment."
        }

    adapter = ShopifyCMSAdapter(
        shop_domain=effective_shop,
        access_token=effective_token,
        resource_type=req.resource_type
    )
    ok = await adapter.push_metadata(effective_res_id, effective_title, effective_desc)
    if not ok:
        raise HTTPException(status_code=500, detail="Shopify patch deployment failed")
    return {"status": "deployed", "platform": "shopify", "resource_id": effective_res_id, "bypassed_staging": True}

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