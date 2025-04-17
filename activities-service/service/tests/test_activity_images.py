import json
import pytest
from fastapi.testclient import TestClient

from tests.test_activity_creation_api import load_test_file


def test_upload_hero_image___success(client):
    hero = ("hero_image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        "/images/activity/1/hero/upload",
        files=[hero],
    )
    assert response.status_code == 201


def test_upload_hero_image___invalid_activity_id(client):
    hero = ("hero_image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        "/images/activity/9999/hero/upload",
        files=[hero],
    )
    assert response.status_code == 404


def test_upload_hero_image___missing_file(client):
    response = client.post(
        "/images/activity/1/hero/upload",
    )
    assert response.status_code == 422


def test_upload_hero_image___invalid_file_type(client):
    invalid_file = (
        "hero_image",
        ("hero.txt", load_test_file("swk_1.jpg"), "text/plain"),
    )

    response = client.post(
        "/images/activity/1/hero/upload",
        files=[invalid_file],
    )
    assert response.status_code == 422


def test_upload_activity_images___success(client):
    files = [
        ("files", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("files", ("test2.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
    ]

    response = client.post(
        "/images/activity/1/upload",
        files=files,
    )
    assert response.status_code == 201


def test_upload_activity_images___invalid_activity_id(client):
    files = [
        ("files", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("files", ("test2.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
    ]

    response = client.post(
        "/images/activity/9999/upload",
        files=files,
    )
    assert response.status_code == 404


def test_upload_activity_images___missing_files(client):
    response = client.post(
        "/images/activity/1/upload",
    )
    assert response.status_code == 422


def test_upload_activity_images___invalid_file_type(client):
    invalid_file = ("files", ("test.txt", load_test_file("swk_1.jpg"), "text/plain"))

    response = client.post(
        "/images/activity/1/upload",
        files=[invalid_file],
    )
    assert response.status_code == 422


def test_get_activity_image_ids___success(client):
    file = ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")
    response = client.post(
        "/images/activity/1/upload",
        files=[file],
    )
    assert response.status_code == 201

    response = client.get("/images/activity/1/images")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_activity_image_ids___invalid_activity_id(client):
    response = client.get("/images/activity/9999/images")
    assert response.status_code == 404


def test_get_activity_image___success(client):
    file = ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")
    response = client.post(
        "/images/activity/1/upload",
        files=[file],
    )
    assert response.status_code == 201

    activity_image_ids = client.get("/images/1/images")
    assert activity_image_ids.status_code == 200
    data = activity_image_ids.json()
    assert isinstance(data, list)
    assert len(data) == 1

    file_retrieval_response = client.get(f"/images/{data[0]}")
    assert file_retrieval_response.status_code == 200
    assert file_retrieval_response.headers["Content-Type"] == "image/jpeg"
    assert len(file_retrieval_response.content) > 0
