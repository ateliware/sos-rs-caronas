import re


def get_only_numbers(text: str) -> str:
    return re.sub("[^0-9]", "", text)
