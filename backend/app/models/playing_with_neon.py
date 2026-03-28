from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class DBPwn(Base):
    __tablename__ = "playing_with_neon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(String, nullable=True)