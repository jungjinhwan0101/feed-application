from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(fields=["email"], name="email_unique"),
        ]


class UserConfirmCode(models.Model):
    user = models.OneToOneField(
        "account.User", related_name="confirm_code", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=6, help_text="가입 승인 코드")
    expired_at = models.DateTimeField()
