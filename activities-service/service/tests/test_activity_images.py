import json
import os
import pytest
from fastapi.testclient import TestClient

from tests.conftest import BASE_TEST_URL


def load_test_file(filename):
    filepath = os.path.join("tests", "test_upload_files", filename)
    return open(filepath, "rb")


def test_upload_hero_image___success(client):
    hero = ("image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/hero/upload",
        files=[hero],
    )
    assert response.status_code == 201


def test_upload_hero_image___invalid_activity_id(client):
    hero = ("image", ("hero.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/9999/hero/upload",
        files=[hero],
    )
    assert response.status_code == 404


def test_upload_hero_image___missing_file(client):
    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/hero/upload",
    )
    assert response.status_code == 422


def test_upload_hero_image___invalid_file_type(client):
    invalid_file = (
        "image",
        ("hero.txt", load_test_file("swk_1.jpg"), "text/plain"),
    )

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/hero/upload",
        files=[invalid_file],
    )
    assert response.status_code == 422


def test_upload_activity_images___success(client):
    files = [
        ("images", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("images", ("test2.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
    ]

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
        files=files,
    )
    assert response.status_code == 201


def test_upload_activity_images___invalid_activity_id(client):
    files = [
        ("images", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
        ("images", ("test2.jpg", load_test_file("swk_1.jpg"), "image/jpeg")),
    ]

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/9999/upload",
        files=files,
    )
    assert response.status_code == 404


def test_upload_activity_images___missing_files(client):
    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
    )
    assert response.status_code == 422


def test_upload_activity_images___invalid_file_type(client):
    invalid_file = ("images", ("test.txt", load_test_file("swk_1.jpg"), "text/plain"))

    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
        files=[invalid_file],
    )
    assert response.status_code == 422


def test_get_activity_image_ids___success(client):
    file = ("images", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))
    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
        files=[file],
    )
    assert response.status_code == 201

    response = client.get(f"{BASE_TEST_URL}/images/activity/1")
    assert response.status_code == 200
    data = response.json()
    image_ids = data.get("image_ids", [])
    assert isinstance(image_ids, list)
    assert len(image_ids) == 3


def test_get_activity_image_ids___invalid_activity_id(client):
    response = client.get(f"{BASE_TEST_URL}/images/activity/9999")
    assert response.status_code == 404


def test_get_activity_image___success(client):
    file = ("images", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))
    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
        files=[file],
    )
    assert response.status_code == 201

    activity_image_ids = client.get(f"{BASE_TEST_URL}/images/activity/1")
    assert activity_image_ids.status_code == 200
    data = activity_image_ids.json()
    image_ids = data.get("image_ids", [])
    assert isinstance(image_ids, list)
    assert len(image_ids) == 3

    file_retrieval_response = client.get(f"{BASE_TEST_URL}/images/{image_ids[2]}")
    assert file_retrieval_response.status_code == 200
    assert file_retrieval_response.headers["Content-Type"] == "image/jpeg"
    assert len(file_retrieval_response.content) > 0


def test_delete_activity_image___success(client):
    file = ("images", ("test1.jpg", load_test_file("swk_1.jpg"), "image/jpeg"))
    response = client.post(
        f"{BASE_TEST_URL}/images/activity/1/upload",
        files=[file],
    )
    assert response.status_code == 201

    activity_image_ids = client.get(f"{BASE_TEST_URL}/images/activity/1")
    assert activity_image_ids.status_code == 200
    data = activity_image_ids.json()
    image_ids = data.get("image_ids", [])
    assert isinstance(image_ids, list)
    assert len(image_ids) == 3

    delete_response = client.delete(f"{BASE_TEST_URL}/images/{image_ids[2]}")
    assert delete_response.status_code == 200


def test_delete_activity_image___invalid_image_id(client):
    response = client.delete(f"{BASE_TEST_URL}/images/9999")
    assert response.status_code == 404
