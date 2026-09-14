import sys
from pathlib import Path

# Project root ko sys.path mein add karein
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from models.user import User
from models.website import Website
from models.phase4_models import ContentGap, CannibalizationIssue, TechnicalIssue, SeverityLevel

from agents.content_gap_agent import ContentGapAgent
from agents.cannibalization_agent import CannibalizationAgent
from agents.technical_seo_agent import TechnicalSEOAgent

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


async def run_phase4_tests():
    print("--- Phase 4 Core Agents Verification Test Suite ---")

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Database Tables Initialize
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Test User & Website Setup
        test_user = User(email="test@phase4.com", hashed_password="hashed_pwd")
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        test_website = Website(user_id=test_user.id, domain="example.com")
        session.add(test_website)
        await session.commit()
        await session.refresh(test_website)

        # [1/3] Testing Search Intent & Content Gap Agent
        print("[1/3] Testing Content Gap Agent...")
        gap_agent = ContentGapAgent(db=session)

        assert gap_agent.classify_intent("buy seo tool") == "Transactional"
        assert gap_agent.classify_intent("best keyword research software") == "Commercial"
        assert gap_agent.classify_intent("what is technical seo") == "Informational"

        gap_record = await gap_agent.analyze_gap(
            website_id=test_website.id,
            target_keyword="python fast API guide",
            target_url="https://example.com/fastapi",
            current_content="Basic introduction to API creation.",
            competitor_topics=["pricing", "key features", "async performance"]
        )

        assert isinstance(gap_record, ContentGap)
        assert gap_record.intent == "Informational"
        assert "async performance" in gap_record.missing_entities
        print("  ✓ Content Gap Agent PASSED")

        # [2/3] Testing Keyword Cannibalization Agent
        print("[2/3] Testing Keyword Cannibalization Agent...")
        cannibal_agent = CannibalizationAgent(db=session)

        mock_gsc_data = [
            {"keyword": "seo audit tool", "url": "https://example.com/tool-page", "clicks": 120, "impressions": 1500},
            {"keyword": "seo audit tool", "url": "https://example.com/blog/seo-tools", "clicks": 30, "impressions": 400},
            {"keyword": "unique term", "url": "https://example.com/unique", "clicks": 50, "impressions": 200},
        ]

        issues = await cannibal_agent.detect_cannibalization(
            website_id=test_website.id,
            gsc_keyword_data=mock_gsc_data
        )

        assert len(issues) == 1
        assert issues[0].keyword == "seo audit tool"
        assert issues[0].primary_url == "https://example.com/tool-page"
        print("  ✓ Keyword Cannibalization Agent PASSED")

        # [3/3] Testing Technical SEO Agent
        print("[3/3] Testing Technical SEO Agent...")
        tech_agent = TechnicalSEOAgent(db=session)

        mock_audit_data = {
            "url": "http://example.com/broken-page",
            "status_code": 404,
            "is_https": False,
            "meta_robots": "noindex, follow",
            "canonical_url": None,
            "redirect_chain_length": 2,
            "title": "",
            "h1": [],
            "schema_present": False,
            "cwv_lcp": 4.5
        }

        tech_issues = await tech_agent.analyze_technical_health(
            website_id=test_website.id,
            audit_data=mock_audit_data
        )

        assert len(tech_issues) >= 5
        critical_issues = [i for i in tech_issues if i.severity == SeverityLevel.CRITICAL]
        assert len(critical_issues) == 2
        print("  ✓ Technical SEO Agent PASSED")

    await engine.dispose()
    print("\n✅ Phase 4 Core Agents Verification Completed Successfully!")


if __name__ == "__main__":
    asyncio.run(run_phase4_tests())