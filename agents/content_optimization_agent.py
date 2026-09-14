from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase5_models import ContentVersion, OptimizationStatus


class FAQItem(BaseModel):
    question: str
    answer: str


class OptimizationProposal(BaseModel):
    title: str = Field(..., max_length=70)
    meta_description: str = Field(..., max_length=160)
    headings: List[str] = Field(default_factory=list)
    faqs: List[FAQItem] = Field(default_factory=list)
    body: str
    readability_score: float = Field(default=70.0, ge=0.0, le=100.0)

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v


class ContentOptimizationAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_proposal(
        self,
        current_title: str,
        current_meta: str,
        target_keyword: str,
        missing_entities: List[str]
    ) -> OptimizationProposal:
        """
        Generates an optimized content proposal using structured Pydantic guardrails.
        """
        optimized_title = f"{current_title} - Complete {target_keyword.title()} Guide"[:70]
        optimized_meta = f"Discover everything about {target_keyword}. Covers {', '.join(missing_entities[:2])} and expert strategies."[:160]

        headings = [
            f"Overview of {target_keyword.title()}",
            f"Key Benefits & Features",
            f"Frequently Asked Questions"
        ]

        faqs = [
            FAQItem(
                question=f"What is {target_keyword}?",
                answer=f"{target_keyword.title()} refers to strategic optimization techniques designed to improve site performance."
            )
        ]

        body = f"# {optimized_title}\n\n" + "\n".join([f"## {h}" for h in headings])

        return OptimizationProposal(
            title=optimized_title,
            meta_description=optimized_meta,
            headings=headings,
            faqs=faqs,
            body=body,
            readability_score=75.5
        )

    async def propose_optimization(
        self,
        website_id: int,
        url: str,
        target_keyword: str,
        current_title: str = "",
        current_meta: str = "",
        missing_entities: Optional[List[str]] = None
    ) -> ContentVersion:
        """
        Propose-first workflow: Creates and saves an unapplied proposal in PENDING/PROPOSED state.
        """
        proposal = self.generate_proposal(
            current_title=current_title or "Default Title",
            current_meta=current_meta or "Default Description",
            target_keyword=target_keyword,
            missing_entities=missing_entities or []
        )

        version_record = ContentVersion(
            website_id=website_id,
            url=url,
            proposed_title=proposal.title,
            proposed_meta_description=proposal.meta_description,
            proposed_headings=proposal.headings,
            proposed_faqs=[faq.dict() for faq in proposal.faqs],
            proposed_body=proposal.body,
            readability_score=proposal.readability_score,
            status=OptimizationStatus.PROPOSED
        )

        self.db.add(version_record)
        await self.db.commit()
        await self.db.refresh(version_record)

        return version_record