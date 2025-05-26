import json
import pytest
from fastapi.testclient import TestClient

from app.models.dto.models import CreateReviewDTO
from tests.conftest import BASE_TEST_URL


def test_get_reviews___success_no_filters(client):
    response = client.get(
        f"{BASE_TEST_URL}/reviews/",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "activity_id": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_reviews___success_no_reviews(client):
    response = client.get(
        f"{BASE_TEST_URL}/reviews/",
        params={
            "search_term": "",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "activity_id": 4,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_reviews___success_with_search_term_filter(client):
    response = client.get(
        f"{BASE_TEST_URL}/reviews/",
        params={
            "search_term": "Great festival!",
            "sort_field": "",
            "sort_order": "",
            "limit": 100,
            "page": 1,
            "activity_id": 1,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["review_text"] == "Great festival!"


def test_create_review___success(client):
    payload = CreateReviewDTO(
        activity_id=1,
        review="This is a test review",
        rating=5,
    )
    response = client.post(f"{BASE_TEST_URL}/reviews/", json=payload.model_dump())
    assert response.status_code == 201


def test_create_review___failure_empty_review(client):
    payload = CreateReviewDTO(
        activity_id=1,
        review="abcd",
        rating=2,
    )
    payload.review = ""
    response = client.post(f"{BASE_TEST_URL}/reviews/", json=payload.model_dump())
    assert response.status_code == 422


def test_create_review___failure_invalid_rating(client):
    payload = CreateReviewDTO(
        activity_id=1,
        review="This is a test review",
        rating=5,
    )
    payload.rating = 6
    response = client.post(f"{BASE_TEST_URL}/reviews/", json=payload.model_dump())
    assert response.status_code == 422


def test_create_review___failure_missing_fields(client):
    payload = CreateReviewDTO(
        activity_id=1,
        review="This is a test review",
        rating=5,
    )
    payload.review = None
    response = client.post(f"{BASE_TEST_URL}/reviews/", json=payload.model_dump())
    assert response.status_code == 422


def test_create_review___failure_invalid_activity_id(client):
    payload = CreateReviewDTO(
        activity_id=9999,
        review="This is a test review",
        rating=5,
    )
    response = client.post(f"{BASE_TEST_URL}/reviews/", json=payload.model_dump())
    assert response.status_code == 404


def test_delete_review___success(client):
    response = client.delete(f"{BASE_TEST_URL}/reviews/1")
    assert response.status_code == 200


def test_delete_review___failure_not_found(client):
    response = client.delete(f"{BASE_TEST_URL}/reviews/9999")
    assert response.status_code == 404


def test_delete_review___failure_invalid_id(client):
    response = client.delete(f"{BASE_TEST_URL}/reviews/invalid_id")
    assert response.status_code == 422
