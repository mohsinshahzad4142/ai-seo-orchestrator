import httpx
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any, Optional

class UnlinkedBrandMentionDetector:
    def __init__(self, brand_name: str, target_domain: str):
        self.brand_name = brand_name
        self.target_domain = target_domain

    async def scan_url_for_unlinked_mentions(self, source_url: str) -> Optional[Dict[str, Any]]:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-SEO-Orchestrator/1.0"}
        try:
            async with httpx.AsyncClient(headers=headers, timeout=15.0, follow_redirects=True) as client:
                resp = await client.get(source_url)
                if resp.status_code != 200:
                    return None
                soup = BeautifulSoup(resp.text, 'html.parser')
                text = soup.get_text()
                
                pattern = re.compile(re.escape(self.brand_name), re.IGNORECASE)
                if not pattern.search(text):
                    return None
                
                has_link = False
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if self.target_domain.lower() in href.lower():
                        has_link = True
                        break
                
                if not has_link:
                    return {
                        "source_url": source_url,
                        "brand_detected": self.brand_name,
                        "linked_to_target": False,
                        "outreach_status": "alert_triggered",
                        "action_required": f"Send unlinked brand mention outreach template to {source_url}"
                    }
        except Exception as e:
            return {"source_url": source_url, "error": str(e)}
        return None