import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.phase6_models import OrchestratorRunLog

logger = logging.getLogger("orchestrator")


class OrchestratorEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent_registry: Dict[str, Callable] = {}
        self.dependency_graph: Dict[str, List[str]] = {}

    def register_agent(self, name: str, runner_fn: Callable, dependencies: Optional[List[str]] = None):
        self.agent_registry[name] = runner_fn
        self.dependency_graph[name] = dependencies or []

    async def run_pipeline(self, website_id: int, initial_context: Dict[str, Any]) -> Optional[OrchestratorRunLog]:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        
        active_run = await self.db.execute(
            select(OrchestratorRunLog).where(
                OrchestratorRunLog.website_id == website_id,
                OrchestratorRunLog.status == "RUNNING"
            )
        )
        if active_run.scalars().first():
            logger.warning(f"Pipeline execution skipped. Active run in progress for website {website_id}.")
            return None

        log_record = OrchestratorRunLog(
            website_id=website_id,
            run_id=run_id,
            agent_sequence=list(self.agent_registry.keys()),
            results={},
            status="RUNNING"
        )
        self.db.add(log_record)
        await self.db.commit()
        await self.db.refresh(log_record)

        context = initial_context.copy()
        execution_results = {}

        for agent_name, agent_fn in self.agent_registry.items():
            deps = self.dependency_graph.get(agent_name, [])
            failed_deps = [d for d in deps if execution_results.get(d, {}).get("status") == "FAILED"]
            
            if failed_deps:
                execution_results[agent_name] = {
                    "status": "SKIPPED",
                    "reason": f"Dependencies failed: {failed_deps}"
                }
                continue

            try:
                logger.info(f"Executing Agent: {agent_name}")
                output = await agent_fn(self.db, website_id, context)
                execution_results[agent_name] = {"status": "SUCCESS", "output": output}
                context[agent_name] = output
            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {str(e)}")
                execution_results[agent_name] = {
                    "status": "FAILED",
                    "error": str(e)
                }

        log_record.results = execution_results
        log_record.status = "COMPLETED"
        log_record.completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(log_record)
        return log_record
