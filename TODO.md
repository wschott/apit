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


# Development

- refactor test data/fixture setup
- reasearch alternative tagging tools
  - mutagen (has mp3 support)
  - ...
- add more tests
- pass args to functions for better testability
- https://docs.pytest.org/en/latest/monkeypatch.html
- use capsys fixture to capture and analyze stdout/stderr: https://docs.pytest.org/en/latest/capture.html
- simplify loops (and other constructs) using FP
- use and configure flake8?
- setup dev mode for VS code (e.g. w/ pip install flake8 ...)
- configure mypy: https://mypy.readthedocs.io/en/stable/config_file.html#config-file
