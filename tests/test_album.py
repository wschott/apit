from apit.album import Album


def test_album():
    album = Album({
        'collectionId': 12345,
        'artistName': 'test-artist',
        'collectionName': 'test-collection',
    })
    assert album['collectionId'] == 12345
    assert album['artistName'] == 'test-artist'
    assert album['collectionName'] == 'test-collection'
