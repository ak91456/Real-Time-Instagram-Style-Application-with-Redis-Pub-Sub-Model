import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from notifications.models import Notification

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


def test_ping_view(api_client):
    """Your only HTTP endpoint."""
    resp = api_client.get("/api/notifications/ping/")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_notification_model_creation():
    """Signals create notifications, but we test model directly."""
    u1 = User.objects.create_user(username="alice", password="pass")
    u2 = User.objects.create_user(username="bob", password="pass")

    n = Notification.objects.create(
        recipient=u1,
        actor=u2,
        verb="liked",
        target_post_id=10,
    )

    assert n.recipient == u1
    assert n.actor == u2
    assert not n.read
    assert n.target_post_id == 10


def test_notification_mark_read_update():
    u1 = User.objects.create_user(username="alice", password="pass")
    u2 = User.objects.create_user(username="bob", password="pass")

    n = Notification.objects.create(
        recipient=u1,
        actor=u2,
        verb="commented",
        target_post_id=5,
    )

    assert n.read is False
    n.read = True
    n.save()

    n.refresh_from_db()
    assert n.read is True
