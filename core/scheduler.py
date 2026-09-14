import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class DynamicScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

    def add_dynamic_job(self, func, job_id: str, cron_expression: Optional[str] = None, **kwargs):
        """
        Dynamically registers tasks without hardcoding schedules.
        Falls back to environment configuration or defaults.
        """
        cron_expr = cron_expression or os.getenv("DEFAULT_SEO_AUDIT_CRON", "0 2 * * *")
        trigger = CronTrigger.from_crontab(cron_expr)

        if self.scheduler.get_job(job_id):
            self.scheduler.reschedule_job(job_id, trigger=trigger)
        else:
            self.scheduler.add_job(func, trigger, id=job_id, kwargs=kwargs, replace_existing=True)

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()