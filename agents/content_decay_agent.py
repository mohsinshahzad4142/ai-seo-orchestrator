from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase5_models import ContentDecay, DecayAction


class ContentDecayAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_decay(
        self,
        website_id: int,
        pages_metrics: List[Dict[str, Any]]
    ) -> List[ContentDecay]:
        """
        Evaluates page metrics to classify content decay, thin content, and zero-click pages.
        Flagging REDIRECT / MERGE as requires_hitl=True for safe execution.
        """
        decay_records: List[ContentDecay] = []

        for item in pages_metrics:
            url = item.get("url", "")
            word_count = item.get("word_count", 0)
            clicks = item.get("clicks", 0)
            impressions = item.get("impressions", 0)
            traffic_drop_pct = item.get("traffic_drop_pct", 0.0)

            decay_type = None
            action = DecayAction.UPDATE
            requires_hitl = False

            # Thin Content Check
            if word_count < 300:
                decay_type = "thin_content"
                action = DecayAction.MERGE
                requires_hitl = True
            # Zero-click Page Check
            elif impressions > 500 and clicks == 0:
                decay_type = "zero_click"
                action = DecayAction.UPDATE
                requires_hitl = False
            # Traffic Decay Check
            elif traffic_drop_pct >= 30.0:
                decay_type = "traffic_decline"
                action = DecayAction.REDIRECT if traffic_drop_pct >= 70.0 else DecayAction.UPDATE
                requires_hitl = action == DecayAction.REDIRECT

            if decay_type:
                record = ContentDecay(
                    website_id=website_id,
                    url=url,
                    decay_score=round(traffic_drop_pct / 100.0, 2),
                    traffic_drop_pct=traffic_drop_pct,
                    decay_type=decay_type,
                    recommended_action=action,
                    requires_hitl=requires_hitl,
                    details={"word_count": word_count, "clicks": clicks, "impressions": impressions}
                )
                self.db.add(record)
                decay_records.append(record)

        if decay_records:
            await self.db.commit()
            for rec in decay_records:
                await self.db.refresh(rec)

        return decay_records