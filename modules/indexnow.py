import httpx
from typing import List, Dict, Any, Optional

class IndexNowConnector:
    async def submit_urls(
        self, 
        host: str, 
        key: str, 
        url_list: List[str], 
        key_location: Optional[str] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "host": host,
            "key": key,
            "urlList": url_list
        }
        if key_location:
            payload["keyLocation"] = key_location
        
        endpoint = "https://api.indexnow.org/indexnow"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(endpoint, json=payload, headers=headers, timeout=10.0)
            return {
                "status_code": resp.status_code,
                "success": resp.status_code in [200, 202],
                "response": resp.text or "Submitted to IndexNow"
            }