import asyncio
from workers.celery_app import celery_app
from core.database import AsyncSessionLocal
from orchestrator.engine import OrchestratorEngine


@celery_app.task(name="tasks.run_orchestrator_pipeline")
def run_orchestrator_pipeline_task(website_id: int, initial_context: dict):
    """
    Background worker task wrapping the async Orchestrator engine pipeline.
    """
    async def _execute():
        async with AsyncSessionLocal() as session:
            engine = OrchestratorEngine(db=session)
            # Pipeline triggers asynchronously inside Celery worker context
            result = await engine.run_pipeline(website_id=website_id, initial_context=initial_context)
            return result.run_id if result else None

    return asyncio.run(_execute())