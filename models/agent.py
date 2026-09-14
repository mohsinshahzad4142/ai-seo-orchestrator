from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from core.database import Base

class AgentStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., "seo_auditor", "content_writer"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    runs = relationship("AgentRun", back_populates="agent", cascade="all, delete-orphan")

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    agent_id: Mapped[int] = mapped_column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    website_id: Mapped[int] = mapped_column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[AgentStatus] = mapped_column(String(20), default=AgentStatus.PENDING, nullable=False)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agent = relationship("Agent", back_populates="runs")
    website = relationship("Website", back_populates="agent_runs")