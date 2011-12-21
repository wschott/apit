#!/usr/bin/env python

import os
import sys
import re
import logging

from AtomicParser import AtomicParser
from iTunesMusic import iTunesMusic

AP_FILE = ''
DEBUG_LOG_FILE = 'debug.log'
LOG_PATH = 'logs'
UPDATES_LOG_FILE = 'updates.log'
OVERWRITE_FILES = True


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
    fsock = open('updates.log', 'a')
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

if __name__ == '__main__':
    if '--help' in sys.argv:
        print '''possible actions:
            --info
            --update'''

    logging.basicConfig(filename=DEBUG_LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    path = sys.argv[-1]

    if not os.path.isdir(path):
        raise Exception("given path '%s' is not readable (the path has to be the last argument)" % path)
    logging.debug('path: %s' % path)

    ap = AtomicParser(AP_FILE, OVERWRITE_FILES)

    if '--info' in sys.argv:
        for f in get_files(path, '.m4a'):
            print "\n%s\n" % (f, ap.get_info(f))
        exit()

    if '--overwrite' in sys.argv:
        AtomicParser.over_write = True
        logging.debug('files will be overwritten')

    extra_data = {}
    query = raw_input('source URL? [http://itunes.apple.com/...]: ')
    extra_data['purchaseDate'] = raw_input('update purchase date? [ YYYY-MM-DD | YYYY-MM-DD_HH-MM-SS | y | n ]: ')
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
    for f in files:
        fileinfo = ap.get_info(f)
        if 'Atom "flvr" contains:' in fileinfo or 'Atom "xid " contains:' in fileinfo:
            files.remove(f)
            print 'iTunes purchased song -> skipped: %s' % f

    print
    for f in files[:]:
        track_disc_number = os.path.basename(f).split(' ')[0]
        # split discnumber if in filename
        if '-' in track_disc_number:
            disc_number = int(track_disc_number.split('-')[0])
            track_number = int(track_disc_number.split('-')[1])
        else:
            disc_number = 1
            track_number = int(track_disc_number)
        # update only if the file's tracknumber is in the search result
        if track_number in songs[disc_number]:
            result = ap.update_metadata(f, songs[disc_number][track_number], album, extra_data)
            print '\nupdating: %s%s' % (f, result)
            files.remove(f)
    
    save_to_file(query, path)
    
    print
    for f in files:
        print 'NOT updated: %s' % f
