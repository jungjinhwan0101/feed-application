from datetime import timedelta

from django.utils.timezone import now

from apps.account.models import User, UserConfirmCode
from apps.account.utils import generate_confirm_code


class AccountService:
    CONFIRM_CODE_EXPIRED_MINUTES = 10

    @classmethod
    def create_user(cls, username: str, password: str, email: str) -> User:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user

    @classmethod
    def generate_confirm_code(cls, user: User):
        confirm_code = generate_confirm_code()

        expired_at = now() + timedelta(minutes=cls.CONFIRM_CODE_EXPIRED_MINUTES)

        UserConfirmCode.objects.update_or_create(user=user, defaults={
            'confirm_code': confirm_code,
            'expired_at': expired_at
        })
