from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
