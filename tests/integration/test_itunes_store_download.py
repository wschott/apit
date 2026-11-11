import json

import pytest

from apit.infra.metadata_source.itunes_store_loader import ItunesStoreLoader


@pytest.mark.integration
def test_download_metadata_using_real_itunes_data():
    json_str = ItunesStoreLoader().download_metadata(
        {"country_code": "us", "id": "1440742903"}
    )

    data = json.loads(json_str)

    assert data["resultCount"] == 15

    # test some album data
    assert data["results"][0]["collectionId"] == 1440742903
    assert data["results"][0]["collectionType"] == "Album"
    assert data["results"][0]["artistName"] == "Kanye West"
    assert data["results"][0]["collectionName"] == "My Beautiful Dark Twisted Fantasy"
    assert data["results"][0]["copyright"] == "℗ 2010 UMG Recordings, Inc."

    # test some song data
    assert data["results"][1]["kind"] == "song"
    assert data["results"][1]["trackName"] == "Dark Fantasy"
    assert data["results"][1]["trackNumber"] == 1
    assert data["results"][1]["trackCount"] == 13


@pytest.mark.integration
def test_downloaded_artwork():
    artwork_content, _ = ItunesStoreLoader().download_artwork(
        "https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/88/92/4c/88924c01-6fb3-8616-f0b3-881b1ed09e03/source/100x100bb.jpg",
        100,
    )

    assert b"JFIF" in artwork_content
