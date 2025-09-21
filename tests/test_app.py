from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app

import pytest


@pytest.fixture()
def client():
    return TestClient(app)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, World!"}


def test_create_user(client):
    user_data = {
        "username": "John Doe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    client.post("/users/", json=user_data)

    response = client.post("/users/", json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 2,
        "username": "John Doe",
        "email": "john.doe@example.com",
    }


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json().get("users", [])) >= 0


def test_update_user(client):
    user_data = {
        "username": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "newpassword123",
    }

    client.post(
        "/users/", json=user_data
    )  # Create a user to update just to make the test independent

    response = client.put("/users/1", json=user_data)
    assert response.status_code == HTTPStatus.OK
    assert "id" in response.json()


def test_delete_user(client):
    user_data = {
        "username": "Mark Smith",
        "email": "mark.smith@example.com",
        "password": "password123",
    }

    client.post(
        "/users/", json=user_data
    )  # Create a user to delete just to make the test independent

    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted successfully"}
