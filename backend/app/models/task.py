from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class DBTask(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    # NEW: The Foreign Key linking to the projects table
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    # NEW: The SQLAlchemy relationship to easily access the project object
    project = relationship("DBProject", back_populates="tasks")