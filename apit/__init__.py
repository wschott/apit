import os
from optparse import OptionParser

from AtomicParser import get_info, update_metadata
from MusicData import generate_lookup_query, fetch_data, process_data, \
    save_log, extract_disc_and_track_number


LOG_PATH = os.path.abspath(os.path.expanduser('~/.apit'))


def parse_args():
    p = OptionParser('usage: %prog [options] PATH \n\n%prog only supports .mp4 files')

    p.add_option('-i', '--info', dest='info',
                 default=False, action='store_true',
                 help='show current tag information')
    p.add_option('-u', '--update', dest='update',
                 default=False, action='store_true',
                 help='update the .m4a files in the given path')
    p.add_option('-o', '--overwrite', dest='overwrite',
                 action='store_true', default=True,
                 help='overwrite the files [default: %s]' % True)
    p.add_option('-l', '--old-version', dest='old_version',
                 default=False, action='store_false',
                 help='specify whether you are using an old or a new AtomicParsley version [default: %s = new version]' % False)
    #p.add_option('-p', '--path', dest='path',
    #             action='store', type='string',
    #             help='specify the path containing the .m4a files')

    return p.parse_args()


def get_files(path, filter_ext=None):
    """
    Return a list of files in the given `path`. This list might be filtered by
    a given list of extensions provided in `filter_ext`.
    """
    ret = [os.path.join(path, f) for f in os.listdir(path)]

    if not filter_ext:
        return ret

    if isinstance(filter_ext, (unicode, str)):
        filter_ext = [filter_ext]
    return filter(lambda f: os.path.splitext(f)[1] in filter_ext, ret)


def print_file_result(file, status):
    print('-'*80)
    print(os.path.basename(file))
    print('')
    print(status)


def print_file_infos(files):
    for f in files:
        print_file_result(f, get_info(f))


def ask_user_for_data():
    extra_data = {}

    url = raw_input('iTunes Store URL? [http://itunes.apple.com/...]: ')
    if not url:
        exit('Please provide an iTunes Store URL')

    extra_data['purchaseDate'] = raw_input('update purchase date? [ YYYY-MM-DD | YYYY-MM-DD-HH-MM-SS | y | n ]: ')
    extra_data['account'] = raw_input('update account? [test@example.com]: ')

    return url, extra_data


def skip_itunes_files(files):
    """
    Skip files that were bought on iTunes.
    """
    files_to_process = []

    for f in files:
        fileinfo = get_info(f)
        if fileinfo is None:
            exit("AtomicParsley is not able read the metadata of '%s'. Is this a valid .m4a file?" % f)
        if 'Atom "flvr" contains:' in fileinfo or 'Atom "xid " contains:' in fileinfo:
            print_file_result(f, 'iTunes purchased song -> skip')
        else:
            files_to_process.append(f)

    return files_to_process


def update_files(files, songs, album, extra_data, overwrite, old_version):
    for f in files[:]:
        disc, track = extract_disc_and_track_number(f)
        # update only if the file's tracknumber is in the search result
        if disc in songs and track in songs[disc]:
            result = update_metadata(f, songs[disc][track], album, extra_data, overwrite, old_version)
            print_file_result(f, "updating: %s" % result)
            files.remove(f)

    return files


def process(options, path):
    files = get_files(path, '.m4a')

    if options.info:
        print_file_infos(files)
        exit()
    elif options.update:
        url, extra_data = ask_user_for_data()

        query = generate_lookup_query(url)
        data = fetch_data(query)
        album, songs, = process_data(data)
        save_log(data, LOG_PATH, album)

        files = skip_itunes_files(files)

        files = update_files(files, songs, album, extra_data, options.overwrite, options.old_version)

        for f in files:
            print_file_result(f, 'NOT updated')
    else:
        exit('Please specify a mode (i.e., -u to update tags or -i to show the current tags)')


def main():
    options, args = parse_args()

    if not len(args):
        exit('Please specify a path.')

    path = args[0]

    if not os.path.isdir(path):
        exit("Specified path '%s' is not accessible." % path)

    process(options, path)
