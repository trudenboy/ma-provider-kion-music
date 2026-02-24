# Copilot Instructions — ma-provider-kion-music

## What This Is

A [Music Assistant](https://music-assistant.io/) provider that exposes KION Music (MTS) via the Yandex Music API (`yandex-music` library). The provider is loaded by MA at runtime from the `provider/` directory.

## Commands

**Setup** (run after `git pull` — MA models version may change):
```bash
./scripts/setup.sh
```

**Tests:**
```bash
pytest tests/ -m "not integration"       # unit tests only (fast, no MA server)
pytest tests/                            # full suite (stop dev server first — port conflict)
pytest tests/test_parsers.py             # single test file
pytest --cov=provider --cov-report=html tests/   # with coverage
```

**Lint / type check:**
```bash
pre-commit run --all-files               # ruff + mypy + codespell (run before PR)
uv run mypy provider/                    # type check only
uv run ruff check provider/             # lint only
uv run ruff format --check provider/   # format check only
```

**Dev server** (Music Assistant with live provider, UI at `http://localhost:8095`):
```bash
./scripts/dev-server.sh
```

## Architecture

```
provider/
  provider.py      # KionMusicProvider — main class, extends MusicProvider (MA base class)
  api_client.py    # KionMusicClient — wraps yandex_music.ClientAsync, handles auth/retries
  parsers.py       # parse_track/album/artist/playlist — converts yandex_music objects → MA models
  streaming.py     # KionMusicStreamingManager — resolves stream URLs, handles AES decryption
  constants.py     # all string constants and numeric defaults
  manifest.json    # provider metadata (domain: kion_music, type: music)

tests/
  conftest.py           # concrete stub classes (no Mock); ProviderStub, StreamingProviderStub
  fixtures/             # JSON snapshots of real API responses (artists/, albums/, tracks/, playlists/)
  __snapshots__/        # syrupy snapshot files (auto-updated with --snapshot-update)
  test_parsers.py       # parser unit tests — parametrized over fixture files
  test_integration.py   # full MA in-process tests (marked @pytest.mark.integration)
  test_streaming.py     # streaming unit tests
  test_api_client.py    # API client unit tests
  test_my_mix.py        # My Mix / rotor-specific tests
```

**Data flow:** MA calls `KionMusicProvider` → `KionMusicClient` fetches from Yandex/KION API → `parsers.py` converts to MA model types → MA stores/plays.

**My Mix track IDs** use a composite format: `track_id@station_id`. Any code touching item IDs must handle this separator (`RADIO_TRACK_ID_SEP`).

## Key Conventions

**No `unittest.mock`** — tests use hand-written stub classes in `conftest.py`. Add new stubs there when needed.

**Snapshot tests** — parser tests compare against syrupy snapshots. Update with:
```bash
pytest tests/test_parsers.py --snapshot-update
```

**Fixture files** — when adding API response coverage, add JSON files under `tests/fixtures/<type>/`. Existing tests auto-discover via `glob("*.json")`.

**Branch naming:**
```
feature/<2-4-word-kebab>   # new functionality
fix/<2-4-word-kebab>       # bugfixes
chore/<2-4-word-kebab>     # maintenance
```
PRs target `dev`; `dev` → `main` only for releases. No direct commits to `main`.

**Conventional commits** (required for CHANGELOG generation):
```
feat: add offline download support
fix: fix token refresh on 401
chore: update kion dependencies
test: add streaming test
```

**Cover URI format:** API returns URIs with `%%` placeholder (e.g. `avatars.kion.net/get-music-content/xxx/yyy/%%`). Replace `%%` with the size string (`1000x1000`) to get the full URL — see `_get_image_url` in `parsers.py`.

**All Python files** include `from __future__ import annotations` at the top; type-only imports go inside `if TYPE_CHECKING:`.

**Port conflict:** Dev server and integration tests both use port 8095 (via the `mass` fixture). Run `pytest tests/ -m "not integration"` while the dev server is active.

**Package manager:** `uv` — use `uv run <cmd>` or activate the venv created by `./scripts/setup.sh`.
