def generate_padded_track_number(
    track_number: int, track_total: int, disc_number: int, disc_total: int
) -> str:
    if disc_total > 1:
        return f"{padded_number(disc_number, disc_total)}-{padded_number(track_number, track_total)}"  # noqa: B950
    return padded_number(track_number, track_total)


def padded_number(number: int, total: int) -> str:
    return str(number).rjust(len(str(total)), "0")
