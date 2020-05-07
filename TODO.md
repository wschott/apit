# Features

- add preview + confirmation before updating
  - (-> interactive mode like in isort unnecessary)
  - allows CWD usage
  - allows checking metadata cache lookup using e.g. folder name (otherwise exit)
- allow CWD usage
  -  interactive mode (`-i`?) (like isort (see `isort -h`))?
  - `apitt` (apit this) or `apith` (apit here)?
- improve logging output
- check against metadata cache before downloading
  - ask user what should be done if already cached data is found
  - allow re-download using -f/--force
- add a ~/.apit/config file to omit cli flags?
- metadata caching
  - move metadata downloads to ~/.apit/metadata-cache/?
- add apit execution logging to ~/.apit/logs/?
- allow setting AtomicParsley location using a cli option
- allow setting cli flag to optionally overwrite original itunes files (-> don't skip them)?
- save artwork to file
  - "--artwork /path/to/art.jpg"
  - use json property "artworkUrl100", manipulate to use 600x600, download artwork and pass as value to file
- research about more AtomicParsley flags: --composer, --grouping, --bpm, --compilation, --encodingTool, --gapless


# Development

- reasearch alternative tagging tools
  - mutagen (has mp3 support)
  - ...
- add more tests
- pass args to functions for better testability
- https://docs.pytest.org/en/latest/monkeypatch.html
- use capsys fixture to capture and analyze stdout/stderr: https://docs.pytest.org/en/latest/capture.html
- use pytest-cov?
- simplify loops (and other constructs) by transforming to functional programming
- use and configure flake8?
- setup dev mode for VS code (e.g. w/ pip install flake8 ...)
- configure mypy: https://mypy.readthedocs.io/en/stable/config_file.html#config-file
- Python 3.7+:
  - subprocess.run args: https://docs.python.org/3.7/library/subprocess.html#subprocess.run
  - use @dataclass for Album and Song? https://www.python.org/dev/peps/pep-0557/
