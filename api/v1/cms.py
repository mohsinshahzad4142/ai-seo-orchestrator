from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from modules.cms_adapters import WordPressCMSAdapter, ShopifyCMSAdapter

router = APIRouter(prefix="/api/v1/cms", tags=["Multi-CMS Integration"])

class WPPushRequest(BaseModel):
    base_url: str
    username: str
    app_password: str
    post_id: str
    title: str
    meta_description: str
    post_type: str = "posts"
    extra_meta: Optional[Dict[str, Any]] = None

class ShopifyPushRequest(BaseModel):
    shop_domain: str
    access_token: str
    resource_id: str
    title: str
    meta_description: str
    resource_type: str = "products"

@router.post("/wordpress/push")
async def wp_push_metadata(req: WPPushRequest):
    adapter = WordPressCMSAdapter(
        base_url=req.base_url,
        username=req.username,
        app_password=req.app_password,
        post_type=req.post_type
    )
    ok = await adapter.push_metadata(
        page_id=req.post_id,
        title=req.title,
        meta_description=req.meta_description,
        extra_meta=req.extra_meta
    )
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to push metadata to WordPress")
    return {"status": "success", "platform": "wordpress", "post_id": req.post_id}

@router.post("/shopify/push")
async def shopify_push_metadata(req: ShopifyPushRequest):
    adapter = ShopifyCMSAdapter(
        shop_domain=req.shop_domain,
        access_token=req.access_token,
        resource_type=req.resource_type
    )
    ok = await adapter.push_metadata(
        page_id=req.resource_id,
        title=req.title,
        meta_description=req.meta_description
    )
    if not ok:
        raise HTTPException(status_count=500 if hasattr(status_count, '500') else 500, detail="Failed to push metafields to Shopify")
    return {"status": "success", "platform": "shopify", "resource_id": req.resource_id}