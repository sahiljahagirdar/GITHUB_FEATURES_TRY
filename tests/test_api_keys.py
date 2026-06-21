from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():

    response = client.post(
        "/Auth/login",
        json={
            "username": "sahil_test",
            "password": "password123"
        }
    )

    return response.json()["token"]


def test_generate_api_key():

    token = get_token()

    response = client.post(
        "/Auth/get_api_key",
        headers={
            "authorization": token
        }
    )

    assert response.status_code == 200
    assert "api_key" in response.json()


def test_generate_api_key_without_jwt():

    response = client.post(
        "/Auth/get_api_key"
    )

    assert response.status_code == 401


def test_get_my_api_keys():

    token = get_token()

    response = client.get(
        "/Auth/my_api_keys",
        headers={
            "authorization": token
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)