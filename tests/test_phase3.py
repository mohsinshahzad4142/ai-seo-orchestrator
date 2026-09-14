import sys
import os
import asyncio

# Project root ko path mein inject karein
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.database import Base
from models.seo import OpportunityPriority, RecommendationStatus
from agents.opportunity_agent import SEOOpportunityAgent
from agents.indexing_agent import IndexingAgent
from agents.reporting_agent import ReportingAgent

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async def run_phase3_tests():
    print("--- Phase 3 Core Agents Verification Test Suite ---")
    
    # In-memory SQLite DB initialize karein
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with AsyncSessionLocal() as session:
        # 1. SEO Opportunity Agent Test
        print("[1/3] Testing SEO Opportunity Agent...")
        opp_agent = SEOOpportunityAgent(session)
        mock_gsc_data = [
            {
                "keys": ["buy running shoes", "https://example.com/shoes"],
                "position": 10.5,
                "impressions": 600,
                "clicks": 5,
                "ctr": 0.008
            },
            {
                "keys": ["cheap sneakers", "https://example.com/sneakers"],
                "position": 4.0,  # Position 8 se kam hone ki waja se filter ho jayega
                "impressions": 1000,
                "clicks": 100,
                "ctr": 0.1
            }
        ]
        opps = await opp_agent.process_gsc_data(website_id=1, gsc_rows=mock_gsc_data)
        assert len(opps) == 1
        assert opps[0].query == "buy running shoes"
        assert opps[0].priority == OpportunityPriority.HIGH
        print("  ✓ Opportunity Agent PASSED")

        # 2. Indexing Agent Test
        print("[2/3] Testing Indexing Agent...")
        idx_agent = IndexingAgent(session)
        mock_inspection = {
            "indexStatusResult": {
                "verdict": "NEUTRAL",
                "coverageState": "Discovered - currently not indexed",
                "robotsTxtState": "ALLOWED",
                "indexingState": "INDEXING_ALLOWED"
            }
        }
        idx_record = await idx_agent.process_url_inspection(
            website_id=1,
            url="https://example.com/shoes",
            inspection_data=mock_inspection
        )
        assert idx_record.verdict == "NEUTRAL"
        assert idx_record.coverage_state == "Discovered - currently not indexed"
        print("  ✓ Indexing Agent PASSED")

        # 3. Reporting & Decision Agent Test
        print("[3/3] Testing Reporting & Decision Agent...")
        rep_agent = ReportingAgent(session)
        
        # Create Recommendation
        rec = await rep_agent.create_recommendation(
            website_id=1,
            title="Optimize Title Tag for Running Shoes",
            action_type="UPDATE_META",
            suggested_changes={"title": "Buy Premium Running Shoes Online"},
            opportunity_id=opps[0].id
        )
        assert rec.status == RecommendationStatus.PENDING
        
        # Update Decision
        updated_rec = await rep_agent.update_decision(rec.id, RecommendationStatus.APPROVED)
        assert updated_rec.status == RecommendationStatus.APPROVED
        
        # Generate Summary
        summary = await rep_agent.generate_site_summary(website_id=1)
        assert summary["total_opportunities"] == 1
        assert summary["website_id"] == 1
        print("  ✓ Reporting & Decision Agent PASSED")

    await engine.dispose()
    print("\n✅ Phase 3 Core Agents Verification Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(run_phase3_tests())