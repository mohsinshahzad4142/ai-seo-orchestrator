from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from core.database import get_db
from models.phase7_models import ApprovalRequest, ApprovalStatus

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("/pending")
async def get_pending_approvals(website_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ApprovalRequest).where(
            ApprovalRequest.website_id == website_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        )
    )
    return result.scalars().all()


@router.post("/{approval_id}/review")
async def review_approval(
    approval_id: int,
    action: str,  # 'APPROVE' or 'REJECT'
    comment: str = "",
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
    approval = result.scalars().first()

    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    if action.upper() == "APPROVE":
        approval.status = ApprovalStatus.APPROVED
    elif action.upper() == "REJECT":
        approval.status = ApprovalStatus.REJECTED
    else:
        raise HTTPException(status_code=400, detail="Invalid review action")

    approval.reviewer_comment = comment
    approval.reviewed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(approval)

    return {"status": "success", "approval_id": approval_id, "new_status": approval.status}