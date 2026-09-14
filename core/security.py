from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger('security')

@asynccontextmanager
async def safe_db_transaction(db: AsyncSession):
    try:
        yield db
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f'Database transaction rolled back due to error: {str(e)}')
        raise e