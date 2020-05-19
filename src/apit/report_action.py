class ActionReporter:
    @property
    def not_actionable_msg(self) -> str:
        raise NotImplementedError

    @property
    def preview_msg(self) -> str:
        raise NotImplementedError

    @property
    def status_msg(self) -> str:
        raise NotImplementedError
