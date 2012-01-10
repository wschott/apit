# apit

**RUN THIS AT YOUR OWN RISK! MAKE A BACKUP BEFORE RUNNING THIS!**

apit updates the metadata tags of .m4a (AAC and ALAC) files with fetched
metadata from the iTunes Store.


# Requirements

You need either an [*old* version of Atomicparsley ](http://atomicparsley.sourceforge.net/)
or a [*new* version of AtomicParsley](https://bitbucket.org/wez/atomicparsley).

Run the following in your Terminal to compile the new version for OS X Lion:

	$ make maintainer-clean
	$ ./configure --disable-universal
	$ make


# Usage

Make sure `apit.py` is executable (`chmod u+x apit.py`).

Tip: put `apit.py` on your `$PATH` to run it from everywhere.

**Please update the settings in `apit.py` to meet your needs:** (I'll refactor this sometime)

	AP_FILE = ''
	DEBUG_LOG_FILE = os.path.abspath(os.path.expanduser('~/Desktop/apit/debug.log'))
	LOG_PATH = os.path.abspath(os.path.expanduser('~/Desktop/apit/logs'))
	UPDATES_LOG_FILE = os.path.abspath(os.path.expanduser('~/Desktop/apit/updates.log'))
	OVERWRITE_FILES = True
	NEW_EXECUTABLE_VERSION = True


Open your Terminal and run this

## Print the current metadata

	~/path/to/apit.py --info ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/

## Update the metadata of your music files with fetched metadata from the iTunes Store

	~/path/to/apit.py --update ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/

your have to provide a source for the metadata to fetch by copy & paste'ing
a link to an album in the Store functionality in the iTunes.app

	http://itunes.apple.com/us/album/my-beautiful-dark-twisted/id403822142

Additionally it's possible to specify a purchase date (format: YYYY-MM-DD, …)

If you put `--overwrite` in your command your files will be overwritten, otherwise temporary files will be created:

	~/path/to/apit.py --update --overwrite ~/Music/iTunes/iTunes\ Media/Music/Kanye\ West/My\ Beautiful\ Dark\ Twisted\ Fantasy/
