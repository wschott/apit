from apit.commands.list.action import ReadAction
from apit.errors import ApitError
from tests.conftest import FakeFile


def test_read_action_after_init(make_tmp_file):
    tmp_file = make_tmp_file("1 first.m4a")

    action = ReadAction(tmp_file)

    assert action.file == tmp_file
    assert not action.executed
    assert not action.successful
    assert not action.needs_confirmation
    assert not action.result
    assert action.actionable


def test_read_action_apply(monkeypatch, make_tmp_file, test_file_tags):
    monkeypatch.setattr("apit.file_types.file_types", {"fake": FakeFile})
    action = ReadAction(make_tmp_file("1 first.fake"))

    action.apply()

    assert action.executed
    assert action.successful
    assert action.result == test_file_tags


def test_read_action_apply_error_while_reading(monkeypatch, make_tmp_file):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.file_types.file_types", {"fake": _raise})
    action = ReadAction(make_tmp_file("1 first.fake"))

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == error
