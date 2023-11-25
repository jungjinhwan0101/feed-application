from django.core.mail import send_mail as django_send_email

from django.conf import settings


def send_email(*, subject: str, message: str, recipient_email: str):
    django_send_email(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email]
    )
