from sqlalchemy import Column, Integer, String
from app.database.sync.base import Base

class Dummy(Base):
    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
