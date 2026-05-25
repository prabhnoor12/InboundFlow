from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Attachment(Base):
    __tablename__ = "attachment"
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("inbound_email.id"), nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String)
    size = Column(Integer)
    storage_url = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    inbound_email = relationship("InboundEmail", back_populates="attachments")
