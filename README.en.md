# KION Music Provider for Music Assistant

[English](README.en.md) | Русский

> Stream your [KION Music](https://music.kion.ru/) library through [Music Assistant](https://music-assistant.io/) with browse, search, radio, and lossless playback support.

## Quick Start (Docker)

```bash
# Clone the repo
git clone https://github.com/trudenboy/ma-provider-kion-music.git
cd ma-provider-kion-music

# Start Music Assistant with the provider pre-loaded
docker compose -f docker-compose.dev.yml up
```

Open the MA web UI at `http://localhost:8095`, then go to **Settings → Music Sources → Add Source → KION Music** and enter your OAuth token.

For the full Docker dev environment guide see [docs/dev-docker.md](docs/dev-docker.md).

## Features

- **Library sync** — Artists, Albums, Tracks (Liked), Playlists synced to MA library
- **Library editing** — Like / unlike Artists, Albums, Tracks directly from MA
- **Browse** — Liked Tracks, My Mix radio, Artists, Albums, Playlists
- **Recommendations** — My Mix surfaced as a MA recommendation folder
- **Search** — Tracks, Artists, Albums, Playlists
- **Similar tracks** — powered by KION rotor station
- **Audio quality** — High (MP3 320 kbps) / Lossless (FLAC)

## Documentation

| Guide | Description |
|-------|-------------|
| [Configuration](docs/configuration.md) | Token, quality settings |
| [Development](docs/development.md) | Dev setup, tests, linting, commit format |
| [Contributing](docs/contributing.md) | Bug reports, feature requests, pull requests |
| [Testing](docs/testing.md) | Running tests locally, CI pipeline, coverage |
| [Incident Management](docs/incident-management.md) | Labels, automated issue tracking, Copilot triage |
| [Docker Dev Environment](docs/dev-docker.md) | Run MA + provider locally without dependencies |

## References

- [Music Assistant](https://music-assistant.io/) — open-source music server by Marcel van der Veldt
- [KION Music](https://music.kion.ru/) — streaming service by MTS
- [yandex-music](https://github.com/MarshalX/yandex-music-api) — unofficial Python client by MarshalX

## License

[Apache 2.0](LICENSE) — see [CHANGELOG.md](CHANGELOG.md) for version history.
