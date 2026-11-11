from collections.abc import Callable

from apit.core.errors import ApitError


class ApitCliKeyboardInterruptError(ApitError):
    pass


def ask(prompt: str, abort_text: str, input_fn: Callable[[str], str] = input) -> str:
    try:
        return input_fn(prompt)
    except (KeyboardInterrupt, EOFError):
        raise ApitCliKeyboardInterruptError(abort_text)


def confirm(
    prompt: str,
    abort_text: str,
    input_fn: Callable[[str], str] = input,
) -> bool:
    user_input = ask(
        prompt=f"{prompt} Enter [y/n]?: ",
        abort_text=abort_text,
        input_fn=input_fn,
    )
    return user_input == "y"
