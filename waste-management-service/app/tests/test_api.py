import pytest
from fastapi.testclient import TestClient
from app.models.dto.models import (
    CreateMissedWastePickupDto,
    UpdateMissedWastePickupStatusDto,
)
from app.models.enums.enums import MissedWastePickupStatusEnum


def test_create_missed_waste_pickup___success(client):
    payload = CreateMissedWastePickupDto(
        description="Test missed waste pickup",
        date="2023-10-01 12:00:00",
        address="123 Test St",
    )
    response = client.post(
        "/api/waste-management/missed_waste_pickups/", json=payload.model_dump()
    )
    assert response.status_code == 201


def test_create_missed_waste_pickup___failure_invalid_data(client):
    payload = CreateMissedWastePickupDto(
        description="",  # Invalid description
        date="2023-10-01 12:00:00",
        address="123 Test St",
    )
    response = client.post(
        "/api/waste-management/missed_waste_pickups/", json=payload.model_dump()
    )
    assert response.status_code == 400


def test_get_missed_waste_pickups___success_no_filters(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_missed_waste_pickups___success_with_search_term_filter(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups",
        params={
            "search_term": "missed waste pickup 1 -- PENDING",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["description"] == "missed waste pickup 1 -- PENDING"


def test_get_missed_waste_pickups___success_with_sorting(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups",
        params={
            "search_term": "",
            "sort_field": "date",
            "sort_order": "desc",
            "limit": 100,
            "page": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["date"] == "2023-10-02 12:00:00"


def test_update_missed_waste_pickup_status(client):
    payload = UpdateMissedWastePickupStatusDto(
        id=1,
        status=MissedWastePickupStatusEnum.REVIEWED,
    )
    response = client.post(
        "/api/waste-management/missed_waste_pickups/update_status",
        json=payload.model_dump(),
    )
    assert response.status_code == 200


def test_update_missed_waste_pickup_status___failure_not_found(client):
    payload = UpdateMissedWastePickupStatusDto(
        id=9998948393984,
        status=MissedWastePickupStatusEnum.REVIEWED,
    )
    response = client.post(
        "/api/waste-management/missed_waste_pickups/update_status",
        json=payload.model_dump(),
    )
    assert response.status_code == 404


def test_update_missed_waste_pickup_status___failure_invalid_status(client):
    payload = UpdateMissedWastePickupStatusDto(
        id=1,
        status=999,
    )
    response = client.post(
        "/api/waste-management/missed_waste_pickups/update_status",
        json=payload.model_dump(),
    )
    assert response.status_code == 400


def test_get_missed_waste_pickup_details___success(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups/1",
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert data["description"] == "missed waste pickup 1 -- PENDING"


def test_get_missed_waste_pickup_details___failure_not_found(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups/9999999",
    )
    assert response.status_code == 404


def test_get_missed_waste_pickup_details___failure_id_less_than_1(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups/0",
    )
    assert response.status_code == 400


def test_get_missed_waste_pickup_details___failure_id_invalid(client):
    response = client.get(
        "/api/waste-management/missed_waste_pickups/abc",
    )
    assert response.status_code == 422
