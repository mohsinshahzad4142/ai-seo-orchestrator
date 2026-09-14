# AI SEO Orchestrator Architecture
Autonomous multi-agent SEO optimization engine built with FastAPI, Next.js, PostgreSQL/SQLite, and Celery.

## Features
- **Multi-Agent SEO Pipeline:** Content Decay Agent, Internal Links Engine, Keyword Cannibalization Fixer.
- **HITL Gate:** Human-in-the-loop review queue before publishing live site changes.
- **Audit Logging:** Full persistent audit logs for security and compliance.
- **Multi-Channel Alerts:** Slack, Telegram, and Email notifications.

## Quick Start (Docker)
```bash
docker-compose up --build -d