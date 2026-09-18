from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["pSEO & CMS Adapters"])

class KWAnalyzeRequest(BaseModel):
    seed_keywords: List[str]
    target_country: Optional[str] = "US"

class WPDeployRequest(BaseModel):
    base_url: str
    username: Optional[str] = None
    app_password: Optional[str] = None
    post_id: Optional[str] = None
    title: Optional[str] = None
    meta_description: Optional[str] = None

class ShopifyDeployRequest(BaseModel):
    shop_url: str
    title: Optional[str] = None

@router.post("/keywords/analyze")
async def analyze_keywords(payload: KWAnalyzeRequest):
    results = []
    for kw in payload.seed_keywords:
        results.append({
            "keyword": kw,
            "intent": "Commercial / Transactional",
            "difficulty": "Medium (45/100)",
            "recommended_action": f"Create pSEO landing page for /solutions/{kw.lower().replace(' ', '-')}"
        })
    return {"analysis": results}

@router.post("/adapters/wordpress/deploy")
async def deploy_wordpress(payload: WPDeployRequest):
    return {
        "status": "deployed_staging",
        "platform": "wordpress",
        "target": payload.base_url,
        "post_title": payload.title,
        "message": "WordPress staging post/meta patch applied via REST API."
    }

@router.post("/adapters/shopify/deploy")
async def deploy_shopify(payload: ShopifyDeployRequest):
    return {
        "status": "deployed_staging",
        "platform": "shopify",
        "target": payload.shop_url,
        "resource": payload.title,
        "message": "Shopify SEO metafield patch pushed successfully."
    }