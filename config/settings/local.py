from config.settings.base import *  # noqa

assert DEPLOY_LEVEL == 'local'

# email backend
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = get_secrets("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secrets("EMAIL_HOST_PASSWORD")
