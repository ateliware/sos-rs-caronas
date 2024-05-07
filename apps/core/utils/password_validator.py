import re


def validate_password(password: str) -> bool:
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^\dA-Za-z ]).{6,}$"
    regex = re.compile(pattern)
    if regex.match(password):
        return True
    else:
        return False
