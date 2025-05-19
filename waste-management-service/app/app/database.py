import uuid
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

Base = declarative_base()


def get_engine(testing: bool = False):
    url = DATABASE_URL

    if testing:
        db_name = f"file:{uuid.uuid4().hex}?mode=memory"
        url = "sqlite:///" + db_name

    return create_engine(
        url, connect_args={"check_same_thread": False} if testing else {}
    )


def get_session(testing: bool = False):
    engine = get_engine(testing)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = get_session()
