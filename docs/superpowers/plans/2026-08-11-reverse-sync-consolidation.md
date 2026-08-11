# Consolidated Reverse-Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace ten stale reverse-sync drafts with one tested KION Music port that matches the final upstream recommendation, setup-flow, and cache-sharing contracts.

**Architecture:** Port behavior from upstream merge commit `e7d50f8` onto fresh `origin/dev` without copying conflicted draft patches. Keep KION API parsing and radio behavior intact, split changes into independently reviewable commits, and exercise real provider methods with mocks only at external API and Music Assistant infrastructure boundaries.

**Tech Stack:** Python 3.12+, asyncio, pytest, pytest-snapshot, Ruff, mypy, pre-commit, Music Assistant provider APIs, yandex-music.

## Global Constraints

- Work only in `/tmp/ma-provider-kion-reverse-sync` on branch `codex/reverse-sync-consolidation`; the user's dirty checkout must remain unchanged.
- Use final upstream behavior from Music Assistant server merge commit `e7d50f8`; do not reuse conflict-marker patches from PRs 140, 143, 146, 148, 150, or 154.
- Preserve existing KION streaming, library, browse, radio feedback, token, quality, and exception behavior unless this plan explicitly changes it.
- Follow red-green-refactor for behavior changes and commit after every task.
- Keep one active specification under `specs/inprogress/` and remove all unfinished-template markers from specification and plan files.
- Do not modify `VERSION` or add the final changelog entry until review feedback on the replacement draft PR has been addressed.
- Do not close any superseded PR until the replacement draft PR URL exists.
- Do not modify generated lint or repository-policy configuration.

---

## File Map

- `specs/inprogress/0002-consolidated-reverse-sync.md`: active feature contract and acceptance criteria.
- `specs/done/0001-reverse-sync-pr4637.md`: completed historical record replacing the stale placeholder specification.
- `tests/__snapshots__/test_parsers.ambr`: model-serialization expectations.
- `tests/test_recommendations.py`: static recommendation rows, row isolation, and rotating subtitle behavior.
- `tests/test_config_entries.py`: provider options contract after authentication migration.
- `tests/test_setup_flow.py`: token collection, retry, and translated failure behavior.
- `tests/test_provider.py`: playlist cache boundaries, pagination, concurrency, failure, and cancellation behavior.
- `provider/provider.py`: recommendation API, provider options, setup-value lookup, and playlist cache dispatch.
- `provider/setup_flow.py`: interactive token setup loop.
- `provider/__init__.py`: provider bootstrap only; no options/auth form construction.
- `provider/constants.py`: removal of obsolete auth action constants.
- `provider/strings.json`: static row names and setup-flow translations.

### Task 1: Replace the Stale Specification with an Executable Contract

**Files:**
- Delete: `specs/inprogress/reverse-sync-pr4637.md`
- Create: `specs/done/0001-reverse-sync-pr4637.md`
- Create: `specs/inprogress/0002-consolidated-reverse-sync.md`

**Interfaces:**
- Consumes: repository feature-spec format from `specs/feature-spec.md` and the approved design in `docs/superpowers/specs/2026-08-11-reverse-sync-consolidation-design.md`.
- Produces: one completed historical specification and one size-L active specification whose acceptance criteria map directly to Tasks 2–6.

- [ ] **Step 1: Record the already-delivered historical change**

Create `specs/done/0001-reverse-sync-pr4637.md` with `id: "0001"`, title `Reverse-sync upstream PR 4637`, size `S`, status `done`, priority `P1`, and the historical scope proven by commit `76b0299`: two parser snapshots gained `audio_metadata: None`. State that no provider runtime code changed, cite `tests/__snapshots__/test_parsers.ambr` as acceptance evidence, and explain that the present Task 2 supersedes those expectations for the newer model schema.

- [ ] **Step 2: Write the consolidated active specification**

Create `specs/inprogress/0002-consolidated-reverse-sync.md` with size `L`, upstream PR references `4793`, `4487`, `4946`, `4948`, `5017`, `5053`, `5058`, `5370`, `5430`, and `5464`, plus these exact acceptance contracts:

```markdown
1. Recommendation descriptors return nine ordered rows without KION backend calls.
2. Loading one recommendation row invokes only that row's backend dependencies.
3. Setup owns the OAuth token; provider options contain only playback and transport settings.
4. Three concurrent requests for one regular playlist perform one backend fetch.
5. Three concurrent My Mix requests perform one backend fetch and one rotor advance.
6. Failed or cancelled shared fetches are not stored as successful cache values.
7. The full repository verification suite is green against current Music Assistant `dev`.
```

Include a Mermaid sequence diagram for recommendation descriptor/item calls and a data-ownership table that assigns token ownership to setup data and playback settings to provider config.

- [ ] **Step 3: Validate the specification files**

Run:

```bash
test "$(find specs/inprogress -maxdepth 1 -type f | wc -l)" -eq 1
bad_markers='TB''D|TO''DO|implement lat''er|fill in det''ails'
rg -n "$bad_markers" specs docs/superpowers
git diff --check
```

Expected: the file-count assertion succeeds, `rg` returns no matches, and `git diff --check` prints nothing.

- [ ] **Step 4: Commit**

```bash
git add specs/inprogress specs/done
git commit -m "docs: define consolidated reverse-sync specification"
```

### Task 2: Refresh Parser Serialization Snapshots

**Files:**
- Modify: `tests/__snapshots__/test_parsers.ambr`

**Interfaces:**
- Consumes: existing parser tests and the installed `music-assistant-models` serialization contract.
- Produces: snapshot expectations containing the current `audio_metadata` representation for both affected track cases.

- [ ] **Step 1: Demonstrate the two existing snapshot failures**

Run:

```bash
.venv/bin/pytest tests/test_parsers.py -q
```

Expected: exactly two track snapshot mismatches whose only semantic difference is `audio_metadata`; all other parser tests pass.

- [ ] **Step 2: Regenerate only parser snapshots**

Run:

```bash
.venv/bin/pytest tests/test_parsers.py --snapshot-update -q
git diff -- tests/__snapshots__/test_parsers.ambr
```

Expected: the test passes and the diff changes only the two affected serialized track snapshots.

- [ ] **Step 3: Verify the pinned-core baseline**

Run:

```bash
.venv/bin/pytest -q
```

Expected: `51 passed` with no failures.

- [ ] **Step 4: Commit**

```bash
git add tests/__snapshots__/test_parsers.ambr
git commit -m "test: refresh parser snapshots for audio metadata"
```

### Task 3: Load Recommendation Rows on Demand

**Files:**
- Create: `tests/test_recommendations.py`
- Modify: `provider/provider.py`
- Modify: `provider/strings.json`

**Interfaces:**
- Consumes: existing `_get_*_recommendations()` helpers, `MY_WAVE_PLAYLIST_ID`, provider cache, and `utc()`.
- Produces: `async get_recommendations() -> list[RecommendationFolder]`, `async get_recommendation_items(item_id: str) -> UniqueList[MediaItemType | ItemMapping | BrowseFolder]`, `async _rotating_row_tag_subtitle(category: str) -> str | None`, and `def _rotating_row_tag(category: str, valid_tags: list[str]) -> str`.

- [ ] **Step 1: Add the recommendation fixture and static-row test**

Create the provider fixture with mocked KION client methods and add:

```python
ROW_IDS = [
    MY_WAVE_PLAYLIST_ID,
    "feed",
    "chart",
    "new_releases",
    "new_playlists",
    "top_picks",
    "mood_mix",
    "activity_mix",
    "seasonal_mix",
]

@pytest.mark.asyncio
async def test_get_recommendations_returns_static_rows_without_backend_calls(
    provider: KionMusicProvider,
) -> None:
    result = await provider.get_recommendations()
    assert [folder.item_id for folder in result] == ROW_IDS
    assert _awaited_methods(cast("Mock", provider.client)) == set()
    assert all(not folder.items for folder in result)
```

- [ ] **Step 2: Run the static-row test and confirm the old API fails**

Run:

```bash
.venv/bin/pytest tests/test_recommendations.py::test_get_recommendations_returns_static_rows_without_backend_calls -q
```

Expected: failure because `KionMusicProvider` has no `get_recommendations` method.

- [ ] **Step 3: Implement the two-method recommendation dispatch**

Replace `recommendations()` with static descriptors in the exact `ROW_IDS` order and a dispatcher with these branches:

```python
async def get_recommendation_items(
    self, item_id: str
) -> UniqueList[MediaItemType | ItemMapping | BrowseFolder]:
    folder: RecommendationFolder | None = None
    if item_id == MY_WAVE_PLAYLIST_ID:
        folder = await self._get_my_wave_recommendations()
    elif item_id == "feed":
        folder = await self._get_feed_recommendations()
    elif item_id == "chart":
        folder = await self._get_chart_recommendations()
    elif item_id == "new_releases":
        folder = await self._get_new_releases_recommendations()
    elif item_id == "new_playlists":
        folder = await self._get_new_playlists_recommendations()
    elif item_id == "top_picks":
        folder = await self._get_top_picks_recommendations()
    elif item_id == "mood_mix":
        if tags := await self._get_valid_tags_for_category("mood"):
            folder = await self._get_mood_mix_recommendations(
                self._rotating_row_tag("mood", tags)
            )
    elif item_id == "activity_mix":
        if tags := await self._get_valid_tags_for_category("activity"):
            folder = await self._get_activity_mix_recommendations(
                self._rotating_row_tag("activity", tags)
            )
    elif item_id == "seasonal_mix":
        folder = await self._get_seasonal_mix_recommendations()
    return UniqueList() if folder is None else folder.items
```

Keep the existing helper signatures and return each folder's `.items`. Static descriptors may inspect only cached tag lists; they must not call the KION client.

- [ ] **Step 4: Add row-isolation and unknown-row tests**

Add the nine-row parameterization and unknown-row assertion:

```python
@pytest.mark.parametrize(
    ("item_id", "expected"),
    [
        (MY_WAVE_PLAYLIST_ID, {"get_my_wave_tracks"}),
        ("feed", {"get_feed"}),
        ("chart", {"get_chart"}),
        ("new_releases", {"get_new_releases", "get_albums"}),
        ("new_playlists", {"get_new_playlists", "get_playlists"}),
        ("top_picks", {"get_tag_playlists"}),
        ("mood_mix", {"get_landing_tags", "get_tag_playlists"}),
        ("activity_mix", {"get_landing_tags", "get_tag_playlists"}),
        ("seasonal_mix", {"get_tag_playlists"}),
    ],
)
async def test_get_recommendation_items_fetches_only_its_row(provider, item_id, expected):
    result = await provider.get_recommendation_items(item_id)
    assert _awaited_methods(cast("Mock", provider.client)) == expected
    assert result

async def test_unknown_recommendation_row_is_empty(provider):
    assert list(await provider.get_recommendation_items("unknown")) == []
    assert _awaited_methods(cast("Mock", provider.client)) == set()
```

Run both tests before implementation refinement; expected failures are extra backend calls, missing dispatch results, or both.

- [ ] **Step 5: Add deterministic subtitle tests**

Warm cache keys `_get_valid_tags_for_category.mood` and `_get_valid_tags_for_category.activity`, freeze `utc()` at `2026-07-24T12:30:00+00:00`, and assert:

```python
rows = {row.item_id: row for row in await provider.get_recommendations()}
tag = provider._rotating_row_tag("mood", ["chill", "focus"])
assert rows["mood_mix"].subtitle == tag.title()
await provider.get_recommendation_items("mood_mix")
cast("Mock", provider.client).get_tag_playlists.assert_awaited_with(tag)
```

Add a cold-cache test asserting mood and activity subtitles are `None` and no backend method was awaited.

- [ ] **Step 6: Implement hourly tag rotation and static translations**

Implement an index stable for category and UTC hour:

```python
def _rotating_row_tag(self, category: str, valid_tags: list[str]) -> str:
    hour_bucket = int(utc().timestamp()) // 3600
    seed = f"{self.instance_id}.{category}.{hour_bucket}".encode()
    return sorted(valid_tags)[zlib.crc32(seed) % len(valid_tags)]
```

`_rotating_row_tag_subtitle()` must read the validated-tag cache without populating it, return `None` on a cold cache, and title-case the selected tag. Remove `random` and `_pick_random_tag_for_category`. Change English translation values to `Mood Mix` and `Activity Mix`, while preserving translation keys.

- [ ] **Step 7: Verify recommendations and method order**

Run:

```bash
.venv/bin/pytest tests/test_recommendations.py -q
.venv/bin/ruff check provider/provider.py tests/test_recommendations.py
.venv/bin/ruff format --check provider/provider.py tests/test_recommendations.py
.venv/bin/python scripts/check_method_order.py
```

Expected: all commands pass. If the method-order script has a different checked-in CLI, run its documented invocation without modifying the script.

- [ ] **Step 8: Commit**

```bash
git add provider/provider.py provider/strings.json tests/test_recommendations.py
git commit -m "feat: load recommendation rows on demand"
```

### Task 4: Move Authentication into the Setup Flow

**Files:**
- Create: `provider/setup_flow.py`
- Create: `tests/test_config_entries.py`
- Create: `tests/test_setup_flow.py`
- Modify: `provider/__init__.py`
- Modify: `provider/provider.py`
- Modify: `provider/constants.py`
- Modify: `provider/strings.json`

**Interfaces:**
- Consumes: `SetupSession.form()`, `SetupSession.finish()`, `SetupFlowError`, `CONF_TOKEN`, and existing option `ConfigEntry` definitions.
- Produces: `async run_setup(session: SetupSession) -> None`; provider method `async get_config_entries() -> tuple[ConfigEntry, ...]`; initialization via `self.get_setup_value(CONF_TOKEN)`.

- [ ] **Step 1: Add failing options-surface tests**

Create `tests/test_config_entries.py` with:

```python
_AUTH_KEYS = frozenset({"token", "auth", "clear_auth"})

async def test_get_config_entries_has_no_auth_entries_or_actions() -> None:
    entries = await KionMusicProvider.get_config_entries(Mock(spec=KionMusicProvider))
    assert {entry.key for entry in entries}.isdisjoint(_AUTH_KEYS)
    assert not [entry for entry in entries if entry.action]

async def test_get_config_entries_keeps_genuine_options() -> None:
    entries = await KionMusicProvider.get_config_entries(Mock(spec=KionMusicProvider))
    assert {
        CONF_QUALITY, CONF_MY_WAVE_MAX_TRACKS, CONF_LIKED_TRACKS_MAX_TRACKS,
        CONF_TRANSPORT, CONF_CODECS, CONF_BASE_URL,
    } <= {entry.key for entry in entries}

async def test_get_config_entries_resolve_without_user_input() -> None:
    entries = await KionMusicProvider.get_config_entries(Mock(spec=KionMusicProvider))
    assert not [entry.key for entry in entries if entry.required and entry.default_value is None and entry.type not in UI_ONLY]
```

Run `.venv/bin/pytest tests/test_config_entries.py -q`; expected failure: the provider method is absent or auth entries remain.

- [ ] **Step 2: Add failing setup retry tests**

Use an `AsyncMock` session with `context.setup_data = {}`. The first test submits `{"token": "secret"}` and asserts `finish` receives it. The retry test uses:

```python
session.form = AsyncMock(side_effect=[{"token": "expired"}, {"token": "fresh"}])
session.finish = AsyncMock(
    side_effect=[SetupFlowError("invalid", translation_key="login_failed"), None]
)
await run_setup(session)
assert session.form.await_args_list[1].kwargs["errors"] == {"base": "login_failed"}
assert session.form.await_args_list[1].args[0][0].value == "expired"
assert session.finish.await_args_list[-1].args[0] == {"token": "fresh"}
```

Also assert that neither exception messages nor form errors contain either submitted token. Run `.venv/bin/pytest tests/test_setup_flow.py -q`; expected failure: `provider.setup_flow` does not exist.

- [ ] **Step 3: Implement the setup loop**

Create `provider/setup_flow.py`:

```python
_ENTRIES = (ConfigEntry(key=CONF_TOKEN, type=ConfigEntryType.SECURE_STRING, required=True),)

async def run_setup(session: SetupSession) -> None:
    errors: dict[str, str] | None = None
    setup_data = dict(session.context.setup_data)
    while True:
        entries = [replace(entry, value=setup_data.get(entry.key, entry.value)) for entry in _ENTRIES]
        submitted = await session.form(entries, step_id="user", errors=errors, last_step=True)
        setup_data.update(submitted)
        try:
            await session.finish(setup_data)
            return
        except SetupFlowError as err:
            errors = {"base": err.translation_key or str(err)}
```

- [ ] **Step 4: Move options and token ownership**

Move the six playback/transport entries from module-level `provider.__init__.get_config_entries()` to `KionMusicProvider.get_config_entries()`. Remove token/auth/clear-auth entries and actions. In `handle_async_init`, replace config token access with:

```python
token = self.get_setup_value(CONF_TOKEN)
```

Remove unused auth action constants and imports. Keep `setup()` and `SUPPORTED_FEATURES` in `provider/__init__.py`.

- [ ] **Step 5: Add setup-flow strings**

Match the current Music Assistant translation schema while retaining existing playback option translations:

```json
"setup_flow": {
  "user": {
    "title": "Connect to KION Music",
    "description": "Music Assistant needs your personal KION Music OAuth token to reach your account and library."
  }
},
"errors": {
  "login_failed": "Could not sign in to KION Music with this token. See the documentation for how to obtain a fresh OAuth token."
}
```

Remove obsolete `auth` and `clear_auth` action strings. Preserve the secure token label used by the setup entry if Music Assistant resolves it through `config_entries`.

- [ ] **Step 6: Verify setup and options**

Run:

```bash
.venv/bin/pytest tests/test_config_entries.py tests/test_setup_flow.py -q
.venv/bin/ruff check provider tests/test_config_entries.py tests/test_setup_flow.py
.venv/bin/ruff format --check provider tests/test_config_entries.py tests/test_setup_flow.py
```

Expected: all commands pass and the test output never displays token values.

- [ ] **Step 7: Rebuild the test environment against current Music Assistant dev**

Remove only the worktree-local `.venv`, recreate it from `pyproject.toml`, install the required test extras, and then replace the installed `music_assistant/providers/kion_music` directory with a symlink to this worktree's `provider` directory. Verify the symlink target before running tests. Do not install over the symlink, because that would overwrite source files.

Run:

```bash
site_dir=$(.venv/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
readlink -f "$site_dir/music_assistant/providers/kion_music"
.venv/bin/python -c 'from music_assistant.providers.kion_music.provider import KionMusicProvider; print(KionMusicProvider.__name__)'
```

Expected: the first command resolves to `/tmp/ma-provider-kion-reverse-sync/provider` and the import prints `KionMusicProvider`.

- [ ] **Step 8: Commit**

```bash
git add provider/__init__.py provider/setup_flow.py provider/provider.py provider/constants.py provider/strings.json tests/test_config_entries.py tests/test_setup_flow.py
git commit -m "feat: migrate token authentication to setup flow"
```

### Task 5: Split Playlist Caches and Share Concurrent Fetches

**Files:**
- Create: `tests/test_provider.py`
- Modify: `provider/provider.py`

**Interfaces:**
- Consumes: Music Assistant `use_cache`, provider cache infrastructure, `_get_my_wave_playlist_tracks(page)`, and `_get_liked_tracks_playlist_tracks(page)`.
- Produces: undecorated `get_playlist_tracks(prov_playlist_id: str, page: int = 0) -> list[Track]`; cached `_get_regular_playlist_tracks(prov_playlist_id: str, page: int) -> list[Track]`; independently cached My Mix and liked helpers.

- [ ] **Step 1: Add concurrent regular-playlist test**

Build a partial provider backed by `mass_minimal` cache and gate the client call:

```python
tasks = [asyncio.create_task(provider.get_playlist_tracks("12345:67")) for _ in range(3)]
await _wait_for_gated_fetch(lambda: mock_client.get_playlist.await_count > 0)
gate.set()
assert await asyncio.gather(*tasks) == [[], [], []]
assert mock_client.get_playlist.await_count == 1
```

Run `.venv/bin/pytest tests/test_provider.py::test_regular_playlist_fetch_is_shared_between_callers -q`; expected failure: backend await count is `3` or cache keys collide through the outer dispatcher.

- [ ] **Step 2: Add concurrent My Mix test**

Gate `get_my_wave_tracks`, start three `MY_WAVE_PLAYLIST_ID` calls, and assert three empty results with one backend await. Also assert `_my_wave_playlist_next_cursor` changes at most once and `_my_wave_radio_started_sent` does not produce duplicate feedback calls.

Run the single test; expected failure: backend await count is greater than `1` on the pre-port cache contract.

- [ ] **Step 3: Add pagination-boundary tests**

Parameterize regular, liked, and My Mix IDs with `page=1` and assert each returns `[]` without awaiting its backend method. This locks in the existing one-page provider contract before cache extraction.

- [ ] **Step 4: Split the dispatcher cache by playlist kind**

Remove `@use_cache` from `get_playlist_tracks`. Keep it as a pure dispatcher and move the existing regular-playlist body unchanged into:

```python
@use_cache(3600 * 3, allow_expired_cache=True)
async def _get_regular_playlist_tracks(
    self, prov_playlist_id: str, page: int
) -> list[Track]:
    ...
```

Apply the same decorator independently to `_get_my_wave_playlist_tracks(page)` and `_get_liked_tracks_playlist_tracks(page)`. Do not pass `single_flight=False`; final upstream behavior shares My Mix requests.

- [ ] **Step 5: Add failure and cancellation tests**

For failure, make `get_playlist` raise `RuntimeError("backend failed")`, gather three concurrent calls with `return_exceptions=True`, then replace the side effect with an empty playlist and call again. Assert all first results are `RuntimeError`, the retry succeeds, and the backend await count advances, proving no successful cache value was written.

For cancellation, cancel the first waiter after the shared fetch starts while leaving a second waiter active, release the gate, and assert the cancelled task raises `CancelledError`, the remaining waiter receives `[]`, and a later call returns `[]` without another backend fetch. These assertions verify provider integration with the current core's shared-task ownership rather than reimplementing it locally.

- [ ] **Step 6: Verify playlist behavior**

Run:

```bash
.venv/bin/pytest tests/test_provider.py -q
.venv/bin/pytest tests/test_streaming.py tests/test_provider.py -q
.venv/bin/ruff check provider/provider.py tests/test_provider.py
.venv/bin/ruff format --check provider/provider.py tests/test_provider.py
.venv/bin/python scripts/check_method_order.py
```

Expected: all tests and checks pass; both concurrency tests report one backend await.

- [ ] **Step 7: Commit**

```bash
git add provider/provider.py tests/test_provider.py
git commit -m "perf: share concurrent playlist track requests"
```

### Task 6: Verify the Consolidated Port and Record Evidence

**Files:**
- Modify: `specs/inprogress/0002-consolidated-reverse-sync.md`

**Interfaces:**
- Consumes: all production and test interfaces from Tasks 2–5.
- Produces: a fully verified branch and an active specification containing exact command evidence, ready for review and a replacement draft PR.

- [ ] **Step 1: Run focused behavioral suites**

Run:

```bash
.venv/bin/pytest tests/test_parsers.py tests/test_recommendations.py tests/test_config_entries.py tests/test_setup_flow.py tests/test_provider.py tests/test_streaming.py -q
```

Expected: all focused tests pass.

- [ ] **Step 2: Run the full test suite**

Run:

```bash
.venv/bin/pytest -q
```

Expected: all tests pass with no deselected regression tests and no snapshot updates pending.

- [ ] **Step 3: Run static and repository checks**

Run:

```bash
.venv/bin/ruff format --check .
.venv/bin/ruff check .
.venv/bin/mypy provider tests
.venv/bin/python scripts/check_method_order.py
.venv/bin/pre-commit run --all-files
git diff --check
```

Expected: every command exits zero. If repository scripts expose a checked-in wrapper or different documented arguments, use that exact checked-in invocation and record it in the specification.

- [ ] **Step 4: Scan for merge damage and release-policy violations**

Run:

```bash
rg -n '^(<{7}|={7}|>{7})' provider tests specs
git diff origin/dev...HEAD -- VERSION CHANGELOG.md uv.lock pyproject.toml
```

Expected: no conflict-marker matches and no version, changelog, lockfile, or dependency-manifest changes.

- [ ] **Step 5: Record verification evidence**

Append the exact command names, pass counts, and current Music Assistant commit to the specification's verification section. Mark each acceptance criterion as evidenced while keeping the specification under `specs/inprogress/` until PR review is complete.

- [ ] **Step 6: Commit the evidence**

```bash
git add specs/inprogress/0002-consolidated-reverse-sync.md
git commit -m "docs: record consolidated reverse-sync verification"
```

- [ ] **Step 7: Request final code review**

Use `superpowers:requesting-code-review` against `origin/dev...HEAD`. The reviewer must check acceptance-criterion coverage, upstream parity at `e7d50f8`, absence of unrelated KION behavior changes, and the prohibition on version/changelog changes before review feedback.

- [ ] **Step 8: Hand off to branch completion**

Use `superpowers:finishing-a-development-branch`. If the user selects publication, create one draft PR targeting `dev`; only after its URL exists, close PRs `139`, `140`, `142`, `143`, `146`, `148`, `150`, `152`, `154`, and `156` with a factual pointer to the replacement. Version bump, changelog entry, and moving the active spec to `specs/done/` remain post-review actions.
