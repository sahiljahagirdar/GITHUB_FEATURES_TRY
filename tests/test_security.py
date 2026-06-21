from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_no_api_key():

    response = client.get(
        "/TMKOC/status"
    )

    assert response.status_code == 401


def test_invalid_api_key():

    response = client.get(
        "/TMKOC/status",
        headers={
            "X-API-KEY": "invalid_key"
        }
    )

    assert response.status_code == 401


def test_search_without_api_key():

    response = client.get(
        "/TMKOC/search?keyword=Daya"
    )

    assert response.status_code == 401


def test_search_invalid_api_key():

    response = client.get(
        "/TMKOC/search?keyword=Daya",
        headers={
            "X-API-KEY": "wrong_key"
        }
    )

    assert response.status_code == 401