import re
import unicodedata
from typing import Final

ELLIPSIS: Final = "…"


def truncate_text(text: str, length: int) -> str:
    if len(text) <= length:
        return text
    return text[: (length - len(ELLIPSIS))] + ELLIPSIS


def normalize_unicode(string: str) -> str:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return unicodedata.normalize("NFC", string)


def compare_normalized_caseless(string1: str, string2: str) -> bool:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return normalize_unicode(
        normalize_unicode(string1).casefold()
    ) == normalize_unicode(normalize_unicode(string2).casefold())


def pad_with_spaces(string: str, length: int) -> str:
    return string.ljust(length, " ")


def clean(uncleaned_str: str) -> str:
    return re.sub(r"[\W_]+", "", uncleaned_str)
