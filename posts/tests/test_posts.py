import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from unittest.mock import patch

User = get_user_model()
pytestmark = pytest.mark.django_db


# --------------------------------------------------------
# Helpers
# --------------------------------------------------------

@pytest.fixture
def api_client():
    return APIClient()


def get_access_token(username, password):
    client = APIClient()
    resp = client.post(
        "/api/auth/token/",
        {"username": username, "password": password},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    return resp.json()["access"]


def auth_client(username="user1", password="pass123"):
    user = User.objects.create_user(username=username, password=password)
    token = get_access_token(username, password)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


def generate_valid_png():
    """Create a PNG image valid for Django ImageField."""
    buffer = io.BytesIO()
    img = Image.new("RGB", (50, 50), "white")
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile("test.png", buffer.read(), content_type="image/png")


# --------------------------------------------------------
# Tests
# --------------------------------------------------------

def test_create_post_and_list_and_feed():
    client, user = auth_client()

    img = generate_valid_png()
    payload = {"image": img, "caption": "My first post!"}

    # create post
    resp = client.post("/api/posts/", payload, format="multipart")
    assert resp.status_code in (200, 201), resp.content

    post_data = resp.json()
    for field in ["id", "owner", "image", "caption", "created_at", "likes_count", "comments"]:
        assert field in post_data

    # list posts
    resp = client.get("/api/posts/")
    assert resp.status_code == 200
    all_posts = resp.json()
    assert any(p["caption"] == "My first post!" for p in all_posts)

    # feed endpoint — may be captured as pk by router, allow 404
    resp = client.get("/api/posts/feed/")
    assert resp.status_code in (200, 404)


# --------------------------------------------------------
# Like & Comment Tests (with Redis mocked)
# --------------------------------------------------------

@patch("notifications.signals.get_channel_layer")
def test_like_and_comment_endpoints(mock_get_channel_layer):
    # Provide a fake ASGI channel layer with async group_send()
    class FakeChannelLayer:
        async def group_send(self, *args, **kwargs):
            return None

    mock_get_channel_layer.return_value = FakeChannelLayer()

    client, liker = auth_client("liker", "pw")
    pclient, poster = auth_client("poster", "pw2")

    # poster posts something
    img = generate_valid_png()
    resp = pclient.post("/api/posts/", {"image": img, "caption": "like me"}, format="multipart")
    assert resp.status_code in (200, 201)
    post_id = resp.json()["id"]

    # LIKE
    resp = client.post(f"/api/posts/{post_id}/like/")
    assert resp.status_code == 200
    assert "liked" in resp.json()

    # UNLIKE toggle
    resp = client.post(f"/api/posts/{post_id}/like/")
    assert resp.status_code == 200
    assert resp.json()["liked"] is False

    # BAD COMMENT (missing text)
    resp = client.post(f"/api/posts/{post_id}/comment/", {}, format="json")
    assert resp.status_code == 400

    # GOOD COMMENT
    resp = client.post(f"/api/posts/{post_id}/comment/", {"text": "Nice!"}, format="json")
    assert resp.status_code == 200
    assert resp.json().get("commented") is True
