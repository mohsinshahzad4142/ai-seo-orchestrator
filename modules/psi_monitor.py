import httpx
from typing import Dict, Any, List, Optional

class CoreWebVitalsMonitor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def check_vitals(self, target_url: str, strategy: str = "mobile") -> Dict[str, Any]:
        base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params: Dict[str, Any] = {"url": target_url, "strategy": strategy}
        if self.api_key:
            params["key"] = self.api_key
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(base_url, params=params, timeout=30.0)
            if resp.status_code != 200:
                return {
                    "status": "error", 
                    "message": f"PSI API failed with status {resp.status_code}"
                }
            
            data = resp.json()
            audits = data.get("lighthouseResult", {}).get("audits", {})
            
            lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
            cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
            inp = audits.get("interaction-to-next-paint", {}).get("displayValue", 
                  audits.get("max-potential-fid", {}).get("displayValue", "N/A"))
            
            perf_score = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score")
            
            return {
                "target_url": target_url,
                "strategy": strategy,
                "metrics": {"lcp": lcp, "cls": cls, "inp": inp},
                "performance_score": perf_score * 100 if perf_score is not None else None,
                "alerts": self._generate_alerts(lcp, cls, inp, perf_score)
            }

    def _generate_alerts(self, lcp: str, cls: str, inp: str, perf_score: Optional[float]) -> List[str]:
        alerts = []
        if perf_score is not None and perf_score < 0.5:
            alerts.append("CRITICAL: Performance score below 50. Immediate optimization required.")
        else:
            alerts.append("Core Web Vitals scan completed. Benchmark against LCP < 2.5s, CLS < 0.1, INP < 200ms.")
        return alerts