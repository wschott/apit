from setuptools import setup


setup(
    name = 'apit',
    version = '0.1',
    author = 'Waldemar Schott',
    author_email = 'code@waldemarschott.com',
    description = ("apit updates the metadata tags of .m4a (AAC and ALAC) "
                   "files with fetched metadata from the iTunes Store."),
    long_description=open('README.md').read(),
    keywords = 'itunes metadata aac',

    packages=['apit'],

    entry_points={
        'console_scripts': [
            'apit = apit:main',
        ]
    },

    test_suite = 'tests',
    tests_require=['mock']
)
