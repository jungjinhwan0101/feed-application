import pytest

from apps.account.models import User
from django.test.client import Client


@pytest.fixture(scope="function")
def authorized_client(client: Client) -> Client:
    user = User.objects.create_user(username='username', password='password', is_active=True)
    client.force_login(user)
    return client


@pytest.mark.django_db
def test_create_user_view(client: Client):
    """
    유저 생성 (회원가입) API 정상 케이스
    """
    # arrange
    payload = {
        "username": "user123",
        "password": "abcd1234defd",
        "email": "jj@gmail.com",
    }

    # act
    response = client.post("/api/users", content_type="application/json", data=payload)

    # assert
    assert response.status_code == 201

    response_json = response.json()
    user_id = response_json["id"]

    assert User.objects.filter(id=user_id).exists()


@pytest.mark.django_db
def test_login_active_user(client: Client):
    active_user = User.objects.create_user(username='username', password='password', is_active=True)

    payload = {
        "username": active_user.username,
        "password": "password",
    }

    response = client.post("/api/users/login", content_type="application/json", data=payload)

    assert response.status_code == 200
    assert 'sessionid' in response.cookies


@pytest.mark.django_db
def test_login_inactive_user(client: Client):
    inactive_user = User.objects.create_user(username='username', password='password', is_active=False)

    payload = {
        "username": inactive_user.username,
        "password": "password",
    }

    response = client.post("/api/users/login", content_type="application/json", data=payload)

    assert response.status_code == 400
    assert 'sessionid' not in response.cookies


@pytest.mark.django_db
def test_logout(authorized_client: Client):
    response = authorized_client.post("/api/users/logout")

    assert response.status_code == 200
