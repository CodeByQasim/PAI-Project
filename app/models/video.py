from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    output_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)
    resolution = Column(String, nullable=True)
    format = Column(String, nullable=True)
    status = Column(String, default="uploaded")
    ai_prompt = Column(String, nullable=True)
    ai_response = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="videos")
    transcript = relationship("Transcript", back_populates="video")
