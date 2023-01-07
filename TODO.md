# Features

- add CWD usage
- improve logging output
- metadata caching
  - add metadata cache lookup (e.g. using folder name)
  - check against metadata cache before downloading
    - ask user what should be done if already cached data is found
    - allow re-download using -f/--force
  - move metadata downloads to ~/.apit/metadata-cache/?
- add a ~/.apit/config file to omit cli flags?
- add apit execution logging to ~/.apit/logs/?
- allow setting cli flag to optionally overwrite original itunes files (-> don't skip them)?
- add flag to add a new artwork instead of removing all before adding
- new command: download lyrics
- add mp3 support
- search store results and match against local files


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
- Python 3.11+
  - use built-in StrEnum
