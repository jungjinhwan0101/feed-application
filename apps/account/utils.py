import random
import string


def generate_confirm_code():
    length = 6
    alphanumeric = string.ascii_letters + string.digits
    confirm_code = "".join([random.choice(alphanumeric) for _ in range(length)])
    return confirm_code
