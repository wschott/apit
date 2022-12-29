import unicodedata

ELLIPSIS = "…"


def truncate_text(text: str, length: int) -> str:
    if len(text) <= length:
        return text
    return text[: (length - len(ELLIPSIS))] + ELLIPSIS


def normalize_unicode(string: str) -> str:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return unicodedata.normalize("NFC", string)
