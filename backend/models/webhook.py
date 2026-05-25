from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base
import enum

class WebhookStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class WebhookDelivery(Base):
    __tablename__ = "webhook_delivery"
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("inbound_email.id"), nullable=False)
    target_url = Column(String, nullable=False)
    status = Column(Enum(WebhookStatus), default=WebhookStatus.pending)
    attempt_count = Column(Integer, default=0)
    last_attempt_at = Column(DateTime)
    next_attempt_at = Column(DateTime)
    response_code = Column(Integer)
    response_body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    retry_queues = relationship("RetryQueue", back_populates="webhook_delivery")
    inbound_email = relationship("InboundEmail", back_populates="webhook_deliveries")
