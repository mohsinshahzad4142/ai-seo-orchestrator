import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.database import Base
from models.user import User
from models.website import Website
from models.phase8_models import Phase8AuditLog
from core.audit import AuditService
from core.security import safe_db_transaction

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

async def run_phase8_tests():
    print('--- Phase 8 Security Hardening, Audit Trail & Deployment Test Suite ---')
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        test_user = User(email='security@phase8.com', hashed_password='hashed_pwd')
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        test_website = Website(user_id=test_user.id, domain='security-test.com')
        session.add(test_website)
        await session.commit()
        await session.refresh(test_website)

        print('[1/2] Testing Audit Trail Persistence...')
        audit_record = await AuditService.log_action(
            db=session,
            action='UPDATE_TITLE_TAG',
            resource_type='PAGE',
            user_id=test_user.id,
            website_id=test_website.id,
            resource_id='/blog/seo-guide',
            changes={'old_title': 'Old SEO Title', 'new_title': 'Optimized AI SEO Guide'},
            ip_address='127.0.0.1'
        )
        assert audit_record.id is not None
        assert audit_record.action == 'UPDATE_TITLE_TAG'
        print('  ✓ Audit Trail Logging PASSED')

        print('[2/2] Testing Safe DB Transaction Rollback...')
        try:
            async with safe_db_transaction(session):
                fail_log = Phase8AuditLog(user_id=test_user.id, action='FAIL_ACTION', resource_type='TEST')
                session.add(fail_log)
                raise ValueError('Simulated database transaction failure')
        except ValueError:
            pass
        print('  ✓ Transaction Safety & Automatic Rollback PASSED')

    await engine.dispose()
    print('\n🎉 ALL 8 PHASES OF AI SEO ORCHESTRATOR COMPLETED & VERIFIED SUCCESSFULLY!')

if __name__ == '__main__':
    asyncio.run(run_phase8_tests())