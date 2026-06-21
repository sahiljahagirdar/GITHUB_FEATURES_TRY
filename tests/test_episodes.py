from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_api_key():
    """
    Login -> Generate API Key -> Return API Key
    """

    login_response = client.post(
        "/Auth/login",
        json={
            "username": "sahil_test",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["token"]

    api_key_response = client.post(
        "/Auth/get_api_key",
        headers={
            "authorization": token
        }
    )

    assert api_key_response.status_code == 200

    return api_key_response.json()["api_key"]


def test_get_episode_success():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/episode/1",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200


def test_get_episode_not_found():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/episode/999999",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 404


def test_status_endpoint():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/status",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200

    data = response.json()

    assert "episodes_in_db" in data
    assert "highest_episode_number" in data
    assert "missing_episodes" in data


def test_random_episode():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/random",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200


def test_latest_episode():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/latest_episode",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200


def test_search_success():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/search?keyword=Daya",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200

    data = response.json()

    assert "page" in data
    assert "limit" in data
    assert "total_records" in data
    assert "total_pages" in data
    assert "has_next" in data
    assert "has_previous" in data


def test_search_no_results():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/search?keyword=abcdefghxyz123",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 404


def test_search_invalid_page():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/search?keyword=Daya&page=0",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 422


def test_search_invalid_limit():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/search?keyword=Daya&limit=101",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 422


def test_search_page_beyond_limit():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/search?keyword=Daya&page=9999",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 404


def test_all_episodes():
    api_key = get_api_key()

    response = client.get(
        "/TMKOC/episodes?page=1&limit=5",
        headers={"X-API-KEY": api_key}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0