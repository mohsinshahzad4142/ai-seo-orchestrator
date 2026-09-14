from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
import enum
from sqlalchemy.orm import relationship
from core.database import Base


class SeverityLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ContentGap(Base):
    __tablename__ = "content_gaps"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    target_keyword = Column(String(255), nullable=False)
    intent = Column(String(100), nullable=True)  # Informational, Commercial, etc.
    target_url = Column(String(500), nullable=True)
    missing_entities = Column(JSON, nullable=True)  # List of entities/topics
    missing_questions = Column(JSON, nullable=True)  # List of missing Q&A
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    website = relationship("Website", backref="content_gaps")


class CannibalizationIssue(Base):
    __tablename__ = "cannibalization_issues"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(255), nullable=False)
    competing_urls = Column(JSON, nullable=False)  # List of conflicting URLs with GSC metrics
    primary_url = Column(String(500), nullable=True)  # Recommended main URL
    action_plan = Column(Text, nullable=True)  # Consolidation / re-linking steps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    website = relationship("Website", backref="cannibalization_issues")


class TechnicalIssue(Base):
    __tablename__ = "technical_issues"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    issue_type = Column(String(100), nullable=False)  # e.g., 404_ERROR, MISSING_ALT, NOINDEX
    severity = Column(Enum(SeverityLevel), default=SeverityLevel.MEDIUM, nullable=False)
    details = Column(JSON, nullable=True)  # Diagnostics metadata
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    website = relationship("Website", backref="technical_issues")