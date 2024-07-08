# Features

- add CWD usage
- improve logging output
- add -f cli flag to allow writing m4a files from iTunes store
- add flag to add a new artwork instead of removing all before adding
- new command: download lyrics
- search store results and match against local files
- add "not actionable" message for original iTunes store files
- musicbrainz lookup + tagging
- acoustid fingerprint


# Development

- refactor test data/fixture setup
- add more tests
- pass args to functions for better testability
- https://docs.pytest.org/en/latest/monkeypatch.html
- use capsys fixture to capture and analyze stdout/stderr: https://docs.pytest.org/en/latest/capture.html
- simplify loops (and other constructs) using FP
- setup dev mode for VS code (e.g. w/ pip install flake8 ...)
- configure mypy: https://mypy.readthedocs.io/en/stable/config_file.html#config-file
- dynamic version: https://github.com/pypa/setuptools_scm
- Python 3.12+
  - @override (~typing_extensions 4.4.0)
