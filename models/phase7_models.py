import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class NotificationChannel(str, enum.Enum):
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    TELEGRAM = "TELEGRAM"


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    action_type = Column(String(100), nullable=False)
    target_url = Column(String(500), nullable=True)
    payload = Column(JSON, nullable=False)
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    reviewer_comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    website = relationship("Website", backref="approval_requests")


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    recipient = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="SENT")
    sent_at = Column(DateTime, default=datetime.utcnow)

    website = relationship("Website", backref="notifications")
