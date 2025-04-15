import os
import pytest
from fastapi.testclient import TestClient


def load_test_file(filename):
    filepath = os.path.join("tests", "test_upload_files", filename)
    return open(filepath, "rb")


def test_create_activity_success(client):
    files = [("files", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))]
    hero = ("hero_image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        "/activities/",
        data={
            "name": "Test Activity",
            "description": "This is a test activity",
            "type": 1,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "address": "123 Test Street",
            "booking_url": "http://example.com/booking",
        },
        files=files + [hero],
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Activity"
    assert data["address"] == "123 Test Street"


def test_create_activity_missing_required_field(client):
    response = client.post(
        "/activities/",
        data={
            # Missing 'name' field
            "type": 1,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "address": "123 Test Street",
            "booking_url": "http://example.com/booking",
        },
    )

    assert response.status_code == 422  # FastAPI's default for missing required fields


def test_create_activity_invalid_lat_long(client):
    response = client.post(
        "/activities/",
        data={
            "name": "Bad Coordinates",
            "type": 1,
            "latitude": "not-a-float",
            "longitude": "not-a-float",
            "address": "Nowhere",
            "booking_url": "http://example.com/booking",
        },
    )

    assert response.status_code == 422


def test_create_activity_multiple_files(client):
    files = [
        ("files", ("img1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("files", ("img2.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("files", ("img3.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
    ]
    hero = ("hero_image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        "/activities/",
        data={
            "name": "Gallery Event",
            "description": "Lots of files",
            "type": 2,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "address": "456 File Lane",
            "booking_url": "http://example.com/book",
        },
        files=files + [hero],
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gallery Event"
