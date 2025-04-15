import uuid
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://postgres:postgres@db/{uuid.uuid4().hex.replace('-', '')}",
)

Base = declarative_base()


def get_engine(use_url=""):
    url = DATABASE_URL

    if len(use_url) > 0:
        url = use_url

    return create_engine(url)


def get_session(use_url: str = ""):
    engine = get_engine(use_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = get_session()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
