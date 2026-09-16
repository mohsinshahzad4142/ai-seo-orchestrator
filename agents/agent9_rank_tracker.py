import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class RankTrackerAgent:
    def __init__(self):
        self.creds_path = "gsc-credentials.json"
        self.site_url = os.getenv("GSC_SITE_URL", "https://yourwebsite.com/")
        self.scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]

    def get_live_rankings(self, days: int = 7):
        if not os.path.exists(self.creds_path):
            return {
                "status": "mock_success",
                "message": "GSC Credentials missing. Returning Mock Data.",
                "data": [
                    {"query": "Mohsin Shahzad Full Stack Developer", "clicks": 142, "position": 1.2},
                    {"query": "Next.js AI SEO Orchestrator", "clicks": 89, "position": 3.4}
                ]
            }

        try:
            creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=self.scopes
            )
            service = build("searchconsole", "v1", credentials=creds)

            request = {
                "startDate": "2026-09-01",  # Adjust dynamic dates as needed
                "endDate": "2026-09-15",
                "dimensions": ["query"],
                "rowLimit": 10
            }

            response = service.searchanalytics().query(
                siteUrl=self.site_url, body=request
            ).execute()

            rows = response.get("rows", [])
            rankings = []
            for row in rows:
                rankings.append({
                    "query": row["keys"][0],
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": round(row.get("ctr", 0) * 100, 2),
                    "position": round(row.get("position", 0), 1)
                })

            return {
                "status": "success",
                "site_url": self.site_url,
                "data": rankings
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to fetch GSC data: {str(e)}"
            }