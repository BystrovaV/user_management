import uuid

import pytest
from pydantic import ValidationError


def test_signup(client):
    request_body = {
        "name": "test1",
        "surname": "test1",
        "phone_number": "+375 44 111-11-11",
        "email": "test1@test.com",
        "role": "admin",
        "group": "b27d2f28-6475-4d52-8165-70e64bb3f90a",
        "password": "1234567",
        "repeat_password": "1234567",
    }

    response = client.post("/auth/signup", json=request_body)
    assert response.status_code == 422

    request_body["username"] = "test1"
    response = client.post("/auth/signup", json=request_body)
    assert response.status_code == 200


def test_login(client):
    request_body = {"user_data": "test1@example.com", "password": "1234567"}

    response = client.post("/auth/login", json=request_body)
    assert response.status_code == 200
    assert response.json().get("access_token") is not None
    assert response.json().get("token_type") is not None


def test_refresh_token(client):
    request_body = {"token": str(uuid.uuid4())}

    response = client.post("/auth/refresh-token", json=request_body)
    assert response.status_code == 401

    headers = {"Authorization": "Bearer"}

    response = client.post("/auth/refresh-token", json=request_body, headers=headers)
    assert response.status_code == 200
    assert response.json().get("access_token") is not None
    assert response.json().get("token_type") is not None
    assert response.json().get("token_type") == "bearer"


def test_reset_password(client):
    request_body = {"email": "test1@test.com"}

    response = client.post("/auth/reset-password", json=request_body)
    assert response.status_code == 200


def test_get_me(client):
    response = client.get("/user/me")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    response = client.get("/user/me", headers=headers)
    assert response.status_code == 200


def test_patch_me(client):
    response = client.patch("user/me")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    response = client.patch("user/me", headers=headers)
    assert response.status_code == 422

    request_body = {
        "id": str(uuid.uuid4()),
        "name": "test1",
        "surname": "test1",
        "username": "test1",
        "phone_number": "+375 44 111-11-11",
        "email": "test1@test.com",
    }

    response = client.patch("user/me", headers=headers, json=request_body)
    assert response.status_code == 200


def test_delete_user(client):
    response = client.delete("user/me")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    response = client.delete("user/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == 1


def test_get_user(client):
    user_id = str(uuid.uuid4())
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    response = client.get(f"/user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == user_id


def test_patch_user(client):
    user_id = str(uuid.uuid4())
    response = client.patch(f"user/{user_id}")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    response = client.patch(f"user/{user_id}", headers=headers)
    assert response.status_code == 422

    request_body = {
        "id": user_id,
        "name": "test1",
        "surname": "test1",
        "username": "test1",
        "phone_number": "+375 44 111-11-11",
        "email": "test1@test.com",
    }

    response = client.patch(f"user/{user_id}", headers=headers, json=request_body)
    assert response.status_code == 200
    assert response.json() == user_id


def test_get_users(client):
    response = client.get("users")
    assert response.status_code == 401

    headers = {"Authorization": "Bearer " + str(uuid.uuid4())}

    params = {"order_by": "desci"}

    with pytest.raises(ValidationError):
        response = client.get("users", params=params, headers=headers)

    params = {
        "sort_by": "group",
    }

    response = client.get("users", params=params, headers=headers)
    assert response.status_code == 422

    response = client.get("users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
