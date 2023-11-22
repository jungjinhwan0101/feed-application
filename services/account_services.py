from account.models import User


class AccountService:
    @classmethod
    def create_user(cls, username: str, password: str, email: str) -> User:
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        return user
