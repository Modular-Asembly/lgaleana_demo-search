from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.sql_adaptor import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=True)
