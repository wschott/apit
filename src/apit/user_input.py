from apit.error import ApitError


def ask_user_for_input(question: str, abortion: str) -> str:
    try:
        user_input = input(question)
    except (KeyboardInterrupt, EOFError):
        raise ApitError(abortion)
    else:
        if not user_input:
            raise ApitError(abortion)
        return user_input


def ask_user_for_confirmation(question: str = 'Apply?', abortion: str = 'Aborted.') -> None:
    user_input = ask_user_for_input(
        question=f"{question} Enter [y/n]?: ",
        abortion=abortion
    )
    if not user_input == 'y':
        raise ApitError(abortion)
