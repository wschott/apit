from apit.commands.tag.action import TagAction
from apit.error import ApitError
from apit.report_action import ActionReporter


class TagActionReporter(ActionReporter):
    def __init__(self, action: TagAction):
        self.action = action

    @property
    def not_actionable_msg(self) -> str:
        if not self.action.file_matched:
            return 'filename not matchable'
        elif self.action.options['is_original']:  # TODO refactor access
            return 'original iTunes Store file'
        elif not self.action.metadata_matched:
            return 'file not matched against metadata'
        raise ApitError('Unknown state')
        # TODO return '?'

    @property
    def preview_msg(self) -> str:
        if not self.action.actionable:
            return f'[{self.not_actionable_msg}]'
        return f'{self.action.song.track_number_padded} {self.action.song.title}'

    @property
    def status_msg(self) -> str:
        # TODO review conditions
        if not self.action.actionable:
            return f'[skipped: {self.not_actionable_msg}]'
        if not self.action.successful:
            return '[error]'
        if self.action.executed and self.action.successful:
            return 'tagged'
        raise ApitError('Invalid state')
