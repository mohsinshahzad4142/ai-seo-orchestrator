from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from modules.scheduler_engine import AutonomousScheduler
from modules.notifications import NotificationEngine

router = APIRouter(prefix="/api/v1/automation", tags=["Phase 6: Autonomous Cron & Notifications"])

class PositionCheckRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    current_rankings: Optional[List[Dict[str, Any]]] = None
    baseline_rankings: Optional[List[Dict[str, Any]]] = None
    threshold: int = 3

class EmailAlertRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    to_email: str = "admin@example.com"
    subject: str = "SEO Audit & Position Drop Report"
    html_content: str = "<p>Automated SEO audit report simulation.</p>"
    provider: str = "mock"
    api_key: Optional[str] = None

@router.post("/position-drops/detect")
async def detect_position_drops(req: Optional[PositionCheckRequest] = Body(default=None)):
    current = req.current_rankings if req and req.current_rankings else [
        {"keyword": "python seo orchestrator", "position": 9, "url": "https://example.com/page1"}
    ]
    baseline = req.baseline_rankings if req and req.baseline_rankings else [
        {"keyword": "python seo orchestrator", "position": 4, "url": "https://example.com/page1"}
    ]
    threshold = req.threshold if req else 3
    scheduler = AutonomousScheduler()
    alerts = scheduler.check_position_drops(current, baseline, threshold)
    return {
        "status": "success",
        "drop_alerts_count": len(alerts),
        "alerts": alerts
    }

@router.post("/notifications/send-report")
async def send_audit_report(req: Optional[EmailAlertRequest] = Body(default=None)):
    to_email = req.to_email if req else "admin@example.com"
    subject = req.subject if req else "SEO Audit & Position Drop Report"
    html_content = req.html_content if req else "<p>Automated SEO audit report simulation.</p>"
    provider = req.provider if req else "mock"
    api_key = req.api_key if req else None
    
    notifier = NotificationEngine(provider=provider, api_key=api_key)
    res = await notifier.send_audit_email(to_email, subject, html_content)
    return {"status": "success", "delivery_result": res}