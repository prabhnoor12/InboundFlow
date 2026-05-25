from sqlalchemy import Column, Integer, String
from backend.database import Base

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    inbound_emails = relationship("InboundEmail", back_populates="user")
    process_addresses = relationship("ProcessAddress", back_populates="user")
