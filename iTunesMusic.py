import re
import urllib2
import json
import os
from StringIO import StringIO

class iTunesMusic():
    def __init__(self, source, log_path='~/logs'):
        self.source = source
        self.log_path = log_path
        self.album = {}
        self.data = {}
        
        self.load_source(source)

    def load_source(self, source):
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        sock = opener.open(source)
        self.original_data = sock.read()
        self.init_data(json.load(StringIO(self.original_data)))
        sock.close()
        self.save_json_to_file()

    def init_data(self, json_result):
        if 'results' not in json_result and json_result['resultCount'] == 0:
            raise Exception('no results found')
        self.original = json_result['results']

        for item in json_result['results']:
            if 'collectionType' in item and item['collectionType'] in ['Album', 'Compilation']:
                self.album = item
            elif 'kind' in item and item['kind'] == 'song':
                if item['discNumber'] not in self.data:
                    self.data[item['discNumber']] = {}
                self.data[item['discNumber']][item['trackNumber']] = item

    def get_songs(self):
        return self.data

    def get_album(self):
        return self.album

    def save_json_to_file(self):
        album_data = self.get_album()

        # filename: logs/artist-album-id.json
        filename = []
        for part in ['artistName', 'collectionName', 'collectionId']:
            if isinstance(album_data[part], int):
                content = str(album_data[part])
            else:
                content = album_data[part]
            filename.append(re.sub(r'\W+', '_', content.encode('utf-8')))

        try:
            os.makedirs(self.log_path)
        except OSError:
            pass

        fsock = open('%s/%s.json' % (self.log_path, '-'.join(filename)), 'w')
        fsock.write(self.original_data)
        fsock.close()
