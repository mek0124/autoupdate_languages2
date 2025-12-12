from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///main.db")


engine = create_engine(
    DATABASE_URL,
    connect_args = {
        "check_same_thread": False,
    }
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def get_session():
    return SessionLocal

def get_base():
    return Base

def get_engine():
    return engine