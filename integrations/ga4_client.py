from typing import List, Dict, Any
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension

class GA4Client:
    def __init__(self, property_id: str, credentials_info: dict):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient.from_service_account_info(credentials_info)

    def get_website_traffic(
        self, start_date: str = "30daysAgo", end_date: str = "today"
    ) -> List[Dict[str, Any]]:
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="activeUsers"), Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = self.client.run_report(request)
        
        results = []
        for row in response.rows:
            results.append({
                "page_path": row.dimension_values[0].value,
                "active_users": int(row.metric_values[0].value),
                "page_views": int(row.metric_values[1].value)
            })
        return results