from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, index=True)
    sender_id = Column(Integer, index=True)
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
