import datetime
import sys
import os
import uuid

# force add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base, get_engine, get_session
from app.models.db.models import MissedWastePickups
from app.models.enums.enums import MissedWastePickupStatusEnum


@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh test DB and seeds it before each test."""

    engine = get_engine(testing=True)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()

    db_file_path = engine.url.database

    # ---- missed waste pickup seeding ----

    missed_waste_pickups = [
        MissedWastePickups(
            id=1,
            description="missed waste pickup 1 -- PENDING",
            date=datetime.datetime.strptime("2023-10-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
            address="123 Main St",
            status=MissedWastePickupStatusEnum.PENDING_REVIEW,
            userId=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
        ),
        MissedWastePickups(
            id=2,
            description="missed waste pickup 2 -- REVIEWED",
            date=datetime.datetime.strptime("2023-10-02 12:00:00", "%Y-%m-%d %H:%M:%S"),
            address="456 Elm St",
            status=MissedWastePickupStatusEnum.REVIEWED,
            userId=uuid.UUID("123e4567-e89b-12d3-a456-426614174001"),
        ),
    ]

    session.add_all(missed_waste_pickups)
    session.commit()

    # ------ end of missed waste pickup seeding ------

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

    if os.path.exists(db_file_path):
        os.remove(db_file_path)


@pytest.fixture(scope="function")
def client(test_db):

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient

    return TestClient(app)
