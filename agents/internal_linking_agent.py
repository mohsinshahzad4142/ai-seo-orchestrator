from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase5_models import InternalLinkOpportunity


class InternalLinkingAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def discover_link_opportunities(
        self,
        website_id: int,
        pages_data: List[Dict[str, Any]]
    ) -> List[InternalLinkOpportunity]:
        """
        Identifies orphan or low internal-link pages and creates contextual anchor text recommendations.
        pages_data structure:
        [
            {"url": "https://example.com/target", "inbound_links": 1, "top_keywords": ["python seo"]},
            {"url": "https://example.com/source", "inbound_links": 10, "content": "...python seo tips..."},
        ]
        """
        opportunities: List[InternalLinkOpportunity] = []

        target_pages = [p for p in pages_data if p.get("inbound_links", 0) <= 2]
        source_pages = [p for p in pages_data if p.get("inbound_links", 0) > 2]

        for target in target_pages:
            t_url = target.get("url", "")
            keywords = target.get("top_keywords", ["seo"])

            for source in source_pages:
                s_url = source.get("url", "")
                s_content = source.get("content", "").lower()

                for kw in keywords:
                    if kw.lower() in s_content and s_url != t_url:
                        opp = InternalLinkOpportunity(
                            website_id=website_id,
                            source_url=s_url,
                            target_url=t_url,
                            suggested_anchor=kw,
                            relevance_score=0.85,
                            status="PENDING"
                        )
                        self.db.add(opp)
                        opportunities.append(opp)
                        break

        if opportunities:
            await self.db.commit()
            for opp in opportunities:
                await self.db.refresh(opp)

        return opportunities