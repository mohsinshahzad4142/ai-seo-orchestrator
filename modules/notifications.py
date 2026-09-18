import httpx
from typing import Optional, Dict, Any

class NotificationEngine:
    def __init__(self, provider: str = "resend", api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key

    async def send_audit_email(self, to_email: str, subject: str, html_content: str) -> Dict[str, Any]:
        if self.provider == "resend" and self.api_key:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "from": "AI SEO Orchestrator <seo@yourdomain.com>",
                "to": [to_email],
                "subject": subject,
                "html": html_content
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, headers=headers, timeout=15.0)
                return {
                    "status_code": resp.status_code,
                    "response": resp.json() if resp.status_code < 400 else resp.text
                }
        elif self.provider == "sendgrid" and self.api_key:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": "seo@yourdomain.com", "name": "AI SEO Orchestrator"},
                "subject": subject,
                "content": [{"type": "text/html", "value": html_content}]
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, headers=headers, timeout=15.0)
                return {"status_code": resp.status_code, "response": resp.text}
        
        # Fallback / Mock mode for local testing
        return {
            "status": "mock_delivered",
            "to": to_email,
            "subject": subject,
            "note": "Configure API key and provider (resend/sendgrid) for live dispatch."
        }