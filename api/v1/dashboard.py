from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from models.phase6_models import AgentAction, BeforeAfterTracking
from models.phase7_models import ApprovalRequest, ApprovalStatus

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
async def get_dashboard_overview(website_id: int, db: AsyncSession = Depends(get_db)):
    # Pending approvals count
    pending_res = await db.execute(
        select(ApprovalRequest).where(
            ApprovalRequest.website_id == website_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        )
    )
    pending_count = len(pending_res.scalars().all())

    # Total actions executed
    actions_res = await db.execute(
        select(AgentAction).where(AgentAction.website_id == website_id)
    )
    actions = actions_res.scalars().all()

    return {
        "health_score": 88.5,
        "total_actions_executed": len(actions),
        "pending_approvals_count": pending_count,
        "status": "OPERATIONAL"
    }


@router.get("/before-after")
async def get_before_after_tracking(website_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BeforeAfterTracking)
        .join(AgentAction)
        .where(AgentAction.website_id == website_id)
    )
    return result.scalars().all()