import os
import shutil
from tempfile import mkdtemp, NamedTemporaryFile
from unittest import TestCase

from apit.MusicData import (_extract_country_code, _extract_id,
    generate_lookup_query, fetch_data, process_data, _generate_filename,
    save_log, extract_disc_and_track_number)


STORE_URL = 'http://itunes.apple.com/us/album/my-beautiful-dark-twisted/id403822142'
LOOKUP_URL = 'http://itunes.apple.com/lookup?entity=song&country=us&id=403822142'
FILENAME = 'Kanye_West-My_Beautiful_Dark_Twisted_Fantasy-403822142.json'


class TestMusicDataProcessing(TestCase):
    def setUp(self):
        """
        Create a temporary folder for log files.
        """
        self.log_dir = mkdtemp()

    def tearDown(self):
        """
        Delete the temporary log files folder.
        """
        shutil.rmtree(self.log_dir)

    def get_test_data(self):
        with open('tests/metadata.js', 'r') as f:
            data = f.read()
        return data

    def test_extract_country_code(self):
        """
        Test the correct country code extraction based on an iTunes Store URL.
        """
        self.assertEqual(_extract_country_code(STORE_URL), 'us')

    def test_extract_id(self):
        """
        Test the correct ID extraction based on an iTunes Store URL.
        """
        self.assertEqual(_extract_id(STORE_URL), '403822142')

    def test_good_lookup_url(self):
        """
        Test the correct iTunes Store lookup URL generation based on an iTunes
        Store URL.
        """
        self.assertEqual(generate_lookup_query(STORE_URL), LOOKUP_URL)

    def test_bad_lookup_url(self):
        """
        Test that an exception is raised during the iTunes Store lookup URL
        generation based on a random URL.
        """
        with self.assertRaises(Exception):
            generate_lookup_query('http://bad-url.com/')

    def test_fetch_data(self):
        """
        Test the fetching of real iTunes data for an album.
        """
        json = fetch_data(LOOKUP_URL)
        self.assertIn('{\n "resultCount":15,\n "results": [\n{', json)

    def test_process_album(self):
        """
        Test the processing of the album information for a fetched data.
        """
        album, _ = process_data(self.get_test_data())

        self.assertEqual(album['collectionId'], 403822142)
        self.assertEqual(album['collectionName'],
                         'My Beautiful Dark Twisted Fantasy')

    def test_process_songs(self):
        """
        Test the processing of the song information for a fetched data.
        """
        _, songs = process_data(self.get_test_data())

        self.assertEqual(songs[1][3]['kind'], 'song')
        self.assertEqual(songs[1][3]['discNumber'],  1)
        self.assertEqual(songs[1][3]['trackNumber'], 3)
        self.assertEqual(songs[1][3]['trackName'], 'Power')

    def test_filename_generation(self):
        """
        Test the generation of the filename for given album data.
        """
        album, _ = process_data(self.get_test_data())

        self.assertEqual(_generate_filename(album), FILENAME)

    def test_log_file_saving(self):
        """
        Test the log file creation for given test data.
        """
        test_data = self.get_test_data()
        album, _ = process_data(test_data)

        save_log(test_data, self.log_dir, album)

        with open(os.path.join(self.log_dir, FILENAME), 'r') as f:
            actual = f.read()

        self.assertEqual(actual, test_data)

    def test_disc_track_number(self):
        """
        Test the correct extraction of the disc and track number for a given
        filename with both numbers.
        """
        self.assertEqual(
            extract_disc_and_track_number('2-14 song title.m4a'),
            (2, 14)
        )

    def test_only_track_number(self):
        """
        Test the correct extraction of the disc and track number for a given
        filename with only a track number and no disc number.
        """
        self.assertEqual(
            extract_disc_and_track_number('14 song title.m4a'),
            (1, 14)
        )
