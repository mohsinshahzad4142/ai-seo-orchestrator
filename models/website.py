from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    domain = Column(String(255), nullable=False)
    gsc_site_url = Column(String(500), nullable=True)
    ga4_property_id = Column(String(100), nullable=True)
    wp_url = Column(String(500), nullable=True)
    wp_username = Column(String(100), nullable=True)
    wp_application_password = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="websites")
    audit_logs = relationship("AuditLog", back_populates="website", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="website", cascade="all, delete-orphan")