from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.seo import SEOOpportunity, OpportunityPriority

class SEOOpportunityAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _calculate_priority(self, position: float, impressions: int, ctr: float) -> OpportunityPriority:
        # High Priority: Top page 2 candidates with solid impression volume & low CTR
        if position <= 12.0 and impressions >= 500 and ctr < 0.03:
            return OpportunityPriority.HIGH
        elif position <= 15.0 and impressions >= 200:
            return OpportunityPriority.MEDIUM
        return OpportunityPriority.LOW

    async def process_gsc_data(
        self, 
        website_id: int, 
        gsc_rows: List[Dict[str, Any]], 
        min_impressions: int = 100
    ) -> List[SEOOpportunity]:
        processed_opportunities = []

        for row in gsc_rows:
            keys = row.get("keys", [])
            if len(keys) < 2:
                continue

            query, page_url = keys[0], keys[1]
            position = float(row.get("position", 0.0))
            impressions = int(row.get("impressions", 0))
            clicks = int(row.get("clicks", 0))
            ctr = float(row.get("ctr", 0.0))

            # Target filter: Striking distance (Position 8-20) with minimum impressions
            if 8.0 <= position <= 20.0 and impressions >= min_impressions:
                priority = self._calculate_priority(position, impressions, ctr)

                # Check existing record for delta update
                stmt = select(SEOOpportunity).where(
                    SEOOpportunity.website_id == website_id,
                    SEOOpportunity.query == query,
                    SEOOpportunity.page_url == page_url
                )
                result = await self.db.execute(stmt)
                existing = result.scalars().first()

                if existing:
                    existing.impressions = impressions
                    existing.clicks = clicks
                    existing.ctr = ctr
                    existing.position = position
                    existing.priority = priority
                    processed_opportunities.append(existing)
                else:
                    new_opp = SEOOpportunity(
                        website_id=website_id,
                        query=query,
                        page_url=page_url,
                        impressions=impressions,
                        clicks=clicks,
                        ctr=ctr,
                        position=position,
                        priority=priority
                    )
                    self.db.add(new_opp)
                    processed_opportunities.append(new_opp)

        await self.db.commit()
        return processed_opportunities