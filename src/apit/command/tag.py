import logging
from pathlib import Path
from typing import List

from apit.album import Album
from apit.atomic_parser import is_itunes_bought_file
from apit.cmd import execute_command_for_file
from apit.debug_helper import logging_debug_filelist
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata_store import save_log
from apit.musicdata import (
    extract_album_and_song_data,
    fetch_store_json_string,
    generate_store_lookup_url,
)
from apit.report import report_to_shell
from apit.song import Song

RATING_MAP = {
    'cleaned': 'clean',
    'explicit': 'explicit',
    'notExplicit': 'remove',
}

ITEM_TYPE_MAP = {
    'song': 'Normal',
}

# https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
# GENRE_MAP = {
#     'Hip Hop/Rap': 18,
#     'Hip-Hop/Rap': 18,
#     'Dance': 17,
#     'Rock': 21,
# }

def execute(files: List[Path], options):
    source: str = options.source

    if not source:
        source = ask_user_for_input()
    logging.info('URL provided: %s', source)

    store_json = None
    if source.startswith('http'):
        logging.info('Use url to fetch music data: %s', source)
        query_url = generate_store_lookup_url(source)
        logging.debug('URL for query: %s', query_url)

        store_json = fetch_store_json_string(query_url)

        if options.has_search_result_cache_flag:
            metadata_cache_path = save_log(store_json, options.log_path)
            logging.info("Metadata search result cached to '%s'", metadata_cache_path)
    elif Path(source).exists():
        logging.info('Use already loaded file to fetch music data: %s', source)
        store_json = Path(source).read_text()
    else:
        raise ApitError(f'Provided path "{source}" doesn\'t exist')

    album = extract_album_and_song_data(store_json)

    files_to_skip_due_to_itunes_original = [f for f in files if is_itunes_bought_file(f)]
    logging_debug_filelist('files_to_skip_due_to_itunes_original:', files_to_skip_due_to_itunes_original)

    files_to_skip_due_to_mismatched_tracknumber = [f for f in files if _is_file_mismatch(f, album)]
    logging_debug_filelist('files_to_skip_due_to_mismatched_tracknumber:', files_to_skip_due_to_mismatched_tracknumber)

    files_to_update = files
    files_to_update = [f for f in files_to_update if f not in files_to_skip_due_to_itunes_original]
    files_to_update = [f for f in files_to_update if f not in files_to_skip_due_to_mismatched_tracknumber]
    logging_debug_filelist('Files to update:', files_to_update)

    files_with_update_error = []
    for file in files_to_update:
        status = _update_file(file, album, options.has_overwrite_flag)
        if status.returncode:
            files_with_update_error.append({'file': file, 'status': status})
        report_to_shell(file, status)

    if files_to_skip_due_to_itunes_original:
        print()
        logging.warn('Skipped (original/purchased iTunes Store file):')
        for file in files_to_skip_due_to_itunes_original:
            logging.warn('  %s', file.name)

    if files_to_skip_due_to_mismatched_tracknumber:
        print()
        logging.warn('Skipped (track number (or disc number) not matched against Apple Music/iTunes Store results):')
        for file in files_to_skip_due_to_mismatched_tracknumber:
            logging.warn('  %s', file.name)

    if files_with_update_error:
        print()
        logging.error('Errors during file updating:')
        for file_status in files_with_update_error:
            file = file_status['file']
            status = file_status['status']
            logging.error('  %s', file.name)
            logging.error('    stdout: %s', status.stdout.strip())
            logging.error('    stderr: %s', status.stderr.strip())

def ask_user_for_input() -> str:
    url = None
    try:
        url = input('Input Apple Music/iTunes Store URL (starts with https://music.apple.com/...): ')
    except KeyboardInterrupt:
        print()  # to nicely print the following error onto the next line
    if not url:
        raise ApitError('No Apple Music/iTunes Store URL provided')
    return url

def _is_file_mismatch(file: Path, album: Album) -> bool:
    disc, track = extract_disc_and_track_number(file)
    return not album.hasSong(track, disc)

def _update_file(file: Path, album: Album, should_overwrite: bool):
    disc, track = extract_disc_and_track_number(file)
    return update_metadata(file, album, album.getSong(track, disc), should_overwrite)

def update_metadata(file: Path, album_metadata: Album, track_metadata: Song, should_overwrite: bool):
    command = _generate_metadata_update_command(album_metadata, track_metadata, should_overwrite)
    return execute_command_for_file(file, command, shell=True)

def _generate_metadata_update_command(album_metadata: Album, track_metadata: Song, should_overwrite: bool) -> List[str]:
    command = [
        f'--artist "{track_metadata["artistName"]}"',
        f'--title "{track_metadata["trackCensoredName"]}"',
        f'--album "{track_metadata["collectionName"]}"',
        f'--genre "{track_metadata["primaryGenreName"]}"',
        f'--year "{track_metadata["releaseDate"]}"',
        f'--disknum {track_metadata["discNumber"]}/{track_metadata["discCount"]}',
        f'--tracknum {track_metadata["trackNumber"]}/{track_metadata["trackCount"]}',
        f'--advisory {RATING_MAP[track_metadata["trackExplicitness"]]}',
        f'--stik "{ITEM_TYPE_MAP[track_metadata["kind"]]}"',
        f'--albumArtist "{album_metadata["artistName"]}"',
        f'--copyright "{album_metadata["copyright"]}"',
        f'--cnID "{track_metadata["trackId"]}"',
    ]

    # command.append(f'--xID "{track[]}"')

    # if track['primaryGenreName'] in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track["primaryGenreName"]]}"')

    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track["artistId"]}"')
    # command.append(f'--plID "{track["collectionId"]}"')

    if should_overwrite:
        command.append('--overWrite')

    return command
