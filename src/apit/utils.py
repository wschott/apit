from apit.types import DiscNumber
from apit.types import TrackNumber


def generate_padded_track_number(
    track_number: TrackNumber,
    track_total: int,
    disc_number: DiscNumber,
    disc_total: int,
) -> str:
    if disc_total > 1:
        return f"{padded_number(disc_number, disc_total)}-{padded_number(track_number, track_total)}"
    return padded_number(track_number, track_total)


def padded_number(number: int, total: int) -> str:
    return str(number).rjust(len(str(total)), "0")
