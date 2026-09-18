from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import List, Dict, Any, Callable
import logging

logger = logging.getLogger("SEOOrchestratorScheduler")

class AutonomousScheduler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AutonomousScheduler, cls).__new__(cls)
            cls._instance.scheduler = AsyncIOScheduler()
        return cls._instance

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("APScheduler background service started.")

    def shutdown(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("APScheduler background service stopped.")

    def schedule_15day_full_crawl(self, job_id: str, func: Callable, target_url: str):
        self.scheduler.add_job(
            func,
            "interval",
            days=15,
            args=[target_url],
            id=job_id,
            replace_existing=True
        )

    def check_position_drops(
        self, 
        current_rankings: List[Dict[str, Any]], 
        baseline_rankings: List[Dict[str, Any]], 
        drop_threshold: int = 3
    ) -> List[Dict[str, Any]]:
        baseline_map = {item.get("keyword"): item.get("position") for item in baseline_rankings}
        triggered_alerts = []

        for curr in current_rankings:
            kw = curr.get("keyword")
            curr_pos = curr.get("position", 0)
            base_pos = baseline_map.get(kw)
            
            if base_pos is not None:
                drop_delta = curr_pos - base_pos  # positive delta means position worsened (e.g. 2 -> 6 = drop of 4)
                if drop_delta >= drop_threshold:
                    triggered_alerts.append({
                        "keyword": kw,
                        "url": curr.get("url"),
                        "previous_position": base_pos,
                        "current_position": curr_pos,
                        "drop_delta": drop_delta,
                        "status": "TRIGGERED: Auto re-optimization pipeline queued"
                    })
        return triggered_alerts