from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase4_models import CannibalizationIssue


class CannibalizationAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    def select_primary_url(self, competing_urls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Selects the best primary URL based on clicks and impressions.
        """
        # Sort by clicks descending, then impressions descending
        sorted_urls = sorted(
            competing_urls,
            key=lambda x: (x.get("clicks", 0), x.get("impressions", 0)),
            reverse=True,
        )
        return sorted_urls[0] if sorted_urls else {}

    async def detect_cannibalization(
        self,
        website_id: int,
        gsc_keyword_data: List[Dict[str, Any]],
    ) -> List[CannibalizationIssue]:
        """
        Detects keyword cannibalization where multiple URLs rank for the same keyword.
        gsc_keyword_data format:
        [
            {"keyword": "seo tools", "url": "https://example.com/page1", "clicks": 50, "impressions": 1000, "position": 8.5},
            {"keyword": "seo tools", "url": "https://example.com/page2", "clicks": 20, "impressions": 500, "position": 12.1},
        ]
        """
        # Group URLs by keyword
        keyword_map: Dict[str, List[Dict[str, Any]]] = {}
        for row in gsc_keyword_data:
            kw = row.get("keyword", "").strip().lower()
            if not kw:
                continue
            if kw not in keyword_map:
                keyword_map[kw] = []
            keyword_map[kw].append(row)

        detected_issues: List[CannibalizationIssue] = []

        # Find keywords with 2 or more competing URLs
        for kw, urls in keyword_map.items():
            if len(urls) > 1:
                primary_info = self.select_primary_url(urls)
                primary_url = primary_info.get("url", "")

                competing_url_strings = [u.get("url") for u in urls if u.get("url") != primary_url]

                # Generate recommendations (consolidation / internal linking / repositioning)
                action_plan_parts = [
                    f"Keyword: '{kw}' has {len(urls)} competing URLs.",
                    f"• Primary Target Page: {primary_url} (Highest clicks/performance).",
                    f"• Competing Pages: {', '.join(competing_url_strings)}.",
                    "Recommended Strategic Actions:",
                    f"  1. Content Consolidation: Merge unique sections from competing pages into '{primary_url}'.",
                    f"  2. Internal Linking: Update internal links on competing pages to point towards '{primary_url}' using exact/phrase match anchor text.",
                    "  3. Keyword Repositioning: Re-optimize competing pages for secondary or long-tail intent variations to resolve conflict.",
                    "  Note: No automatic URL deletions or redirects have been performed.",
                ]

                action_plan = "\n".join(action_plan_parts)

                issue = CannibalizationIssue(
                    website_id=website_id,
                    keyword=kw,
                    competing_urls=urls,
                    primary_url=primary_url,
                    action_plan=action_plan,
                )

                self.db.add(issue)
                detected_issues.append(issue)

        if detected_issues:
            await self.db.commit()
            for issue in detected_issues:
                await self.db.refresh(issue)

        return detected_issues