import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.phase8_models import Phase8AuditLog

logger = logging.getLogger('audit')

class AuditService:
    @staticmethod
    async def log_action(db: AsyncSession, action: str, resource_type: str, user_id: Optional[int] = None, website_id: Optional[int] = None, resource_id: Optional[str] = None, changes: Optional[Dict[str, Any]] = None, ip_address: Optional[str] = None) -> Phase8AuditLog:
        audit_entry = Phase8AuditLog(user_id=user_id, website_id=website_id, action=action, resource_type=resource_type, resource_id=resource_id, changes=changes or {}, ip_address=ip_address)
        db.add(audit_entry)
        await db.commit()
        await db.refresh(audit_entry)
        logger.info(f'AUDIT LOG [{action}] on {resource_type} (ID: {resource_id}) by User {user_id}')
        return audit_entry