import sys
from pathlib import Path

# Add project root path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from models.user import User
from models.website import Website
from models.phase6_models import AgentAction, BeforeAfterTracking, ActionStatus

from core.memory_manager import MemoryManager
from orchestrator.engine import OrchestratorEngine

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


async def dummy_agent_1(db, website_id, context):
    return {"data": "agent_1_done"}


async def dummy_agent_2(db, website_id, context):
    if "agent_1" not in context:
        raise RuntimeError("Missing context from Agent 1")
    return {"data": "agent_2_done"}


async def run_phase6_tests():
    print("--- Phase 6 Core Engine & Memory Test Suite ---")

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Setup Test User/Website
        test_user = User(email="test@phase6.com", hashed_password="hashed_pwd")
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        test_website = Website(user_id=test_user.id, domain="example.com")
        session.add(test_website)
        await session.commit()
        await session.refresh(test_website)

        # 1. Test Agent Memory Manager
        print("[1/2] Testing Memory Manager (BEFORE/AFTER Delta)...")
        memory_mgr = MemoryManager(db=session)
        action = await memory_mgr.log_action(
            website_id=test_website.id,
            agent_name="ContentOptimizationAgent",
            action_type="TITLE_UPDATE",
            target_url="https://example.com/page1",
            target_keyword="python seo",
            details={"title": "New Title"},
            baseline_metrics={"clicks": 10.0, "impressions": 100.0, "position": 15.0}
        )
        assert action.status == ActionStatus.EXECUTED

        tracking = await memory_mgr.validate_28day_delta(
            action_id=action.id,
            after_metrics={"clicks": 25.0, "impressions": 250.0, "position": 8.0}
        )
        assert tracking.delta_validated is True
        assert tracking.after_clicks == 25.0
        print("  ✓ Memory Manager PASSED")

        # 2. Test Orchestrator Core Engine
        print("[2/2] Testing Orchestrator Core Engine...")
        orchestrator = OrchestratorEngine(db=session)
        orchestrator.register_agent("agent_1", dummy_agent_1)
        orchestrator.register_agent("agent_2", dummy_agent_2, dependencies=["agent_1"])

        log_record = await orchestrator.run_pipeline(
            website_id=test_website.id,
            initial_context={"init": True}
        )

        assert log_record.status == "COMPLETED"
        assert log_record.results["agent_1"]["status"] == "SUCCESS"
        assert log_record.results["agent_2"]["status"] == "SUCCESS"
        print("  ✓ Orchestrator Core Engine PASSED")

    await engine.dispose()
    print("\n✅ Phase 6 Core Orchestration & Memory Verification Completed Successfully!")


if __name__ == "__main__":
    asyncio.run(run_phase6_tests())