#!/usr/bin/env python

import os
import sys
import re
import logging

from AtomicParser import AtomicParser
from iTunesMusic import iTunesMusic

AP_FILE = ''
DEBUG_LOG_FILE = os.path.abspath(os.path.expanduser('~/Desktop/apit/debug.log'))
LOG_PATH = os.path.abspath(os.path.expanduser('~/Desktop/apit/logs'))
UPDATES_LOG_FILE = os.path.abspath(os.path.expanduser('~/Desktop/apit/updates.log'))
OVERWRITE_FILES = True
NEW_EXECUTABLE_VERSION = True


def get_files(path, filter_ext=None):
    """Return a list of files in the given path. This list might be filtered
    by a given list of extensions.

    Keyword arguments:
    filter_ext -- the (list of) extension(s) by which the files will be filtered (default None)
    """
    ret = [os.path.join(path, f) for f in os.listdir(path)]

    if filter_ext:
        if isinstance(filter_ext, str) or isinstance(filter_ext, unicode):
            filter_ext = [filter_ext]
        ret = [f for f in ret if os.path.splitext(f)[1] in filter_ext]

    return ret

def save_to_file(query, path):
    fsock = open(UPDATES_LOG_FILE, 'a')
    fsock.write('%s\t%s\n' % (query, path))
    fsock.close()

def get_itunes_query(source):
    query = source
    country = 'US'
    if query.startswith('http://itunes.apple.com/'):
        country = query.split('http://itunes.apple.com/')[1][0:2].upper()
        logging.debug("country: '%s' for %s" % (country, query))
        sid = query.split('/id')[1]
        sid = re.match(r'^\d+', sid).group(0)
        query = 'http://itunes.apple.com/lookup?entity=song&country=%s&id=%s' % (country, sid)
        logging.debug("itunes search query: '%s'" % query)
    return query

def extract_disc_and_track_number(filename):
    """Split the disc and track number from a given filename
    (e.g. '2-14 song title.m4a' returns 2, 14)."""
    track_disc = os.path.basename(filename).split(' ')[0]
    # split discnumber if in filename
    if '-' in track_disc:
        disc = int(track_disc.split('-')[0])
        track = int(track_disc.split('-')[1])
    else:
        disc = 1
        track = int(track_disc)
    return disc, track


if __name__ == '__main__':
    if '--help' in sys.argv:
        print '''possible actions:
            --info /path/to/m4a/files
            --update /path/to/m4a/files'''

    logging.basicConfig(filename=DEBUG_LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    path = sys.argv[-1]

    if not os.path.isdir(path):
        raise Exception("given path '%s' is not readable (the path has to be the last argument)" % path)
    logging.debug('path: %s' % path)

    ap = AtomicParser(AP_FILE, OVERWRITE_FILES, NEW_EXECUTABLE_VERSION)

    if '--info' in sys.argv:
        for f in get_files(path, '.m4a'):
            print "\n%s\n%s" % (f, ap.get_info(f))
        exit()

    if '--overwrite' in sys.argv:
        AtomicParser.over_write = True
        logging.debug('files will be overwritten')

    extra_data = {}
    query = raw_input('source URL? [http://itunes.apple.com/...]: ')
    extra_data['purchaseDate'] = raw_input('update purchase date? [ YYYY-MM-DD | YYYY-MM-DD-HH-MM-SS | y | n ]: ')
    extra_data['account'] = raw_input('update account? [test@example.com]: ')
    print

    if query == '':
        raise Exception('please provide a source!')

    query = get_itunes_query(query)
    music = iTunesMusic(query, LOG_PATH)
    album = music.get_album()
    songs = music.get_songs()
    files = get_files(path, '.m4a')

    # skip files which were bought on iTunes
    for f in files[:]:
        fileinfo = ap.get_info(f)
        if fileinfo is None:
            raise Exception("AtomicParsley can not read the metadata of '%s'" %  f)
        if 'Atom "flvr" contains:' in fileinfo or 'Atom "xid " contains:' in fileinfo:
            files.remove(f)
            print 'iTunes purchased song -> skipped: %s' % f

    print
    for f in files[:]:
        disc, track = extract_disc_and_track_number(f)
        # update only if the file's tracknumber is in the search result
        if disc in songs and track in songs[disc]:
            result = ap.update_metadata(f, songs[disc][track], album, extra_data)
            print '\nupdating: %s%s' % (f, result)
            files.remove(f)

    save_to_file(query, path)

    print
    for f in files:
        print 'NOT updated: %s' % f
