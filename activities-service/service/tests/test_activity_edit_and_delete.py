import os
import pytest
from fastapi.testclient import TestClient

from app.models.dto.models import ActivityEditDTO


def test_edit_activity_success(client):
    data: ActivityEditDTO = ActivityEditDTO(
        id=1,
        name="Updated Activity",
        description="This is an updated test activity",
        type=1,
        latitude=37.7749,
        longitude=-122.4194,
        address="456 Updated Street",
        booking_url="http://example.com/updated_booking",
    )

    response = client.post(
        "/activities/edit",
        data=data.model_dump_json(),
    )

    assert response.status_code == 200


def test_edit_activity_invalid_id(client):
    data: ActivityEditDTO = ActivityEditDTO(
        id=9999,  # Assuming this ID does not exist
        name="Nonexistent Activity",
        description="This activity does not exist",
        type=1,
        latitude=37.7749,
        longitude=-122.4194,
        address="Nowhere",
        booking_url="http://example.com/booking",
    )

    response = client.post(
        "/activities/edit",
        data=data.model_dump_json(),
    )

    assert response.status_code == 404  # Not Found for non-existent ID


def test_edit_activity_missing_required_field(client):
    data: ActivityEditDTO = ActivityEditDTO(
        id=1,
        name="sdfn",
        description="This is a test activity",
        type=1,
        latitude=37.7749,
        longitude=-122.4194,
        address="123 Test Street",
        booking_url="http://example.com/booking",
    )

    data.name = None

    response = client.post(
        "/activities/edit",
        data=data.model_dump(),
    )

    assert response.status_code == 422  # FastAPI's default for missing required fields


def test_edit_activity_invalid_lat_long(client):
    data: ActivityEditDTO = ActivityEditDTO(
        id=1,
        name="Bad Coordinates",
        type=1,
        latitude=0,
        longitude=0,
        address="Nowhere",
        booking_url="http://example.com/booking",
    )

    data.latitude = "not-a-float"
    data.longitude = "not-a-float"

    response = client.post(
        "/activities/edit",
        data=data.model_dump(),
    )

    assert response.status_code == 422


def test_delete_activity_success(client):
    response = client.delete("/activities/1")

    assert response.status_code == 200


def test_delete_activity_not_found(client):
    response = client.delete("/activities/9999999")

    assert response.status_code == 404


def test_delete_activity_invalid_id(client):
    response = client.delete("/activities/invalid_id")

    assert response.status_code == 422
