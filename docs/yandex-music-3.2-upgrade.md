# yandex-music 3.2.0 compatibility

The provider requires `yandex-music[async]==3.2.0`. The async extra declares the
HTTP and file-I/O dependencies used by ClientAsync.

Radio feedback now uses the library's JSON request body. Parser fixtures use a
real, disconnected ClientAsync so model deserialization follows the same schema
and JSON configuration as production. The library's published type annotations
are checked without broadening the repository's mypy exceptions.

Stream delivery continues through bounded Range requests, preserving retry,
URL refresh, seek and AES-CTR handling. File-info requests use the public Request
property and preserve the provider's existing signature and quality parameters.
The new tracks_file_info convenience method uses a different desktop signature
and client header; adopting it requires a separate check with real KION credentials.

## Validation

Validated with Python 3.14.3, yandex-music 3.2.0, music-assistant-models 1.1.217
and Music Assistant dev commit c0f4425c92867e76a84afb9430bac60a1d400c24.

- Full provider suite, including real server cache and scheduling fixtures.
- Parser snapshots covering current access, favorite and metadata fields.
- Real ClientAsync feedback methods with only HTTP transport replaced.
- Reconnect throttling and expired-URL priority regressions.
- Ruff, mypy and repository pre-commit checks.

The environment uses installed supporting dependencies because the current MA
PyTorch download host was unavailable. Tests exercise MA's current source and
models; authenticated KION playback and the full MA server suite are separate
checks and were not run.

The work consolidates provider PRs #179, #182, #184 and #188. Their closure and
merging this branch are maintainer decisions.
