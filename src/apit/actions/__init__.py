from typing import List, Type

from .base import (
    Action,
    all_actions_successful,
    any_action_needs_confirmation,
    filter_errors,
    filter_not_actionable,
    filter_successes,
    find_action_type,
)
from .read import ReadAction
from .tag import TagAction

AVAILAIBLE_ACTIONS: List[Type[Action]] = [
    ReadAction,
    TagAction,
]
