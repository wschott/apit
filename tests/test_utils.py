from apit.types import DiscNumber
from apit.types import TrackNumber
from apit.utils import generate_padded_track_number


def test_generate_padded_track_number():
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=5,
            disc_number=DiscNumber(1),
            disc_total=1,
        )
        == "3"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=11,
            disc_number=DiscNumber(1),
            disc_total=1,
        )
        == "03"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=5,
            disc_number=DiscNumber(1),
            disc_total=2,
        )
        == "1-3"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=5,
            disc_number=DiscNumber(2),
            disc_total=2,
        )
        == "2-3"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=11,
            disc_number=DiscNumber(2),
            disc_total=2,
        )
        == "2-03"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=5,
            disc_number=DiscNumber(2),
            disc_total=11,
        )
        == "02-3"
    )
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(3),
            track_total=11,
            disc_number=DiscNumber(2),
            disc_total=11,
        )
        == "02-03"
    )
