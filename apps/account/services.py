from datetime import timedelta

from django.db import transaction
from django.utils.timezone import now

from apps.account.models import User, UserConfirmCode
from apps.account.utils import generate_confirm_code


class AccountService:
    CONFIRM_CODE_EXPIRED_MINUTES = 10

    @classmethod
    @transaction.atomic
    def signup(cls, username: str, password: str, email: str) -> User:
        user = User.objects.create_user(
            username=username, email=email, password=password, is_active=False
        )

        cls._set_confirm_code(user)

        cls._send_email_confirm_code(user)

        return user

    @classmethod
    def _set_confirm_code(cls, user: User):
        confirm_code = generate_confirm_code()

        expired_at = now() + timedelta(minutes=cls.CONFIRM_CODE_EXPIRED_MINUTES)

        UserConfirmCode.objects.update_or_create(
            user=user, defaults={"code": confirm_code, "expired_at": expired_at}
        )

    @classmethod
    def _send_email_confirm_code(cls, user: User):
        print(f"Email 발송 : {user.confirm_code.code}")
