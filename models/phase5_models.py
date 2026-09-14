import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class DecayAction(str, enum.Enum):
    UPDATE = "UPDATE"
    MERGE = "MERGE"
    REDIRECT = "REDIRECT"


class OptimizationStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    APPLIED = "APPLIED"


class InternalLinkOpportunity(Base):
    __tablename__ = "internal_link_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    source_url = Column(String(500), nullable=False)
    target_url = Column(String(500), nullable=False)
    suggested_anchor = Column(String(255), nullable=False)
    relevance_score = Column(Float, default=0.0)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", backref="internal_links")


class ContentDecay(Base):
    __tablename__ = "content_decay"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    url = Column(String(500), nullable=False)
    decay_score = Column(Float, default=0.0)
    traffic_drop_pct = Column(Float, default=0.0)
    ranking_drop_positions = Column(Float, default=0.0)
    decay_type = Column(String(100), nullable=False)  # e.g., 'zero-click', 'thin', 'declining'
    recommended_action = Column(Enum(DecayAction), default=DecayAction.UPDATE)
    requires_hitl = Column(Boolean, default=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", backref="content_decays")


class ContentVersion(Base):
    __tablename__ = "content_versions"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    url = Column(String(500), nullable=False)
    proposed_title = Column(String(255), nullable=True)
    proposed_meta_description = Column(Text, nullable=True)
    proposed_headings = Column(JSON, nullable=True)
    proposed_faqs = Column(JSON, nullable=True)
    proposed_body = Column(Text, nullable=True)
    readability_score = Column(Float, default=0.0)
    status = Column(Enum(OptimizationStatus), default=OptimizationStatus.PROPOSED)
    created_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", backref="content_versions")