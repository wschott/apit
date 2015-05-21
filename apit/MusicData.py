import os
import re
import json
import urllib2
from collections import defaultdict


def _extract_country_code(url):
    """
    Return the country code (e.g., us, de, uk) for a given `url`.

    Arguments:
    url -- URL to extract the country code
    """
    country = url.split('itunes.apple.com/')[1][0:2].lower()
    return country


def _extract_id(url):
    """
    Return the iTunes Store ID for a given `url`.

    Arguments:
    url -- URL to extract the ID
    """
    sid = url.split('/id')[-1]
    sid = re.match(r'^\d+', sid).group(0)
    return sid


def generate_lookup_query(url):
    """
    Return an iTunes Store query url for the given `url`.

    Arguments:
    url -- URL to generate a lookup URL
    """
    query = url.lstrip('http://').lstrip('https://')

    if not query.startswith('itunes.apple.com/'):
        raise Exception('Invalid query URL: %s' % url)

    country = _extract_country_code(query)
    sid = _extract_id(query)

    query = 'http://itunes.apple.com/lookup?entity=song&country=%s&id=%s' % (country, sid)
    return query


def fetch_data(url):
    """
    Fetch JSON data at the given `url`.

    Arguments:
    url -- location of the JSON data to fetch
    """
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    sock = opener.open(url)
    data = sock.read()
    sock.close()
    return data


def process_data(itunes_data):
    """
    Process JSON data in the given string `itunes_data` by returning two dicts
    containing the information for the album and its songs.

    Arguments:
    itunes_data -- JSON data in a string
    """
    json_result = json.loads(itunes_data)

    if 'results' not in json_result and json_result['resultCount'] == 0:
        raise Exception('no results found')

    album = {}
    data = defaultdict(dict)

    for item in json_result['results']:
        if 'collectionType' in item and item['collectionType'] in ['Album', 'Compilation']:
            album = item
        elif 'kind' in item and item['kind'] == 'song':
            data[item['discNumber']][item['trackNumber']] = item

    return album, data


def _generate_filename(album):
    """
    Return a filename in the format `artist-album-id.json` for the given
    `album`.

    The filename contains `id` for the case that the artist has multiple
    albums with the same name in the iTunes Store.

    Arguments:
    album -- dict containing the data to create the filename
    """
    filename = []
    for part in ['artistName', 'collectionName', 'collectionId']:
        content = str(album[part])
        filename.append(re.sub(r'\W+', '_', content.encode('utf-8')))

    return '%s.json' % '-'.join(filename)


def save_log(json, log_path, album):
    """
    Save a log file with the `json` data of the fetched `album` in `log_path`.

    Arguments:
    json     -- data to save
    log_path -- location of the final log file
    album    -- used to generate the filename
    """
    log_file = os.path.join(log_path, _generate_filename(album))

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    with open(log_file, 'w') as f:
        f.write(json)


def extract_disc_and_track_number(filename):
    """
    Split the disc and track number from a given `filename`
    (e.g. '2-14 song title.m4a' returns 2, 14).
    """
    disc_track = os.path.basename(filename).split(' ')[0]

    # split discnumber if in filename
    if '-' in disc_track:
        disc = disc_track.split('-')[0]
        track = disc_track.split('-')[1]
    else:
        disc = 1
        track = disc_track

    return int(disc), int(track)
