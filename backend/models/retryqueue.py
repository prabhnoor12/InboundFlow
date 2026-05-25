from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base
import enum

class RetryStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class RetryQueue(Base):
    __tablename__ = "retry_queue"
    id = Column(Integer, primary_key=True, index=True)
    webhook_delivery_id = Column(Integer, ForeignKey("webhook_delivery.id"), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    retry_count = Column(Integer, default=0)
    status = Column(Enum(RetryStatus), default=RetryStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    webhook_delivery = relationship("WebhookDelivery", back_populates="retry_queues")
