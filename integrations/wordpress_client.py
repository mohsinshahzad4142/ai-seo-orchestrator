import httpx
from typing import List, Dict, Any

class WordPressClient:
    def __init__(self, base_url: str, username: str, application_password: str):
        self.base_url = base_url.rstrip("/")
        self.auth = (username, application_password)

    async def get_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/wp-json/wp/v2/posts",
                params={"per_page": limit},
                auth=self.auth
            )
            response.raise_for_status()
            return response.json()

    async def create_draft_post(self, title: str, content: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            payload = {
                "title": title,
                "content": content,
                "status": "draft"
            }
            response = await client.post(
                f"{self.base_url}/wp-json/wp/v2/posts",
                json=payload,
                auth=self.auth
            )
            response.raise_for_status()
            return response.json()