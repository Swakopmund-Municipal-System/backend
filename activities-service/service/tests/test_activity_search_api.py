import json
import pytest
from fastapi.testclient import TestClient

from app.models.enums.enums import ActivityType


def test_get_activities___success_no_filters(client):
    response = client.get(
        "/activities/search",
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


def test_get_activities___success_with_search_term_filter(client):
    response = client.get(
        "/activities/search",
        params={
            "search_term": "Description for Festival 1",
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
    assert data[0]["description"] == "Description for Festival 1"


def test_get_activities___success_with_sorting(client):
    response = client.get(
        "/activities/search",
        params={
            "search_term": "",
            "sort_field": "created_at",
            "sort_order": "desc",
            "limit": 100,
            "page": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 2


def test_get_activities___success_category_festival(client):
    response = client.get(
        "/activities/search",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "categories": f"{ActivityType.FESTIVAL}",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["type"] == ActivityType.FESTIVAL.value


def test_get_activities___success_category_recreational_and_festival(client):
    response = client.get(
        "/activities/search",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "categories": f"{ActivityType.FESTIVAL},{ActivityType.RECREATIONAL}",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert (
        data[0]["type"] == ActivityType.FESTIVAL.value
        or data[0]["type"] == ActivityType.RECREATIONAL.value
    )


def test_get_activities___success_no_item_with_category(client):
    response = client.get(
        "/activities/search",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "categories": f"99999",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_activities_by_location___success(client):
    response = client.get(
        "/activities/search/location",
        params={
            "latitude": -22.592063343286743,
            "longitude": 17.080047073592386,
            "radius": 1000,
            "search_term": "",
            "categories": None,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_activities_by_location___success_with_search_term(client):
    response = client.get(
        "/activities/search/location",
        params={
            "latitude": -22.592063343286743,
            "longitude": 17.080047073592386,
            "radius": 1000,
            "search_term": "Festival 1",
            "categories": None,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_activities_by_location___success_with_category(client):
    response = client.get(
        "/activities/search/location",
        params={
            "latitude": -22.592063343286743,
            "longitude": 17.080047073592386,
            "radius": 1000,
            "search_term": "",
            "categories": f"{ActivityType.FESTIVAL}",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["type"] == ActivityType.FESTIVAL.value


def test_get_activities_by_location___success_larger_radius(client):
    response = client.get(
        "/activities/search/location",
        params={
            "latitude": -22.592063343286743,
            "longitude": 17.080047073592386,
            "radius": 10000,
            "search_term": "",
            "categories": None,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_activities_by_location___success_no_items(client):
    response = client.get(
        "/activities/search/location",
        params={
            "latitude": -21.592063343286743,
            "longitude": 17.080047073592386,
            "radius": 1000,
            "search_term": "",
            "categories": None,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_actitity_by_id___success(client):
    response = client.get("/activities/1")
    assert response.status_code == 200
    raw_data = response.json()
    data = json.loads(raw_data)

    assert data["id"] == 1
    assert data["name"] == "Festival 1"


def test_get_activity_by_id___not_found(client):
    response = client.get("/activities/9999")
    assert response.status_code == 404


def test_get_activity_by_id___invalid_id(client):
    response = client.get("/activities/invalid_id")
    assert response.status_code == 422
