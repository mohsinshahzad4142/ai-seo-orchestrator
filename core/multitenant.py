from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.website import Website

class CredentialManager:
    @staticmethod
    async def get_website_credentials(website_id: int, db: AsyncSession) -> Optional[Dict[str, Any]]:
        result = await db.execute(select(Website).where(Website.id == website_id))
        website = result.scalars().first()
        if not website or not website.credentials:
            return None
        return website.credentials