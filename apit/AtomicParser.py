# -*- coding: utf-8 -*-

# --composer, --grouping, --bpm, --compilation, --encodingTool, --gapless

import os
import datetime


DEFAULT_AP_LOCATIONS = (
    '/Applications/AtomicParsley',
    '~/Applications/AtomicParsley',
    '~/bin/AtomicParsley'
)


DATE_FORMAT = (
    '%Y-%m-%d',
    '%Y-%m-%d_%H',
    '%Y-%m-%d-%H',
    '%Y-%m-%d_%H-%M',
    '%Y-%m-%d-%H-%M',
    '%Y-%m-%d_%H-%M-%S',
    '%Y-%m-%d-%H-%M-%S'
)


RATING_MAP = {
    'cleaned': 'clean',
    'explicit': 'explicit',
    'notExplicit': 'remove'
}


KIND_MAP = {
    'song': 'Normal'
}


# GENRE_MAP = {
#     'Hip Hop/Rap': 18,
#     'Hip-Hop/Rap': 18,
#     'Dance': 17
# }


# STORE_MAP = {
#     'USA': 'United States (143441)',
#     'DEU': 'Germany (143443)'
# }


def get_atomicparsley():
    """
    Find the AtomicParsley executable.
    """
    for f in DEFAULT_AP_LOCATIONS:
        if os.path.isfile(os.path.expanduser(f)):
            return f

    raise Exception('AtomicParsley executable not found. Default locations: %s' % ', '.join(DEFAULT_AP_LOCATIONS))


# def get_atomicparsley_version(ap):
#     return os.popen(get_atomicparsley() + ' -v').read()


def escape(string):
    return string.replace('"', '\\"')


def add_extra_data_to_command(extra_data, old_version):
    cmd = []

    if 'purchaseDate' in extra_data:
        if extra_data['purchaseDate'] == 'y':
            cmd.append('--purchaseDate "timestamp"')
        elif extra_data['purchaseDate'] not in ('', 'n'):
            for fmt in DATE_FORMAT:
                try:
                    date = datetime.datetime.strptime(extra_data['purchaseDate'], fmt).strftime('%Y-%m-%d %H:%M:%S')
                    cmd.append('--purchaseDate "%s"' % date)
                except ValueError:
                    pass

    if 'account' in extra_data and '@' in extra_data['account']:
        if not old_version:
            cmd.append('--apID "%s"' % extra_data['account'])
        # else:
        #     cmd.append('--meta-uuid "apID" text "%s"' % extra_data['account'])

    return cmd


def construct_update_command(track, album, extra_data, overwrite, old_version):
    cmd = []
    cmd.append('--artist "%s"'      % escape(track['artistName']))
    cmd.append('--title "%s"'       % escape(track['trackCensoredName']))
    cmd.append('--album "%s"'       % escape(track['collectionName']))
    cmd.append('--genre "%s"'       % escape(track['primaryGenreName']))
    cmd.append('--year "%s"'        % track['releaseDate'])
    cmd.append('--disknum %s/%s'    % (track['discNumber'], track['discCount']))
    cmd.append('--tracknum %s/%s'   % (track['trackNumber'], track['trackCount']))
    cmd.append('--advisory %s'      % RATING_MAP[track['trackExplicitness']])
    cmd.append('--stik "%s"'        % KIND_MAP[track['kind']])
    cmd.append('--albumArtist "%s"' % escape(album['artistName']))
    cmd.append('--copyright "%s"'   % escape(album['copyright']))

#    if not old_version:
#        cmd.append('--cnID "%s"' % track['trackId'])
    # else:
        # cmd.append('--meta-uuid "cnID" text "%s"' % track['trackId'])

    cmd.extend(add_extra_data_to_command(extra_data, old_version))

    # native tag writing for the following isn't supported by AtomicParsley yet
    # cmd.append('--meta-uuid "atID" text "%s"' % track['artistId'])
    # cmd.append('--meta-uuid "plID" text "%s"' % track['collectionId'])
    # if track['primaryGenreName'] in GENRE_MAP:
        # cmd.append('--meta-uuid "geID" text "%s"' % GENRE_MAP[track['primaryGenreName']])
    # if track['country'] in STORE_MAP:
        # cmd.append('--meta-uuid "sfID" text "%s"' % STORE_MAP[track['country']])

    if overwrite:
        cmd.append('--overWrite')

    return cmd


def _construct_command(filename, command):
    if isinstance(command, (unicode, str)):
        command = [command]

    command = [get_atomicparsley(), '"%s"' % filename] + command

    command = map(lambda x: x.encode('utf-8'), command)

    cmd = ' '.join(command).replace('$', '\\$')
    return cmd


def _exec_command(filename, command):
    """
    Execute a syscall in order to call AtomicParsley with the given `command` on
    the given `filename`.
    """
    cmd = _construct_command(filename, command)
    return os.popen(cmd).read()


def get_info(filename):
    """
    Return metadata for the given `filename`.
    """
    return _exec_command(filename, '-t')


def update_metadata(filename, track, album, extra_data, overwrite, old_version):
    """
    Update the metadata in the file specified by the given `filename` with
    information in `track`, `album` and `extra_data`. It's possible to overwrite
    the files using `overwrite`. Moreover the AtomicParsley version is specified
    using `old_version`.
    """
    cmd = construct_update_command(track, album, extra_data, overwrite, old_version)
    print(_construct_command(filename, cmd))
    return _exec_command(filename, cmd)
