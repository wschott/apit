from pathlib import Path

from apit.commands.tag.action import TagAction
from apit.commands.tag.reporter import TagActionReporter
from apit.metadata import Song


def test_not_actionable_msg_not_file_matched():
    action = TagAction(Path('dummy.m4a'), {
        'song': None,
        'disc': None,
        'track': None,
        'is_original': False,
    })

    reporter = TagActionReporter(action)

    assert reporter.not_actionable_msg == 'filename not matchable'


def test_not_actionable_msg_file_original():
    action = TagAction(Path('dummy.m4a'), {
        'song': None,
        'disc': 1,
        'track': 1,
        'is_original': True,
    })

    reporter = TagActionReporter(action)

    assert reporter.not_actionable_msg == 'original iTunes Store file'


def test_not_actionable_msg_not_metadata_matched():
    action = TagAction(Path('dummy.m4a'), {
        'song': None,
        'disc': 1,
        'track': 1,
        'is_original': False,
    })

    reporter = TagActionReporter(action)

    assert reporter.not_actionable_msg == 'file not matched against metadata'


def test_preview_msg_not_actionable():
    action = TagAction(Path('dummy.m4a'), {
        'song': None,
        'disc': None,
        'track': None,
        'is_original': False,
    })

    reporter = TagActionReporter(action)

    assert reporter.preview_msg == '[filename not matchable]'


def test_preview_msg_actionable(test_song: Song):
    action = TagAction(Path('dummy.m4a'), {
        'song': test_song,
        'disc': test_song.disc_number,
        'track': test_song.track_number,
        'is_original': False,
    })

    reporter = TagActionReporter(action)

    assert reporter.preview_msg == '2-3 Track (feat. Other & $Artist) [Bonus Track]'


def test_status_msg_successful(test_song: Song):
    action = TagAction(Path('dummy.m4a'), {
        'song': test_song,
        'disc': test_song.disc_number,
        'track': test_song.track_number,
        'is_original': False,
    })
    action.mark_as_success('test-success')

    reporter = TagActionReporter(action)

    assert reporter.status_msg == 'tagged'


def test_status_msg_tag_not_successful(test_song: Song):
    action = TagAction(Path('dummy.m4a'), {
        'song': test_song,
        'disc': test_song.disc_number,
        'track': test_song.track_number,
        'is_original': False,
    })
    action.mark_as_fail('test-error')

    reporter = TagActionReporter(action)

    assert reporter.status_msg == '[error]'


def test_status_msg_tag_not_actionable():
    action = TagAction(Path('dummy.m4a'), {
        'song': None,
        'disc': None,
        'track': None,
        'is_original': False,
    })

    reporter = TagActionReporter(action)

    assert reporter.status_msg.startswith('[skipped')
    assert reporter.status_msg.endswith(']')
