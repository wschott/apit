from apit.string_utils import clean
from apit.string_utils import compare_normalized_caseless
from apit.string_utils import normalize_unicode

ACCENT_AS_DOUBLE_CHAR = "xúx"
ACCENT_AS_SINGLE_CHAR = "xúx"


def test_strings_looking_similar_but_having_different_chars_are_equal_once_normalized():
    normalized_double_char = normalize_unicode(ACCENT_AS_DOUBLE_CHAR)
    normalized_single_char = normalize_unicode(ACCENT_AS_SINGLE_CHAR)

    assert ACCENT_AS_DOUBLE_CHAR != ACCENT_AS_SINGLE_CHAR
    assert len(ACCENT_AS_DOUBLE_CHAR) != len(ACCENT_AS_SINGLE_CHAR)
    assert normalized_double_char == normalized_single_char
    assert len(normalized_double_char) == len(normalized_single_char)


def test_not_normalized_strings_are_comparable_with_normalization():
    assert compare_normalized_caseless(ACCENT_AS_DOUBLE_CHAR, ACCENT_AS_SINGLE_CHAR)


def test_clean():
    assert clean("-t. é\\ s/ t_") == "tést"
