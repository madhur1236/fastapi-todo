from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False)

Base = declarative_base()

def get_db() : 
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()