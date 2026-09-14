import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ActionStatus(str, enum.Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    MONITORING = "MONITORING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    action_type = Column(String(100), nullable=False)
    target_url = Column(String(500), nullable=True)
    target_keyword = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)
    status = Column(Enum(ActionStatus), default=ActionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", backref="agent_actions")


class BeforeAfterTracking(Base):
    __tablename__ = "before_after_tracking"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(Integer, ForeignKey("agent_actions.id"), nullable=False)
    url = Column(String(500), nullable=False)
    applied_at = Column(DateTime, default=datetime.utcnow)

    # Baseline (BEFORE) Metrics
    before_clicks = Column(Float, default=0.0)
    before_impressions = Column(Float, default=0.0)
    before_position = Column(Float, default=0.0)

    # Post-Execution (AFTER - 28 Day Delta) Metrics
    after_clicks = Column(Float, nullable=True)
    after_impressions = Column(Float, nullable=True)
    after_position = Column(Float, nullable=True)
    delta_validated = Column(Boolean, default=False)
    validation_date = Column(DateTime, nullable=True)

    action = relationship("AgentAction", backref="tracking")


class OrchestratorRunLog(Base):
    __tablename__ = "orchestrator_run_logs"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    run_id = Column(String(100), nullable=False, unique=True)
    agent_sequence = Column(JSON, nullable=False)
    results = Column(JSON, nullable=True)
    status = Column(String(50), default="RUNNING")
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    website = relationship("Website", backref="orchestrator_logs")