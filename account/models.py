from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(fields=['email'], name='email_unique'),
        ]
