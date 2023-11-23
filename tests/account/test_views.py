import pytest

from apps.account.models import User


@pytest.mark.django_db
def test_create_user_view(client):
    """
    유저 생성 (회원가입) API 정상 케이스
    """
    # arrange
    payload = {"username": "user123", "password": "abcd1234defd", "email": "jj@gmail.com"}

    # act
    response = client.post('/api/users', content_type='application/json', data=payload)

    # assert
    assert response.status_code == 201

    response_json = response.json()
    user_id = response_json['id']

    assert User.objects.filter(id=user_id).exists()
