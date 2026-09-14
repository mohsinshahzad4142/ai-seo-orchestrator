from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase4_models import ContentGap


class ContentGapAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    def classify_intent(self, keyword: str) -> str:
        """
        Classifies keyword search intent (Informational, Commercial, Transactional, Navigational).
        """
        kw = keyword.lower()
        if any(term in kw for term in ["buy", "price", "order", "cheap", "cost", "discount"]):
            return "Transactional"
        elif any(term in kw for term in ["best", "top", "vs", "review", "comparison", "alternative"]):
            return "Commercial"
        elif any(term in kw for term in ["login", "portal", "official", "website"]):
            return "Navigational"
        else:
            return "Informational"

    async def analyze_gap(
        self,
        website_id: int,
        target_keyword: str,
        target_url: Optional[str] = None,
        current_content: str = "",
        competitor_topics: Optional[List[str]] = None,
    ) -> ContentGap:
        """
        Analyzes target keyword content gaps against competitor topics & intent.
        """
        intent = self.classify_intent(target_keyword)

        # Missing entities & questions identification logic
        standard_entities = ["pricing", "key features", "pros & cons", "use cases", "specifications"]
        if competitor_topics:
            all_topics = list(set(standard_entities + competitor_topics))
        else:
            all_topics = standard_entities

        content_lower = current_content.lower()
        missing_entities = [topic for topic in all_topics if topic.lower() not in content_lower]

        standard_questions = [
            f"What is {target_keyword}?",
            f"How does {target_keyword} work?",
            f"Why choose {target_keyword}?",
        ]
        missing_questions = [q for q in standard_questions if q.lower() not in content_lower]

        # Natural language recommendation generation
        rec_parts = [
            f"Target Keyword: '{target_keyword}' | Search Intent: {intent}.",
            f"Content Depth Recommendation: Expand page content at '{target_url or 'N/A'}'."
        ]
        if missing_entities:
            rec_parts.append(f"• Add key missing subtopics: {', '.join(missing_entities)}.")
        if missing_questions:
            rec_parts.append(f"• Add FAQ section answering: {'; '.join(missing_questions)}.")

        recommendation_text = "\n".join(rec_parts)

        # Save gap result in database
        gap_record = ContentGap(
            website_id=website_id,
            target_keyword=target_keyword,
            intent=intent,
            target_url=target_url,
            missing_entities=missing_entities,
            missing_questions=missing_questions,
            recommendation=recommendation_text,
        )

        self.db.add(gap_record)
        await self.db.commit()
        await self.db.refresh(gap_record)

        return gap_record