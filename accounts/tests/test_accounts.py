import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


def get_token(client: APIClient, username: str, password: str):
    """
    Your JWT token obtain endpoint is:

        /api/auth/token/

    not /api/accounts/login/.
    """
    resp = client.post(
        "/api/auth/token/",
        {"username": username, "password": password},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    data = resp.json()
    return data["access"], data["refresh"]


def test_register_and_get_user_list_and_detail(api_client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "AstrongPass123",
        "password2": "AstrongPass123",
    }

    # Register
    resp = api_client.post("/api/accounts/register/", payload, format="json")
    assert resp.status_code == 201, resp.content

    # List users
    resp = api_client.get("/api/accounts/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(u["username"] == "alice" for u in data)

    # Detail
    alice = User.objects.get(username="alice")
    resp = api_client.get(f"/api/accounts/{alice.id}/")
    assert resp.status_code == 200
    d = resp.json()

    for field in [
        "id",
        "username",
        "email",
        "bio",
        "avatar",
        "followers_count",
        "following_count",
    ]:
        assert field in d


def test_login_and_jwt_token_flow(api_client):
    User.objects.create_user(username="bob", password="pass123")

    access, refresh = get_token(api_client, "bob", "pass123")
    assert access
    assert refresh

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    resp = api_client.get("/api/accounts/")
    assert resp.status_code == 200


def test_follow_toggle_requires_authentication(api_client):
    u1 = User.objects.create_user(username="u1", password="p1")
    u2 = User.objects.create_user(username="u2", password="p2")

    # unauthenticated → reject
    resp = api_client.post(f"/api/accounts/{u2.id}/follow-toggle/")
    assert resp.status_code in (401, 403)

    # authenticated
    access, _ = get_token(api_client, "u1", "p1")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    resp = api_client.post(f"/api/accounts/{u2.id}/follow-toggle/")
    assert resp.status_code == 200
    assert "followed" in resp.json()
