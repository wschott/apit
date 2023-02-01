import re
import unicodedata


def normalize_unicode(string: str) -> str:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return unicodedata.normalize("NFC", string)


def compare_normalized_caseless(string1: str, string2: str) -> bool:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return normalize_unicode(
        normalize_unicode(string1).casefold()
    ) == normalize_unicode(normalize_unicode(string2).casefold())


def clean(uncleaned_str: str) -> str:
    return re.sub(r"[\W_]+", "", uncleaned_str)
