from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True)
    text = Column(String)
    category = Column(String)  # Formato: tema/subtema/artículo
    difficulty = Column(Integer)
    options = Column(String)  # JSON serializado

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    question_id = Column(String, ForeignKey('questions.id'))
    reason = Column(String)
    comment = Column(String)
