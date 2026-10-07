# What does this implement/fix?

Fix KION library sync when a successful track batch omits still-liked tracks,
and upgrade the runtime dependency from yandex-music 3.0.0 to
`yandex-music[async]==3.2.0`.

A successful partial or empty response preserves omitted liked IDs for the
sync deletion pass, without reporting each unavailable item as a failure.
A rejected batch raises ResourceTemporarilyUnavailable and aborts listing instead
of returning a fabricated empty response. Rejected requests do not trigger reconnect.
Liked-playlist browsing keeps its local parse-error log without changing library sync state.

The full diff also places private provider/client/streaming methods after public
methods, removes the corresponding lint baseline exceptions, and adapts request
return values and quality-selection typing to the library's published annotations.
Existing signed KION requests, streaming quality selection, Range requests and
encrypted streaming remain in place.

Tests cover setup token collection and localized error propagation, concurrent
playlist fetches, cancellation and retry, stale recommendation tags during refresh,
real library feedback serialization, streaming URL refresh, and library omission
protection. Redundant decorator assertions, dead cache mocks and the duplicated
core migration test have been removed. Lazy recommendations and the setup flow
already exist on upstream dev; this PR adds coverage rather than introducing them.

Source: [ma-provider-kion-music](https://github.com/trudenboy/ma-provider-kion-music).
The existing PR imports release v3.0.10; the additional library sync fixes are
prepared for v3.0.11. Update this provenance sentence to the final synced release
and commit before publication. The Yandex compatibility companion aligns its manifest to the same library pin
and updates its typing and deserialization fixtures, because both providers share
the installed package. Include that change before publishing this description.

Changelog:
- Upgrade the Yandex Music library to 3.2.0 with its async dependencies.
- Preserve still-liked tracks omitted from successful batch responses without
  repeated warnings, and abort rejected requests separately.
- Keep playlist browsing errors separate from library sync failure reports.

Validation: 479 KION/Yandex tests and 14 snapshots pass on the audited PR head
with the prepared changes; mypy passes 42 provider/test files. These are local
results using existing supporting dependencies. Current upstream CI remains
blocked until the fixes and shared dependency companion are published and checked.
Authenticated KION playback has not been retested.

**Related issue (if applicable):**

Review feedback on #5585.

## Types of changes

- [x] Bugfix (non-breaking change which fixes an issue) — `bugfix`
- [ ] New feature (non-breaking change which adds functionality) — `new-feature`
- [ ] Enhancement to an existing feature — `enhancement`
- [ ] New music/player/metadata/plugin provider — `new-provider`
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected) — `breaking-change`
- [x] Refactor (no behaviour change) — `refactor`
- [ ] Documentation only — `documentation`
- [ ] Maintenance / chore — `maintenance`
- [ ] CI / workflow change — `ci`
- [x] Dependencies bump — `dependencies`

## Checklist

- [x] The code change is tested and works locally.
- [x] `pre-commit run --all-files` passes in the provider repository.
- [x] `pytest` passes for the affected provider suites, and tests have been added/updated.
- [ ] For changes to shared models, the companion PR in `music-assistant/models` is linked.
- [ ] For changes affecting the UI, the companion PR in `music-assistant/frontend` is linked.
- [ ] I have read and complied with the project's [AI Policy](https://github.com/music-assistant/.github/blob/main/AI_POLICY.md) for any AI-assisted contributions.
