import re


def zip_code_format_validator(zip_code: str) -> bool:
    return bool(re.match(r"^\d{5}-\d{3}$", zip_code))
