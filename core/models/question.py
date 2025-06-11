from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from .base import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String(50), unique=True, index=True)  # ID de tu YAML
    text = Column(Text, nullable=False)
    options = Column(JSON)  # {"A": "Opción 1", "B": "Opción 2"}
    correct_answer = Column(String(1))  # "A", "B", etc.
    explanation = Column(Text)
    difficulty = Column(String(20))
    tags = Column(JSON)  # ["titulo1", "capitulo2"]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)