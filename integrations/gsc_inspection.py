from typing import Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GSCInspectionClient:
    def __init__(self, credentials_info: dict):
        self.creds = Credentials.from_authorized_user_info(credentials_info)
        self.service = build('searchconsole', 'v1', credentials=self.creds)

    def inspect_url(self, inspection_url: str, site_url: str) -> Dict[str, Any]:
        request_body = {
            "inspectionUrl": inspection_url,
            "siteUrl": site_url
        }
        
        response = self.service.urlInspection().index().inspect(
            body=request_body
        ).execute()
        
        return response.get("inspectionResult", {})