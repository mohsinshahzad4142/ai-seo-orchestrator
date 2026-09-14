from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.seo import SEOOpportunity, Recommendation, RecommendationStatus, IndexingStatus

class ReportingAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_recommendation(
        self,
        website_id: int,
        title: str,
        action_type: str,
        suggested_changes: Dict[str, Any],
        opportunity_id: Optional[int] = None
    ) -> Recommendation:
        rec = Recommendation(
            website_id=website_id,
            opportunity_id=opportunity_id,
            title=title,
            action_type=action_type,
            suggested_changes=suggested_changes,
            status=RecommendationStatus.PENDING
        )
        self.db.add(rec)
        await self.db.commit()
        return rec

    async def update_decision(
        self, recommendation_id: int, new_status: RecommendationStatus
    ) -> Optional[Recommendation]:
        stmt = select(Recommendation).where(Recommendation.id == recommendation_id)
        result = await self.db.execute(stmt)
        rec = result.scalars().first()
        if rec:
            rec.status = new_status
            await self.db.commit()
        return rec

    async def generate_site_summary(self, website_id: int) -> Dict[str, Any]:
        opp_count = await self.db.scalar(
            select(func.count(SEOOpportunity.id)).where(SEOOpportunity.website_id == website_id)
        )
        rec_count = await self.db.scalar(
            select(func.count(Recommendation.id)).where(
                Recommendation.website_id == website_id,
                Recommendation.status == RecommendationStatus.PENDING
            )
        )
        indexing_issues = await self.db.scalar(
            select(func.count(IndexingStatus.id)).where(
                IndexingStatus.website_id == website_id,
                IndexingStatus.verdict != 'PASS'
            )
        )
        return {
            'website_id': website_id,
            'total_opportunities': opp_count or 0,
            'pending_recommendations': rec_count or 0,
            'indexing_issues': indexing_issues or 0
        }