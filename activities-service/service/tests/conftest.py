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
from app.models.db.models import Activity, ActivityReview, Image, ActivityImage
from app.models.enums.enums import ActivityType
from app.services.auth_service import (
    authenticate_request,
    authenticate_request_with_user,
    authentication_override,
)


TEST_DATABASE_URL_WITHOUT_DB_NAME = os.getenv("TEST_DATABASE_URL_WITHOUT_DB_NAME")
BASE_TEST_URL = "/api/activities"


@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh test DB and seeds it before each test."""

    db_name = f"test{uuid.uuid4().hex.replace('-', '')}"
    db_url = f"{TEST_DATABASE_URL_WITHOUT_DB_NAME}/{db_name}"

    admin_engine = create_engine(f"{TEST_DATABASE_URL_WITHOUT_DB_NAME}/postgres")

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
                created_by=1,
                updated_by=1,
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
                created_by=1,
                updated_by=1,
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

        activity_reviews = [
            ActivityReview(
                id=1,
                activity_id=1,
                user_id=1,
                review_text="Great festival!",
                rating=5,
                created_at=datetime.datetime.now(),
            ),
            ActivityReview(
                id=2,
                activity_id=1,
                user_id=1,
                review_text="Amazing concert!",
                rating=4,
                created_at=datetime.datetime.now(),
            ),
        ]
        session.add_all(activity_reviews)
        session.commit()

        # reset the sequence for the activities table
        session.execute(
            text("SELECT setval('activities_id_seq', (SELECT MAX(id) FROM activities))")
        )
        # reset the sequence for the activity_reviews table
        session.execute(
            text(
                "SELECT setval('activity_reviews_id_seq', (SELECT MAX(id) FROM activity_reviews))"
            )
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

    def override_authenticate_request():
        return {
            "app": {
                "status": "authorised",
                "application": "test",
                "resource": "activities-services",
                "permission": "admin",
            },
            "user": {
                "status": "authorised",
                "user": {"id": 1, "email": "admin@admin.com"},
                "permission": "read,write",
                "user_types": [
                    "resident",
                    "tourist",
                    "property-developer",
                    "planning-department",
                    "law-enforcement",
                    "waste-management",
                    "health-services",
                    "community-services",
                    "business-owner",
                    "restaurant-owner",
                    "accommodation-provider",
                    "building-inspector",
                    "environmental-officer",
                    "funeral-home",
                    "event-organizer",
                    "library-staff",
                    "business-support",
                    "fire-department",
                ],
            },
        }

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[authentication_override] = override_authenticate_request

    from fastapi.testclient import TestClient

    return TestClient(app)
