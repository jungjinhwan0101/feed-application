from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(fields=["email"], name="email_unique"),
        ]

    def active(self):
        self.is_active = True
        self.save()


class UserConfirmCode(models.Model):
    user = models.OneToOneField(
        "account.User", related_name="confirm_code", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=6, help_text="가입 승인 코드")
    expired_at = models.DateTimeField()

    @property
    def is_expired(self):
        return self.expired_at < now()
