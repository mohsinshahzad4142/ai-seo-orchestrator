import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from models.user import User
from models.website import Website
from models.phase7_models import ApprovalRequest, ApprovalStatus, NotificationChannel
from core.notifications import NotificationService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


async def run_phase7_tests():
    print("--- Phase 7 Core Dashboard, HITL & Notifications Test Suite ---")

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        test_user = User(email="test@phase7.com", hashed_password="hashed_pwd")
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        test_website = Website(user_id=test_user.id, domain="example.com")
        session.add(test_website)
        await session.commit()
        await session.refresh(test_website)

        print("[1/2] Testing HITL Approval Queue Gate...")
        approval = ApprovalRequest(
            website_id=test_website.id,
            agent_name="ContentDecayAgent",
            action_type="REDIRECT",
            target_url="https://example.com/decayed-page",
            payload={"redirect_to": "https://example.com/target-page"},
            status=ApprovalStatus.PENDING
        )
        session.add(approval)
        await session.commit()
        await session.refresh(approval)

        assert approval.status == ApprovalStatus.PENDING

        approval.status = ApprovalStatus.APPROVED
        await session.commit()
        await session.refresh(approval)

        assert approval.status == ApprovalStatus.APPROVED
        print("  ✓ HITL Approval Queue Gate PASSED")

        print("[2/2] Testing Notification Service Dispatches...")
        notifier = NotificationService()
        email_sent = await notifier.notify(
            channel=NotificationChannel.EMAIL,
            recipient="admin@example.com",
            message="Test Notification"
        )
        assert email_sent is True
        print("  ✓ Notification Service PASSED")

    await engine.dispose()
    print("\n✅ Phase 7 Core Verification Completed Successfully!")


if __name__ == "__main__":
    asyncio.run(run_phase7_tests())
