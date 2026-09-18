from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import base64
import httpx

class BaseCMSAdapter(ABC):
    @abstractmethod
    async def get_pages(self, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def push_metadata(
        self, 
        page_id: str, 
        title: str, 
        meta_description: str, 
        extra_meta: Optional[Dict[str, Any]] = None
    ) -> bool:
        pass


class WordPressCMSAdapter(BaseCMSAdapter):
    def __init__(self, base_url: str, username: str, app_password: str, post_type: str = "posts"):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.app_password = app_password
        self.post_type = post_type
        
        credentials = f"{username}:{app_password}"
        encoded_creds = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_creds}",
            "Content-Type": "application/json"
        }

    async def get_pages(self, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/wp-json/wp/v2/{self.post_type}?per_page={limit}&_fields=id,title,link,meta"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "id": str(item["id"]),
                    "title": item.get("title", {}).get("rendered", ""),
                    "url": item.get("link", ""),
                    "meta": item.get("meta", {})
                }
                for item in data
            ]

    async def push_metadata(
        self, 
        page_id: str, 
        title: str, 
        meta_description: str, 
        extra_meta: Optional[Dict[str, Any]] = None
    ) -> bool:
        url = f"{self.base_url}/wp-json/wp/v2/{self.post_type}/{page_id}"
        
        # Yoast & RankMath supported meta mapping
        payload: Dict[str, Any] = {
            "title": title,
            "meta": {
                "_yoast_wpseo_title": title,
                "_yoast_wpseo_metadesc": meta_description,
                "rank_math_title": title,
                "rank_math_description": meta_description,
            }
        }
        if extra_meta:
            payload["meta"].update(extra_meta)

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=self.headers, timeout=15.0)
            return resp.status_code == 200


class ShopifyCMSAdapter(BaseCMSAdapter):
    def __init__(self, shop_domain: str, access_token: str, resource_type: str = "products"):
        self.shop_domain = shop_domain.rstrip("/")
        self.access_token = access_token
        self.resource_type = resource_type  # 'products' or 'pages'
        self.api_version = "2024-01"
        self.base_url = f"https://{self.shop_domain}/admin/api/{self.api_version}"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    async def get_pages(self, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{self.resource_type}.json?limit={limit}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
            items = data.get(self.resource_type, [])
            return [
                {
                    "id": str(item.get("id")),
                    "title": item.get("title", ""),
                    "handle": item.get("handle", ""),
                }
                for item in items
            ]

    async def push_metadata(
        self, 
        page_id: str, 
        title: str, 
        meta_description: str, 
        extra_meta: Optional[Dict[str, Any]] = None
    ) -> bool:
        owner_id = int(page_id) if page_id.isdigit() else page_id
        res_meta_url = f"{self.base_url}/{self.resource_type}/{owner_id}/metafields.json"
        
        metafields_payload = [
            {"metafield": {"namespace": "global", "key": "title_tag", "value": title, "type": "single_line_text_field"}},
            {"metafield": {"namespace": "global", "key": "description_tag", "value": meta_description, "type": "single_line_text_field"}}
        ]

        async with httpx.AsyncClient() as client:
            success = True
            for m in metafields_payload:
                resp = await client.post(res_meta_url, json=m, headers=self.headers, timeout=15.0)
                if resp.status_code not in (200, 201):
                    success = False
            return success