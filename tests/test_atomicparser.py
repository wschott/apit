# -*- coding: utf-8 -*-

import os
from collections import namedtuple
from unittest import TestCase, skipIf
from StringIO import StringIO

from mock import patch

from apit.AtomicParser import (get_atomicparsley, construct_update_command,
    _construct_command, _exec_command, get_info, escape, update_metadata,
    add_extra_data_to_command) # get_atomicparsley_version


ALBUM = {
    'artistName': 'Album Artist',
    'copyright': u'℗ 2010 Album Copyright'
}


SONG = {
    'artistName': 'Main Artist',
    'trackCensoredName': u'Track (feat. Other & $Artist) [Bonus Track]',
    'collectionName': 'Album Name',
    'primaryGenreName': 'Genre Name',
    'releaseDate': '2010-01-30',
    'discNumber': 1,
    'discCount': 2,
    'trackNumber': 3,
    'trackCount': 4,
    'trackExplicitness': 'explicit',
    'kind': 'song',
    # 'trackId': 12345,
}


EXPECTED = ' '.join(
    [
        'AtomicParsley "dummy.m4a" --artist "Main Artist"',
        '--title "Track (feat. Other & \\$Artist) [Bonus Track]"',
        '--album "Album Name" --genre "Genre Name"',
        '--year "2010-01-30" --disknum 1/2 --tracknum 3/4',
        '--advisory explicit --stik "Normal"',
        '--albumArtist "Album Artist"',
        '--copyright "\xe2\x84\x97 2010 Album Copyright"'
    ]
)

@patch('apit.AtomicParser.get_atomicparsley', new=lambda: '/Mock/AtomicParsley')
class TestAtomicParser(TestCase):
    def get_test_data(self):
        with open('tests/metadata.js', 'r') as f:
            data = f.read()
        return data

    @skipIf(os.environ.get('TRAVIS') == '1', 'skip on Travis CI')
    def test_atomicparsley_finding(self):
        self.assertIn('AtomicParsley', get_atomicparsley())

    # def test_new_atomicparsley_version(self):
    #     print get_atomicparsley_version(get_atomicparsley())
    #     assert False

    def test_arg_escaping(self):
        self.assertEqual('foo\\"bar', escape('foo"bar'))

    def test_command_constructing_unicode(self):
        self.assertIn('AtomicParsley "dummy.m4a" --artist "Kanye, Beyonc\xc3\xa9 & Big"',
                      _construct_command('dummy.m4a', [u'--artist "Kanye, Beyoncé & Big"']))

    def test_command_constructing_escaping(self):
        self.assertIn('AtomicParsley "dummy.m4a" a --b "foo \\$bar"',
                      _construct_command('dummy.m4a', ['a', '--b "foo $bar"']))

    def test_metadata_command_constructing_no_overwrite(self):
        cmd_to_test = _construct_command(
            'dummy.m4a',
            construct_update_command(SONG, ALBUM, extra_data={}, overwrite=False, old_version=False)
        )
        self.assertIn(EXPECTED, cmd_to_test)

    def test_metadata_command_constructing_with_overwrite(self):
        cmd_to_test = _construct_command(
            'dummy.m4a',
            construct_update_command(SONG, ALBUM, extra_data={}, overwrite=True, old_version=False)
        )
        self.assertIn(EXPECTED + ' --overWrite', cmd_to_test)

    def test_metadata_command_constructing_account(self):
        extra_data = {'account': 'first@last.com'}

        cmd_to_test = add_extra_data_to_command(extra_data, old_version=False)
        self.assertEqual(['--apID "first@last.com"'], cmd_to_test)

    def test_metadata_command_constructing_no_purchase_date(self):
        for test_date in ['', 'n']:
            cmd_to_test = add_extra_data_to_command(extra_data={'purchaseDate': test_date}, old_version=False)
            self.assertEqual([], cmd_to_test)

    def test_metadata_command_constructing_bad_purchase_date_format(self):
        for extra_data in [{'purchaseDate': 'foobar'}, {'purchaseDate': '01-01-2010'}]:
            cmd_to_test = add_extra_data_to_command(extra_data, old_version=False)
            self.assertEqual([], cmd_to_test)

    def test_metadata_command_constructing_purchase_date(self):
        extra_data = {'purchaseDate': 'y'}

        cmd_to_test = add_extra_data_to_command(extra_data, old_version=False)
        self.assertEqual(['--purchaseDate "timestamp"'], cmd_to_test)

        for test_date in ['2010-01-01', '2010-01-01_00-00-00']:
            cmd_to_test = add_extra_data_to_command(extra_data={'purchaseDate': test_date}, old_version=False)
            self.assertEqual(['--purchaseDate "2010-01-01 00:00:00"'], cmd_to_test)

    @patch('os.popen', new=lambda x: StringIO(x))
    def test_command_execution(self):
        self.assertIn('AtomicParsley "dummy.m4a" --my-test test',
                      _exec_command('dummy.m4a', '--my-test test'))

    @patch('os.popen', new=lambda x: StringIO(x))
    def test_metadata_reading(self):
        self.assertIn('AtomicParsley "dummy.m4a" -t',
                      get_info('dummy.m4a'))

    @patch('os.popen', new=lambda x: StringIO(x))
    def test_metadata_updating(self):
        cmd_to_test = update_metadata('dummy.m4a', SONG, ALBUM, extra_data={}, overwrite=False, old_version=False)
        self.assertIn(EXPECTED, cmd_to_test)
