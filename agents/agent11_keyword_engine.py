import httpx
import os
from typing import List, Dict, Any

class KeywordIntelligenceEngine:
    def __init__(self, api_login: str = None, api_password: str = None):
        self.base_url = "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live"
        self.auth = (
            api_login or os.getenv("DATAFORSEO_LOGIN", ""),
            api_password or os.getenv("DATAFORSEO_PASSWORD", "")
        )

    async def fetch_high_intent_keywords(
        self, seed_keywords: List[str], location_code: int = 2840, language_code: str = "en"
    ) -> List[Dict[str, Any]]:
        payload = [{
            "keywords": seed_keywords,
            "location_code": location_code,
            "language_code": language_code,
            "include_seed_keyword": True
        }]
        
        async with httpx.AsyncClient(auth=self.auth, timeout=30.0) as client:
            response = await client.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()

        results = []
        commercial_triggers = {"services", "agency", "developer", "hire", "cost", "pricing", "best", "top", "saas", "platform"}

        for task in data.get("tasks", []):
            for item in task.get("result", []):
                for kw_item in item.get("items", []):
                    kw = kw_item.get("keyword", "")
                    metrics = kw_item.get("keyword_info", {})
                    competition = metrics.get("competition", 1.0)
                    search_volume = metrics.get("search_volume", 0)

                    # Commercial intent + low/moderate competition filter
                    tokens = set(kw.lower().split())
                    if tokens.intersection(commercial_triggers) and competition <= 0.65 and search_volume >= 40:
                        results.append({
                            "keyword": kw,
                            "search_volume": search_volume,
                            "competition": competition,
                            "intent": "commercial_high_intent"
                        })

        return sorted(results, key=lambda x: x["search_volume"], reverse=True)