from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_register_user():

    unique = uuid.uuid4().hex[:8]

    response = client.post(
        "/Auth/register",
        json={
            "name": f"Sahil Test {unique}",
            "username": f"sahil_test_{unique}",
            "email": f"sahil_test{unique}@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code in [200, 201]


def test_register_duplicate_email():

    response = client.post(
        "/Auth/register",
        json={
            "name": "Duplicate User",
            "username": "duplicate_user",
            "email": "sahil_test@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400


def test_login_success():

    response = client.post(
        "/Auth/login",
        json={
            "username": "sahil_test",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_wrong_password():

    response = client.post(
        "/Auth/login",
        json={
            "username": "sahil_test",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_non_existing_user():

    response = client.post(
        "/Auth/login",
        json={
            "username": "not_exists",
            "password": "password123"
        }
    )

    assert response.status_code == 404


def test_register_duplicate_email():

    response = client.post(
        "/Auth/register",
        json={
            "name": "Duplicate Email",
            "username": "duplicate_email_user",
            "email": "sahil_test@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400


def test_register_blank_name():

    response = client.post(
        "/Auth/register",
        json={
            "name": "   ",
            "username": "user123",
            "email": "user123@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 422


def test_login_blank_username():

    response = client.post(
        "/Auth/login",
        json={
            "username": "   ",
            "password": "password123"
        }
    )

    assert response.status_code == 422