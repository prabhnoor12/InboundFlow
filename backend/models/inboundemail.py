from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class InboundEmail(Base):
    __tablename__ = "inbound_email"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    subject = Column(String)
    body_text = Column(Text)
    body_html = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="received")
    raw_headers = Column(Text)
    sanitized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="inbound_emails")
    attachments = relationship("Attachment", back_populates="inbound_email")
    webhook_deliveries = relationship("WebhookDelivery", back_populates="inbound_email")
