from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from apps.account.models import User, UserConfirmCode
from apps.account.services import AccountService


class TestAccountService(TestCase):
    def setUp(self):
        self.username = "user123"
        self.password = "abcd1234defd"
        self.email = "jj@gmail.com"

    def test_create_user(self):
        user: User = AccountService.create_user(
            username=self.username, password=self.password, email=self.email
        )

        assert UserConfirmCode.objects.filter(user=user).exists()

        assert user.is_active is False

        confirm_code = UserConfirmCode.objects.get(user=user)

        assert confirm_code.code

        assert (
            now()
            < confirm_code.expired_at
            < (now() + timedelta(minutes=AccountService.CONFIRM_CODE_EXPIRED_MINUTES))
        )
