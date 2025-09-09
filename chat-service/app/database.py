from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL (adjust to your docker-compose setup)
# Example: postgres://user:password@db:5432/chat_db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatuser:chatpass@db:5432/chatdb")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 👇 this is the Base your models need
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()