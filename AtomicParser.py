# -*- coding: utf-8 -*-

# --composer, --grouping, --bpm, --compilation, --encodingTool, --gapless

import os
import datetime
import logging

class AtomicParser:
    # should the file be overwritten or create a duplicate
    DEFAULT_AP_FILES = ['/Applications/AtomicParsley',
                        '~/Applications/AtomicParsley',
                        '~/bin/AtomicParsley']
    rating_map = {
        'cleaned': 'clean',
        'explicit': 'explicit',
        'notExplicit': 'remove',
    }
    kind_map = {
        'song': 'Normal',
    }
    genre_map = {
        'Hip Hop/Rap': 18,
        'Hip-Hop/Rap': 18,
        'Dance': 17,
    }
    store_map = {
        'USA': 'United States (143441)',
        'DEU': 'Germany (143443)',
    }

    def __init__(self, ap_file='', overwrite_files=False, new_executable_version=True):
        self.over_write = overwrite_files
        self.new_ap_executable = new_executable_version
        self.atomic_parsley_file = 'AtomicParsley'
        # find AtomicParsley
        for f in [ap_file] + AtomicParser.DEFAULT_AP_FILES:
            if os.path.isfile(f):
                self.atomic_parsley_file = f
                logging.debug("'%s' found" % f)
            else:
                logging.debug("'%s' not found" % f)

        if not self.atomic_parsley_file:
            raise Exception('AtomicParsley executable not found')

    def escape(self, string):
        return string.replace('"', '\\"').encode('utf-8')

    def update_metadata(self, filename, track, album, extra_data=None):
        cmd = []

        cmd.append('--artist "%s"'      % self.escape(track['artistName']))
        cmd.append('--title "%s"'       % self.escape(track['trackCensoredName'])) # trackName
        cmd.append('--album "%s"'       % self.escape(track['collectionName']))
        cmd.append('--genre "%s"'       % self.escape(track['primaryGenreName']))
        cmd.append('--year "%s"'        % self.escape(track['releaseDate']))
        cmd.append('--disknum %s/%s'    % (track['discNumber'], track['discCount']))
        cmd.append('--tracknum %s/%s'   % (track['trackNumber'], track['trackCount']))
        cmd.append('--advisory %s'      % self.rating_map[track['trackExplicitness']])
        cmd.append('--stik "%s"'        % self.kind_map[track['kind']])
        cmd.append('--albumArtist "%s"' % self.escape(album['artistName']))
        copyright = u'--copyright "℗ %s"' % self.escape(album['copyright'])
        cmd.append(copyright.encode('utf-8'))

        if 'purchaseDate' in extra_data:
            if extra_data['purchaseDate'] == 'y':
                cmd.append('--purchaseDate "timestamp"')
            elif extra_data['purchaseDate'] != '' and extra_data['purchaseDate'] != 'n':
                for format in ['%Y-%m-%d', '%Y-%m-%d_%H', '%Y-%m-%d_%H-%M', '%Y-%m-%d_%H-%M-%S']:
                    try:
                        date = datetime.datetime.strptime(extra_data['purchaseDate'], format).strftime('%Y-%m-%d %H:%M:%S')
                        cmd.append('--purchaseDate "%s"' % date)
                    except ValueError:
                        pass

        if self.new_ap_executable:
            cmd.append('--cnID "%s"' % track['trackId'])
        # cmd.append('--meta-uuid "cnID" text "%s"' % track['trackId'])

        if 'account' in extra_data and '@' in extra_data['account']:
            if self.new_ap_executable:
                cmd.append('--apID "%s"' % extra_data['account'])
            # cmd.append('--meta-uuid "apID" text "%s"' % extra_data['account'])

        # native tag writing for the following isn't supported by AtomicParsley
        # cmd.append('--meta-uuid "atID" text "%s"' % track['artistId'])
        # cmd.append('--meta-uuid "plID" text "%s"' % track['collectionId'])
        # if track['primaryGenreName'] in self.genre_map:
            # cmd.append('--meta-uuid "geID" text "%s"' % self.genre_map[track['primaryGenreName']])
        # if track['country'] in self.store_map:
            # cmd.append('--meta-uuid "sfID" text "%s"' % self.store_map[track['country']])

        if self.over_write:
            cmd.append('--overWrite')

        return self.__run_command(filename, cmd)

    def get_info(self, filename):
        """Print metadata for the given filename."""
        return self.__run_command(filename, '-t')

    def __run_command(self, filename, command):
        """Run a syscall in order to call AtomicParsley with the given command on the given file."""
        if isinstance(command, str) or isinstance(command, unicode):
            command = [command]

        command = [self.atomic_parsley_file, '"%s"' % filename] + command
        logging.debug(' '.join(command))
        output = os.popen(' '.join(command)).read()
        return output
