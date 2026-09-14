from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GSCClient:
    def __init__(self, credentials_info: dict):
        self.creds = Credentials.from_authorized_user_info(credentials_info)
        self.service = build('searchconsole', 'v1', credentials=self.creds)

    def get_search_analytics(
        self,
        site_url: str,
        start_date: str,
        end_date: str,
        dimensions: List[str] = ["query", "page"],
        row_limit: int = 100
    ) -> List[Dict[str, Any]]:
        request_body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=site_url,
            body=request_body
        ).execute()
        
        return response.get("rows", [])