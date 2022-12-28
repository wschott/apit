import unicodedata


def normalize_unicode(string: str) -> str:
    # docs: https://docs.python.org/3/howto/unicode.html#comparing-strings
    return unicodedata.normalize("NFC", string)
