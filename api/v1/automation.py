from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from modules.scheduler_engine import AutonomousScheduler
from modules.notifications import NotificationEngine

router = APIRouter(prefix="/api/v1/automation", tags=["Phase 6: Autonomous Cron & Notifications"])

class PositionCheckRequest(BaseModel):
    current_rankings: List[Dict[str, Any]]
    baseline_rankings: List[Dict[str, Any]]
    threshold: int = 3

class EmailAlertRequest(BaseModel):
    to_email: str
    subject: str
    html_content: str
    provider: str = "mock"
    api_key: Optional[str] = None

@router.post("/position-drops/detect")
async def detect_position_drops(req: PositionCheckRequest):
    scheduler = AutonomousScheduler()
    alerts = scheduler.check_position_drops(req.current_rankings, req.baseline_rankings, req.threshold)
    return {
        "status": "success",
        "drop_alerts_count": len(alerts),
        "alerts": alerts
    }

@router.post("/notifications/send-report")
async def send_audit_report(req: EmailAlertRequest):
    notifier = NotificationEngine(provider=req.provider, api_key=req.api_key)
    res = await notifier.send_audit_email(req.to_email, req.subject, req.html_content)
    return {"status": "success", "delivery_result": res}