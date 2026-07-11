from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transcript_text = Column(String, nullable=False)
    srt_path = Column(String, nullable=True)
    language = Column(String, nullable=True)
    whisper_model = Column(String, default="base")
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="transcript")
