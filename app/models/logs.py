from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database.sync.base import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    module = Column(String, nullable=True)
    func_name = Column(String, nullable=True)
    line_no = Column(Integer, nullable=True)
    extra = Column(JSON, nullable=True)  
