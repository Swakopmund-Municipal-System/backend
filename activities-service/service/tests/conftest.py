import datetime
import sys
import os
import uuid

# force add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine, make_url, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db, get_engine, get_session
from app.models.db.models import Activity, Image, ActivityImage
from app.models.enums.enums import ActivityType


@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh test DB and seeds it before each test."""

    db_name = f"test{uuid.uuid4().hex.replace('-', '')}"
    db_url = f"postgresql://postgres:postgres@db/{db_name}"

    admin_engine = create_engine(f"postgresql://postgres:postgres@db/postgres")

    admin_conn = admin_engine.connect()
    admin_conn.execution_options(isolation_level="AUTOCOMMIT")
    admin_conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
    admin_conn.execute(text(f"CREATE DATABASE {db_name}"))
    admin_conn.close()

    try:
        engine = get_engine(use_url=db_url)

        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))

        Base.metadata.create_all(bind=engine)
        TestingSession = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        session = TestingSession()

        # ---- seeding ----

        images = [
            Image(
                id=1,
                name="Image 1",
                filepath="path/to/image1.jpg",
            ),
            Image(
                id=2,
                name="Image 2",
                filepath="path/to/image2.jpg",
            ),
        ]
        session.add_all(images)
        session.commit()

        # Reset the sequence for the images table
        session.execute(
            text("SELECT setval('images_id_seq', (SELECT MAX(id) FROM images))")
        )

        # test get all images
        images = session.query(Image).all()
        assert len(images) == 2, "Failed to seed images"
        print(f"Seeded {len(images)} images.")

        activities = [
            Activity(
                id=1,
                type=ActivityType.FESTIVAL,
                name="Festival 1",
                description="Description for Festival 1",
                address="123 Festival St, City, Country",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                created_by=uuid.uuid4(),
                updated_by=uuid.uuid4(),
                booking_url="http://example.com/booking",
                hero_image_id=1,
                latitude=-22.592063343286743,
                longitude=17.080047073592386,
                point_geom="SRID=4326;POINT(17.080047073592386 -22.592063343286743)",
            ),
            Activity(
                id=2,
                type=ActivityType.RECREATIONAL,
                name="Concert 1",
                description="Description for Concert 1",
                address="456 Concert Ave, City, Country",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                created_by=uuid.uuid4(),
                updated_by=uuid.uuid4(),
                booking_url="http://example.com/booking",
                hero_image_id=2,
                latitude=-22.54742520993337,
                longitude=17.076575094549124,
                point_geom="SRID=4326;POINT(17.076575094549124 -22.54742520993337)",
            ),
        ]
        session.add_all(activities)
        session.commit()
        activity_images = [
            ActivityImage(
                image_id=1,
                activity_id=1,
            ),
            ActivityImage(
                image_id=2,
                activity_id=1,
            ),
        ]
        session.add_all(activity_images)
        session.commit()

        # reset the sequence for the activities table
        session.execute(
            text("SELECT setval('activities_id_seq', (SELECT MAX(id) FROM activities))")
        )

        # ------ end of seeding ------

        yield session

        session.close()
        Base.metadata.drop_all(bind=engine)

    finally:
        admin_conn = admin_engine.connect()
        admin_conn.execution_options(isolation_level="AUTOCOMMIT")
        admin_conn.execute(
            text(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                AND pid <> pg_backend_pid();
            """
            )
        )
        admin_conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        admin_conn.close()


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
