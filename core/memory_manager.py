from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.phase6_models import AgentAction, BeforeAfterTracking, ActionStatus


class MemoryManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_action(
        self,
        website_id: int,
        agent_name: str,
        action_type: str,
        target_url: str,
        target_keyword: str,
        details: Dict[str, Any],
        baseline_metrics: Dict[str, float]
    ) -> AgentAction:
        """
        Logs an executed agent action and establishes baseline performance metrics.
        """
        action = AgentAction(
            website_id=website_id,
            agent_name=agent_name,
            action_type=action_type,
            target_url=target_url,
            target_keyword=target_keyword,
            details=details,
            status=ActionStatus.EXECUTED
        )
        self.db.add(action)
        await self.db.commit()
        await self.db.refresh(action)

        tracking = BeforeAfterTracking(
            action_id=action.id,
            url=target_url,
            applied_at=datetime.utcnow(),
            before_clicks=baseline_metrics.get("clicks", 0.0),
            before_impressions=baseline_metrics.get("impressions", 0.0),
            before_position=baseline_metrics.get("position", 0.0)
        )
        self.db.add(tracking)
        await self.db.commit()
        await self.db.refresh(tracking)

        return action

    async def validate_28day_delta(
        self,
        action_id: int,
        after_metrics: Dict[str, float]
    ) -> BeforeAfterTracking:
        """
        Calculates and validates 28-day performance changes post-optimization.
        """
        result = await self.db.execute(
            select(BeforeAfterTracking).where(BeforeAfterTracking.action_id == action_id)
        )
        tracking = result.scalars().first()

        if not tracking:
            raise ValueError(f"No tracking entry found for action ID {action_id}")

        tracking.after_clicks = after_metrics.get("clicks", 0.0)
        tracking.after_impressions = after_metrics.get("impressions", 0.0)
        tracking.after_position = after_metrics.get("position", 0.0)
        tracking.delta_validated = True
        tracking.validation_date = datetime.utcnow()

        # Update action status
        action_res = await self.db.execute(select(AgentAction).where(AgentAction.id == action_id))
        action = action_res.scalars().first()
        if action:
            action.status = ActionStatus.COMPLETED

        await self.db.commit()
        await self.db.refresh(tracking)
        return tracking