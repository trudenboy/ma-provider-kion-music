# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.5] - 2026-07-16

- feat: reverse-port the unported upstream mass-migrations (May 22 – Jun 19, pre-dating the reverse-sync radar): browse/recommendation labels localized via server translations (`strings.json` `media.folder`, replacing the in-code `BROWSE_NAMES_RU/EN` dicts), common-string references (upstream #4327), the unofficial-integration disclaimer entry (upstream #4164), and `RateLimited` for the 429 path (was `ResourceTemporarilyUnavailable`). Provider tree now matches upstream's inlined copy modulo method order.

## [3.0.4] - 2026-07-16

- refactor(config): move every `ConfigEntry` label/description and all static `ConfigValueOption` titles into `provider/strings.json` (upstream `check_config_entries` compliance); `ConfigValueOption` calls are now value-only, the `base_url` description uses a `{0}` template with `translation_params`.
- fix: replace direct `datetime.now()` calls with `music_assistant.helpers.datetime.utc()` (upstream `check_datetime_helpers` compliance).
- style: ruff 0.15 safe autofixes matching the upstream dev lint rules.
- refactor: reorder class methods in `api_client.py` / `provider.py` / `streaming.py` — public methods first, private helpers last (pre-commit `check-method-order` compliance; pure moves, AST-verified no code change).
- fix(tests): refresh `test_parsers.ambr` snapshots for the current `music_assistant_models` (new `collections`, `description_language`, `proxy_id`, `translation_params` fields; `translation_key: None` no longer serialized).

## [3.0.3] - 2026-05-09

- fix(tests/snapshots): refresh `test_parsers.ambr` for the upstream `music_assistant_models` evolution — `Artist.artist_type` (new field, default `singer`) and the new `MediaItemMetadata` fields (`review`, `mood`, `style`, `lyrics`, `lrc_lyrics`, `performers`, `preview`, `popularity`, `release_date`).
- chore: sync workflow wrappers from ma-provider-tools (CLAUDE.md, ruff/mypy/codespell from upstream music-assistant/server, config-sync CI guard).

## [3.0.2] - 2026-04-28

- fix(api_client): strip base64 padding from the `/get-file-info` HMAC signature via
  `.rstrip("=")` instead of a fixed `[:-1]` slice, so the sign stays valid even if the
  padding length ever differs from one character.

## [3.0.1] - 2026-04-23

- fix(streaming): return `(MP4, FLAC)` / `(MP4, AAC)` for MP4-container codecs, matching the
  yandex_music provider convention so MA core treats flac-mp4/aac-mp4 as MP4 containers
  (correct mime type, seek handling, passthrough) rather than raw FLAC/AAC byte streams.
- fix(streaming): tighten `_select_best_quality` lossless detection to exact match on
  `{QUALITY_LOSSLESS, "lossless"}` — no longer matches arbitrary strings containing
  "lossless" (e.g. "lossless_foo").

## [3.0.0] - 2026-04-20

- Bump version from 2.6.7 to 3.0.0 (`5ecbed1`)
- feat: port functional improvements from PR #87 (keep manual-token auth) (#89) (`91f345f`)
  - Encrypted streaming via `/get-file-info` with HMAC-SHA256 signing + AES-CTR decryption
  - New `SIMILAR_ARTISTS` provider feature
  - Expanded `parse_artist` with description/popularity metadata
  - Browse additions: pinned items, listening history, wave landing/my-waves
  - Renamed `QUALITY_SUPERB` → `QUALITY_LOSSLESS` (legacy `"lossless"` still accepted)
  - Advanced settings: `CONF_TRANSPORT` (raw/encraw), `CONF_CODECS`
  - Typed v3 rotor feedback dispatch (radioStarted/trackStarted/trackFinished/skip)
- refactor: rename cosmetic Yandex references to Kion (`6ebc874`)
- feat: migrate to yandex-music v3 (`54f1119`)
- chore: sync workflow wrappers from ma-provider-tools (#86) (`f79a6a9`)
- chore: sync workflow wrappers from ma-provider-tools (#84) (`d983524`)
- chore: sync workflow wrappers from ma-provider-tools (#83) (`c74b7af`)
- chore: sync workflow wrappers from ma-provider-tools (#79) (`a17276c`)
- chore: sync workflow wrappers from ma-provider-tools (#76) (`740b812`)
- chore: add VERSION file (2.6.7) (`4ce884a`)
- chore: sync workflow wrappers from ma-provider-tools (#74) (`bbf078d`)
- chore: sync workflow wrappers from ma-provider-tools (#68) (`1023c16`)
- fix: catch BadRequestError in connect() for rejected tokens (`d36b51c`)
- fix: remove extra trailing newlines in docs-site content files (`b743be3`)
- fix: update playlist snapshots with is_dynamic field (`c5febd6`)
- fix: rename QUALITY_LOSSLESS to QUALITY_SUPERB for consistency (`0a9b89f`)
- chore: sync workflow wrappers from ma-provider-tools (#67) (`b873620`)
- fix: relax LRC timestamp regex to allow 1-2 digit minutes/seconds (`1db7a9f`)
- fix: address PR #3234 second wave of review comments (#65) (`bb99d0a`)
- fix: address PR #3234 second wave of review comments (`55ae177`)
- fix: address PR #3234 review comments (#64) (`67af90f`)
- fix: remove extra trailing newlines in docs-site content files (`12c33cf`)
- test: remove test_get_audio_stream_invalid_key_hex_raises_error (`d7e76ee`)
- feat(kion_music): sync branding from yandex_music v2.6.7 (#63) (`06d703e`)
- chore: sync workflow wrappers from ma-provider-tools (#62) (`6f15ab4`)
- chore: reformat CHANGELOG — use commit history instead of PR notes [skip ci] (`86afa5e`)
- chore: reformat CHANGELOG — marker to top, releases newest-first [skip ci] (`17ec51f`)
- chore: reformat CHANGELOG — marker to top, releases newest-first [skip ci] (`f7147e7`)
- fix: use asyncio.TimeoutError instead of built-in TimeoutError in get_audio_stream (`d797269`)
- fix: cast streaming stubs to KionMusicProvider to satisfy mypy (`9d6072b`)
- chore: update manifest to match yandex_music format (`5fd5e2a`)
- chore: update changelog for v2.6.7 [skip ci] (`fe06348`)

---

## [3.0.1] - 2026-04-23

- fix(streaming): treat MP4-container codecs as MP4+codec_type, tighten lossless match (`cc907b1`)
- fix: remove auto-enable of "Don't stop the music" from on_played/on_streamed (`6130ff5`)
- fix: always set track.metadata.lyrics so synced LRC isn't skipped by core (`55227cb`)
- docs: enrich 3.0.0 changelog with PR #89 functional highlights (`e08525a`)
- chore: update changelog for v3.0.0 [skip ci] (`8592859`)

---

## [3.0.2] - 2026-04-28

- fix(api_client): strip base64 sign padding via rstrip("=") (`428411b`)
- chore: update changelog for v3.0.1 [skip ci] (`92c34a3`)

---

## [3.0.3] - 2026-05-09

- chore: sync workflow wrappers from ma-provider-tools (#96) (`24d4f1e`)
- chore: sync workflow wrappers from ma-provider-tools (#94) (`ec42d4b`)
- chore: update changelog for v3.0.2 [skip ci] (`94a4342`)

---

<!-- changelog entries will be added here by release workflow -->

## [2.6.7] - 2026-02-27

- fix: resolve CI failures for PR #3234 (`563fecc`)
- test: update playlist snapshots for supported_mediatypes field (`be86030`)
- fix: address PR review comments (`446ff66`)
- fix: use rstrip('=') instead of [:-1] for HMAC base64 padding removal (`c41effb`)
- fix: resolve mypy failures in streaming tests (`316fe29`)
- fix: catch BadRequestError as LoginFailed in connect() (`993706d`)
- fix: change DEFAULT_BASE_URL to api.music.yandex.net (`edc9033`)
- chore: sync workflow wrappers from ma-provider-tools (#60) (`cdd79ed`)
- feat(kion_music): sync branding from yandex_music v2.6.7 (#61) (`e5c6348`)
- fix: resolve CI failures from branding sync (`38bc41a`)
- fix: update hardcoded music.mts.ru URLs in test_parsers.py (`6adfac2`)

---

## [2.6.5] - 2026-02-26

- feat(kion_music): sync branding from yandex_music v2.6.5 (#58) (`edd4323`)

---

## [2.6.4] - 2026-02-26

- Update manifest.json for KION Music service (`d7afce8`)
- feat(kion_music): sync branding from yandex_music v2.6.3 (#53) (`4df9ff5`)
- feat(kion_music): sync branding from yandex_music v2.6.3 (#54) (`a813ca9`)
- fix: update _get_content_type assertion to match tuple return type (`e738b74`)
- chore: remove unused type: ignore comments in test_streaming (`5af5f4d`)
- fix: use DEFAULT_BASE_URL when no base_url passed to KionMusicClient (`344f313`)
- fix: use Protocol for streaming provider type to fix mypy in MA server (`eb02a79`)
- feat(kion_music): sync branding from yandex_music v2.6.3 (#55) (`cabedd5`)
- chore: revert to baseline tests, fix api_client base_url default, add hass-client dep (`884f8da`)
- chore: remove .ma-data from tracking (`be49b2c`)
- fix: use Protocol for streaming provider type to fix mypy in MA server (`6556c9b`)
- test: remove flaky lossless fallback test with mypy attr issue (`c9cbca2`)
- test: remove integration tests (`21afb41`)
- fix: address PR review comments — quality match, lambda, LRC regex, HMAC strip, test coverage (`3e1bc6b`)
- test: remove lossless UI label test that fails with exact quality match (`7a27b69`)
- fix: wrap bytes.fromhex() in try/except for clearer AES key error, clarify backoff comment (`515d8f5`)
- docs: add Starlight package.json (`b74a30c`)
- docs: add Starlight tsconfig.json (`12a7f0d`)
- docs: add Starlight astro.config.mjs (`7e1d0af`)
- docs: add Starlight content.config.ts (`5c6215e`)
- docs: add Starlight index.md (`de64709`)
- docs: add Starlight known-issues.md (`f42b01b`)
- docs: add Starlight testing.md (`9e54853`)
- docs: add Starlight dev-docker.md (`355364a`)
- docs: add Starlight incident-management.md (`77face9`)
- docs: add configuration page (`9a56e53`)
- docs: add contributing page (`b5fd2c5`)
- ci: migrate docs to Astro Starlight (`e079de3`)
- chore: sync workflow wrappers from ma-provider-tools (#56) (`cf5a9c3`)
- chore: add package-lock.json for npm cache (`59f2a8f`)
- docs: add Starlight title frontmatter to contributing.md (`99f3355`)
- docs: add development.md (dev environment guide) (`36fdee3`)
- docs: add provider icon emblem to index page (`b8b19aa`)
- docs: add user documentation link to README (`fdd342b`)
- docs: обновить пользовательскую документацию (`d1b29ec`)
- docs: добавить плашки о неофициальном статусе и подписке (`d33fca4`)
- docs: заменить инструкцию по токену на метод через браузер (`89b4755`)
- docs: привести плашки к стилю yandex-music провайдера (`1bd2cdc`)
- docs: обновить плашку подписки по образцу yandex-music (`0ad35df`)
- docs: вернуть расширенный текст дисклеймера (`c25b8b4`)
- Update KION Music references in documentation (`7914ce6`)
- feat(kion_music): sync branding from yandex_music v2.6.4 (#57) (`ade94a2`)

---

## [2.6.2] - 2026-02-24

- feat(kion_music): sync branding from yandex_music v2.6.1 (#52) (`b6d6660`)

---

## [2.6.1] - 2026-02-24

- feat(kion_music): sync branding from yandex_music v2.6.1 (#48) (`e230836`)
- feat(kion_music): sync branding from yandex_music v2.6.1 (#49) (`2b9e880`)
- feat(kion_music): sync branding from yandex_music v2.6.1 (#50) (`a2fa87b`)
- feat(kion_music): sync branding from yandex_music v2.6.1 (#51) (`dcdf517`)

---

## [2.5.8] - 2026-02-24

- docs: extend DEVELOPMENT.md with day-to-day workflow, troubleshooting, E2E checklist (`17c9430`)
- fix: use setuptools.build_meta backend (compatible with setuptools<77) (`87912d7`)
- chore: sync workflow wrappers from ma-provider-tools (`5de1f1c`)
- chore: sync workflow wrappers from ma-provider-tools (`f42e650`)
- chore: sync workflow wrappers from ma-provider-tools (`80641f2`)
- chore: sync workflow wrappers from ma-provider-tools (`c186dbc`)
- chore: sync workflow wrappers from ma-provider-tools (`e7a1a41`)
- chore: sync workflow wrappers from ma-provider-tools (`c98701f`)
- chore: sync workflow wrappers from ma-provider-tools (`c5a7ea4`)
- chore: sync workflow wrappers from ma-provider-tools (`ae5cede`)
- docs: unify documentation structure (#9) (`3e5a49e`)
- chore: sync workflow wrappers from ma-provider-tools (#10) (`5766763`)
- chore: sync workflow wrappers from ma-provider-tools (#11) (`7a1ca0c`)
- chore: sync workflow wrappers from ma-provider-tools (#13) (`756cb4d`)
- chore: sync workflow wrappers from ma-provider-tools (#14) (`d091d45`)
- chore: sync workflow wrappers from ma-provider-tools (#15) (`fe5c54d`)
- chore: sync workflow wrappers from ma-provider-tools (#16) (`ce110bb`)
- Remove music-assistant-models dependency (`8fb7cb6`)
- chore: sync workflow wrappers from ma-provider-tools (#17) (`36b5847`)
- chore: sync workflow wrappers from ma-provider-tools (#18) (`b4ba322`)
- chore: sync workflow wrappers from ma-provider-tools (#19) (`8bdb1e0`)
- chore: sync workflow wrappers from ma-provider-tools (#21) (`3cb6926`)
- docs: add testing, incident-management, dev-docker links to README (#22) (`be5c27d`)
- fix: ensure docs files end with exactly one trailing newline (#23) (`5f62bc9`)
- chore: sync workflow wrappers from ma-provider-tools (#24) (`a56efde`)
- chore: sync workflow wrappers from ma-provider-tools (#25) (`90a199f`)
- chore: sync workflow wrappers from ma-provider-tools (#26) (`71d30b0`)
- chore: sync workflow wrappers from ma-provider-tools (#27) (`7e69313`)
- chore: sync workflow wrappers from ma-provider-tools (#28) (`b37cc9d`)
- chore: sync workflow wrappers from ma-provider-tools (#29) (`7d305c7`)
- docs: rewrite README in MSX style with Docker Quick Start, full features, references (`21ab140`)
- docs: rewrite README.ru in MSX style with Docker Quick Start, full features, references (`b089ae0`)
- chore: sync workflow wrappers from ma-provider-tools (#30) (`0135594`)
- chore: sync workflow wrappers from ma-provider-tools (#31) (`fe9cd88`)
- chore: sync workflow wrappers from ma-provider-tools (#32) (`165f3dd`)
- chore: sync workflow wrappers from ma-provider-tools (#33) (`07d101e`)
- chore: sync workflow wrappers from ma-provider-tools (#34) (`37e4238`)
- chore: set Russian README as default (#35) (`0a58cc4`)
- chore: sync workflow wrappers from ma-provider-tools (#36) (`e747f49`)
- chore: sync workflow wrappers from ma-provider-tools (#37) (`1f4cef4`)
- chore: sync workflow wrappers from ma-provider-tools (#38) (`e37cf76`)
- chore: sync workflow wrappers from ma-provider-tools (#39) (`eb2f2cd`)
- chore: sync workflow wrappers from ma-provider-tools (#40) (`a815a2c`)
- chore: sync workflow wrappers from ma-provider-tools (#41) (`73da6c2`)
- chore: sync workflow wrappers from ma-provider-tools (#42) (`52c7792`)
- chore: generate historical changelog [skip ci] (`09b240b`)
- docs: add pre-separation upstream PR history to CHANGELOG (`69b48c7`)
- chore: sync workflow wrappers from ma-provider-tools (#43) (`e203280`)
- feat(kion_music): sync branding from yandex_music v2.5.8 (#45) (`39ec2d1`)

---

## 2026-02-22

- chore: set Russian README as default (#35) (`0a58cc4`)
- docs: rewrite README.ru in MSX style with Docker Quick Start, full features, references (`b089ae0`)
- docs: rewrite README in MSX style with Docker Quick Start, full features, references (`21ab140`)

## 2026-02-21

- fix: ensure docs files end with exactly one trailing newline (#23) (`5f62bc9`)
- Remove music-assistant-models dependency (`8fb7cb6`)
- docs: unify documentation structure (#9) (`3e5a49e`)

## 2026-02-19

- feat: initial provider setup (`cdd1fbc`)


<!-- Pre-separation: development in trudenboy/ma-server monorepo -->
<!-- The following changes were developed in the `trudenboy/ma-server` monorepo before this provider was extracted into its own repository on 2026-02-19. -->

## 2026-02-17

- feat: add configurable My Mix settings and improvements (music-assistant/server#3145)

## 2026-02-10

- feat: provider accepted into upstream Music Assistant (music-assistant/server#3100)

## 2026-02-07

- fix: address PR review — fix base_url, performance, redundant condition, docstrings; add tests

## 2026-02-05

- feat: add KION Music (MTS Music) provider
- fix: fix playlist tracks not loading in UI
- fix: fix missing album cover art in library
- Reverse-synced upstream PR #4637 (WIP)
- Reverse-synced upstream PR #5053 (WIP)
