import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from core.database import Base

class OpportunityPriority(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RecommendationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    APPLIED = "APPLIED"

class SEOOpportunity(Base):
    __tablename__ = "seo_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    query = Column(String(255), nullable=False)
    page_url = Column(String(500), nullable=False)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    position = Column(Float, default=0.0)
    priority = Column(SQLEnum(OpportunityPriority), default=OpportunityPriority.MEDIUM)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IndexingStatus(Base):
    __tablename__ = "indexing_status"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False, index=True)
    verdict = Column(String(50), nullable=True)
    coverage_state = Column(String(100), nullable=True)
    robots_txt_state = Column(String(50), nullable=True)
    indexing_state = Column(String(50), nullable=True)
    last_crawled_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("seo_opportunities.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    action_type = Column(String(100), nullable=False)
    suggested_changes = Column(JSON, nullable=False)
    status = Column(SQLEnum(RecommendationStatus), default=RecommendationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))