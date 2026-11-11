class ApitError(Exception):
    pass


class ApitNoTagsPresentError(ApitError):
    def __init__(self) -> None:
        super().__init__("No tags present")
