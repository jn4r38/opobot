from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from datetime import datetime
from .base import Base

class ReportStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String(50), nullable=False)
    question_text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(String(50), nullable=False)  # "format", "duplicate", "content"
    comment = Column(Text)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolved_by = Column(String(100))
    
    # Relaciones (opcional)
    # user = relationship("User", back_populates="reports")