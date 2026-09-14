import sys
from pathlib import Path

# Resolve root path for import handling
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from models.user import User
from models.website import Website
from models.phase5_models import ContentVersion, InternalLinkOpportunity, ContentDecay, DecayAction, OptimizationStatus

from agents.content_optimization_agent import ContentOptimizationAgent
from agents.internal_linking_agent import InternalLinkingAgent
from agents.performance_analytics_agent import PerformanceAnalyticsAgent
from agents.content_decay_agent import ContentDecayAgent

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


async def run_phase5_tests():
    print("--- Phase 5 Core Agents Verification Test Suite ---")

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Setup test data
        test_user = User(email="test@phase5.com", hashed_password="hashed_pwd")
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        test_website = Website(user_id=test_user.id, domain="example.com")
        session.add(test_website)
        await session.commit()
        await session.refresh(test_website)

        # 1. Agent 6 Test: Content Optimization
        print("[1/4] Testing Content Optimization Agent (Propose-First)...")
        opt_agent = ContentOptimizationAgent(db=session)
        proposal = await opt_agent.propose_optimization(
            website_id=test_website.id,
            url="https://example.com/blog/seo",
            target_keyword="technical seo",
            missing_entities=["crawl budget", "sitemap index"]
        )
        assert proposal.status == OptimizationStatus.PROPOSED
        assert "technical seo" in proposal.proposed_title.lower()
        print("  ✓ Content Optimization Agent PASSED")

        # 2. Agent 7 Test: Internal Linking Agent
        print("[2/4] Testing Internal Linking Agent...")
        link_agent = InternalLinkingAgent(db=session)
        mock_pages = [
            {"url": "https://example.com/orphan-page", "inbound_links": 1, "top_keywords": ["fastapi python"]},
            {"url": "https://example.com/hub-page", "inbound_links": 10, "content": "Learn how to use fastapi python for APIs."}
        ]
        link_opps = await link_agent.discover_link_opportunities(website_id=test_website.id, pages_data=mock_pages)
        assert len(link_opps) == 1
        assert link_opps[0].suggested_anchor == "fastapi python"
        print("  ✓ Internal Linking Agent PASSED")

        # 3. Agent 8 Test: Performance & Analytics Agent
        print("[3/4] Testing Performance & Analytics Agent...")
        perf_agent = PerformanceAnalyticsAgent()
        curr = {"clicks": 80.0, "impressions": 1000.0}
        prev = {"clicks": 120.0, "impressions": 1100.0}
        trend_report = perf_agent.analyze_performance_trends(curr, prev, period_label="28D")
        assert trend_report["has_alerts"] is True
        assert len(trend_report["alerts"]) > 0
        print("  ✓ Performance & Analytics Agent PASSED")

        # 4. Agent 9 Test: Content Decay Agent
        print("[4/4] Testing Content Decay Agent...")
        decay_agent = ContentDecayAgent(db=session)
        mock_decay_pages = [
            {"url": "https://example.com/thin", "word_count": 150, "clicks": 10, "impressions": 200, "traffic_drop_pct": 10.0},
            {"url": "https://example.com/declining", "word_count": 1200, "clicks": 5, "impressions": 50, "traffic_drop_pct": 75.0}
        ]
        decays = await decay_agent.detect_decay(website_id=test_website.id, pages_metrics=mock_decay_pages)
        assert len(decays) == 2
        # Destructive action check (REDIRECT requiring HITL approval)
        redirect_decay = next(d for d in decays if d.recommended_action == DecayAction.REDIRECT)
        assert redirect_decay.requires_hitl is True
        print("  ✓ Content Decay Agent PASSED")

    await engine.dispose()
    print("\n✅ Phase 5 Core Agents Verification Completed Successfully!")


if __name__ == "__main__":
    asyncio.run(run_phase5_tests())