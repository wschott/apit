# apit

[![Build Status](https://travis-ci.org/wschott/apit.svg?branch=master)](https://travis-ci.org/wschott/apit)

**RUN THIS AT YOUR OWN RISK! MAKE A BACKUP BEFORE RUNNING THIS!**

apit updates the metadata tags of .m4a (AAC and ALAC) files with fetched metadata from the iTunes Store.


# Requirements

You need either an [*old* version of Atomicparsley ](http://atomicparsley.sourceforge.net/) or a [*new* version of AtomicParsley](https://bitbucket.org/wez/atomicparsley).

Run the following in your terminal to compile the new version for at least OS X Lion:

    $ make maintainer-clean
    $ ./configure --disable-universal
    $ make


# Installation

You can install apit into your system Python library location or into a virtualenv.
Just run the following in your terminal.

    $ python setup.py install


# Usage

## Print the current metadata

    $ apit --info ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/

## Update the metadata of your music files with fetched metadata from the iTunes Store

    $ apit --update ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/

You have to provide a source for the metadata to fetch by copy & past'ing a link to an album from the Store functionality of iTunes.

    http://itunes.apple.com/us/album/my-beautiful-dark-twisted/id403822142

Additionally, it's possible to specify a purchase date (format: YYYY-MM-DD, …)

If you put `--overwrite` in your command your files will be overwritten, otherwise temporary files will be created:

    $ apit --update --overwrite ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/

It's possible to trigger the AtomicParsley version you're using with the `-old-version` parameter.
