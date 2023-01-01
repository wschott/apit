# apit

[![Build Status](https://github.com/wschott/apit/actions/workflows/python-package.yml/badge.svg)](https://github.com/wschott/apit/actions/workflows/python-package.yml)

**RUN THIS AT YOUR OWN RISK! MAKE A BACKUP BEFORE RUNNING THIS!**

apit allows batch tagging .m4a (AAC and ALAC) file metadata tags using data from Apple Music/iTunes Store.


# Installation

## Requirements

At least [Python](https://www.python.org) 3.10

## apit Installation

    $ cd apit-source-code/  # i.e. this folder
    $ pip install .


# Usage

## Command line help

    $ apit -h

## Print the current metadata

    $ apit show ~/Music/Music/Media/Artist/Album/

## Tag the music files' metadata using data from Apple Music/iTunes Store

    $ apit tag ~/Music/Music/Media/Artist/Album/

### Filename format requirements

The filename of your files must have the following format in order to match them against the Apple Music/iTunes Store metadata:

1. **optional**: **disc number** (followed by "-" or ".")
2. **required**: **track number** (followed by an optional ".")
3. **required**: `.m4a` **extension**

Examples:

   - without disc number (defaults to disc 1)
      - `14.m4a`, `14 title.m4a`, `14. title.m4a`, `#14.m4a`, `#14 title.m4a`
      - `2. 14 title.m4a` (track 2: title contains the number 14)
   - with disc number (e.g. disc 2)
      - `2-14 title.m4a`, `2.14 title.m4a`, `2.14. title.m4a`

### Metadata source requirement

You must provide a source for the metadata to be used. Simply search for the album matching your files in the Apple Music/iTunes Store functionality or in a search engine and copy & paste the link to that album.
The format of that url **must match** the following form (as of 2020-05 using Apple Music on macOS 10.15 Catalina):

    https://music.apple.com/{COUNTRY_CODE}/album/album-name/{ID}
    e.g. https://music.apple.com/us/album/album-name/123456789

or the old style iTunes format:

    http://itunes.apple.com/{COUNTRY_CODE}/album/album-name/id{ID}
    e.g. http://itunes.apple.com/us/album/album-name/id123456789

Even this format will match:

    http://x/us/x/9/123456789?i=09876

This will lookup the metadata of the album with the ID _123456789_ in the _US_ store of Apple Music/iTunes (and optionally download that data to `~/.apit`).

### Attention: Beware of album variations (e.g. deluxe editions)

You should compare your files against the album's metadata you found via the iTunes Store or a search engine. Sometimes the songs' track order vary from album edition to album edition (e.g. deluxe edition) or the album published in another country has a different order. This means that your files will be tagged using the wrong metadata if you choose the wrong edition! You can overcome this by renaming your files before tagging to match against the appropriate metadata. Optionally, you can edit your files' track number metadata again after tagging to revert to your original track order.

## Provide a source using a command line option

You can provide the source using a command line option instead of entering/pasting a source while executing apit:

- either using an **url** (depending on your OS you maybe have to quote the url)
- or using an **already downloaded metadata file** (i.e. no further download will happen)
- or using an **ID**
   - with an optional country code: any non-digit character is required as a separator
   - without a country code: your system's locale will be used

Example using an url:

    $ apit tag ~/Music/Music/Media/Artist/Album/ https://music.apple.com/us/album/album-name/123456789

Example using an existing metadata file:

    $ apit tag ~/Music/Music/Media/Artist/Album/ ~/.apit/Artist-Album-123456789.json

Example using an ID:

    $ apit tag ~/Music/Music/Media/Artist/Album/ us,123456789 # separator character is a comma (",")
    $ apit tag ~/Music/Music/Media/Artist/Album/ 123456789    # uses your system's locale for store determination

## Artwork

Optionally, you can use artwork from Apple Music/iTunes Store and save them to your files using `--artwork` (short: `-a`). Additionally, you can specify your desired pixel size (default: 600).

Examples:

    $ apit -a tag ~/Music/Music/Media/Artist/Album/ https://music.apple.com/us/album/album-name/123456789
    $ apit -a --artwork-size 1000 tag ~/Music/Music/Media/Artist/Album/ https://music.apple.com/us/album/album-name/123456789

## Metadata cache

The downloaded metadata can be saved to your disk for later usage using `--cache` (short: `-c`).

    $ apit --cache tag ~/Music/Music/Media/Artist/Album/ https://music.apple.com/us/album/album-name/123456789

## Create backup files

You can create backup files before updating metadata if you put `--backup` (short: `-b`) in your command.

    $ apit --backup tag ~/Music/Music/Media/Artist/Album/

## Verbose mode

To see more information what happens you can put `-v` into your command. Using `-vv` enables debug output.

    $ apit -v tag ~/Music/Music/Media/Artist/Album/


# apit Development

## Develop mode

Install apit in an editable mode:

    $ pip install --editable ".[dev]"

This will install [tox](https://tox.readthedocs.io/) and other development tools.
Tox is used to run for example tests in an isolated environment. Show all possible actions using:

    $ tox -a

Running a specific tox command will install its necessary dependencies in separate virtualenvs.

Code style is ensured using a pre-commit hook:

    $ pre-commit install


## Building

    $ tox -e build
