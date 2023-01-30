from apit.color import Color
from apit.color import to_colored_text


def to_summary_line(successes: int, errors: int, skipped: int) -> str:
    summary = []
    if successes:
        summary.append(to_colored_text(f"{successes} processed", Color.GREEN))
    if errors:
        summary.append(to_colored_text(f"{errors} failed", Color.RED))
    if skipped:
        summary.append(to_colored_text(f"{skipped} skipped", Color.YELLOW))

    bar_color = Color.GREEN
    if errors:
        bar_color = Color.RED
    elif skipped:
        bar_color = Color.YELLOW

    return " ".join(
        [
            to_colored_text("=" * 30, bar_color),
            ", ".join(summary),
            to_colored_text("=" * 30, bar_color),
        ]
    )
