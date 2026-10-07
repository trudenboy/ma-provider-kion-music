# Upstream PR #5585 readiness audit

Audited on 2026-10-07. [PR #5585](https://github.com/music-assistant/server/pull/5585)
head: `73d89a0503109917e733527b801365bab803dd18`. Recheck the head before publishing
or resolving anything. Local provider source is based on released v3.0.10,
commit `45c498d`, with the review fixes in this branch; VERSION stays 3.0.10.

## Current blockers

- Draft, `CHANGES_REQUESTED`, seven unresolved human review threads and a
  follow-up from MarvinSchenkel asking whether this PR is still being pursued.
- [Lint](https://github.com/music-assistant/server/actions/runs/37618391238/job/112782214288)
  fails with 20 mypy errors in `yandex_music` after installing the shared 3.2.0 library.
- [Tests](https://github.com/music-assistant/server/actions/runs/37618391238/job/112782319918)
  fail in eight Yandex tests whose fake clients lack the new `strict` attribute;
  18,766 tests passed, 24 skipped. KION did not fail in this run.
- `Dependency Security Review` remains pending despite the successful audit.
  [The reporting job](https://github.com/music-assistant/server/actions/runs/37618625864/job/112782973296)
  logged `No open PR found for head 73d89a0503109917e733527b801365bab803dd18`.
  A live call to the commits/{sha}/pulls endpoint also returned an empty list.
  The report workflow filters this association list and exits without updating
  the pending status. Upstream maintainers need to repair trusted PR lookup
  (for example, fall back to listing open PRs and match the exact head SHA and
  target branch), then rerun the report. Approval alone is not a remedy: the
  current approval command does not override a pending analysis status.

## Review dispositions (facts for the human author)

These are implementation facts, not messages to publish as answers to reviewers.
The substantive replies must be written by the contributor under the upstream AI policy.

| Discussion | Finding and prepared action |
| --- | --- |
| [3891031587](https://github.com/music-assistant/server/pull/5585#discussion_r3891031587) | Valid: get_tracks swallowed BadRequestError. It now raises ResourceTemporarilyUnavailable with the original cause. BadRequestError inherits NetworkError, so reconnect classification now explicitly excludes it. Real ClientAsync serialization with a patched HTTP boundary verifies the rejected request and absence of reconnect. |
| [3891159728](https://github.com/music-assistant/server/pull/5585#discussion_r3891159728) | Still needs action despite being marked outdated: current head removed omission protection altogether. Successful partial/empty responses now retain still-liked base IDs via public sync_run_state().skipped_item_ids, without fabricating InvalidDataError, incrementing failures or logging per-track warnings. Rejected requests abort listing separately. Tests use real track fixtures and scoped SyncRunState. No authenticated evidence establishes why KION omitted a particular track, so do not claim every omission is a licensing restriction. |
| [3891161528](https://github.com/music-assistant/server/pull/5585#discussion_r3891161528) | Shared-playlist failure regression now raises/asserts ResourceTemporarilyUnavailable instead of RuntimeError. |
| [3891163432](https://github.com/music-assistant/server/pull/5585#discussion_r3891163432) | Removed both redundant token-not-in-error-string assertions. Retained object identity, translation owner/arguments, retry token and successful finish assertions. |
| [3891186942](https://github.com/music-assistant/server/pull/5585#discussion_r3891186942) | Removed unused cache.get mocks and _cache_get_legacy; cache freshness/set behavior is still exercised. |
| [3891194950](https://github.com/music-assistant/server/pull/5585#discussion_r3891194950) | Removed the exact shared decorator argument assertion, including category=0. The test still verifies stale tags are returned promptly while a gated refresh starts and remains in flight. |
| [3891197342](https://github.com/music-assistant/server/pull/5585#discussion_r3891197342) | Removed the duplicate core migration test and import. KION options tests remain. No core migration implementation is changed. |

Additional self-review found liked-playlist browsing calling the sync-only failure
reporter. Restored its local debug log; a real invalid-artist fixture reproduces the
pollution of sync failures and skipped IDs before the fix.

## Shared dependency companion patch

`yandex-music-3.2-compat.patch` applies to the audited #5585 head. It changes only
five Yandex provider/test files: matching the shared library pin, list return typing, dictionary validation at the
existing HTTP boundary, DownloadInfo typing, and real disconnected ClientAsync
fixtures. It does not replace Yandex code with the much newer standalone provider.
The adjacent Yandex working tree is untouched. The Yandex manifest must also
pin `yandex-music[async]==3.2.0`: leaving its old 3.0.0 pin lets the real server's
`load_provider_module` installer request a downgrade when Yandex loads, despite
requirements_all.txt installing 3.2.0. Only KION and Yandex declare this library
in the audited source.

This patch is needed before upstream tests/lint can pass with the KION dependency
upgrade. It belongs in a human-reviewed upstream companion change, or can be applied
to the existing PR branch by the maintainer. It has not been pushed to upstream.
The KION-only sync workflow will not export this companion patch automatically.
The patch uses zero context to remain intact under whitespace hooks. On the exact
reviewed baseline, validate with `git apply --check --unidiff-zero <patch>` and apply
with `git apply --unidiff-zero <patch>`. Do not apply it to an unchecked different head.

## Validation

- Red then green: rejected ClientAsync track request; successful partial/empty
  library responses; liked-playlist browse pollution.
- KION suite: 91 tests, 7 snapshots.
- Exact PR head plus KION fixes and companion patch: 479 KION/Yandex tests,
  14 snapshots; mypy passes all 42 provider/test files.
- Ruff and provider pre-commit gates pass.
- Actual MA source from the audited upstream PR and yandex-music 3.2.0 were used.
  Supporting dependencies came from the existing project environment; this was
  not a fresh installation of all exact server pins. The full 18k server suite
  and authenticated KION playback have not been rerun locally.

## Remaining sequence

1. Human review and merge the provider fix PR, set VERSION to match prepared
   3.0.11 changelog, and let the release/sync workflow update #5585.
2. Include the reviewed Yandex compatibility companion change.
3. Fix/re-run the upstream dependency report lookup; obtain upstream dependency
   approval after successful analysis if required.
4. Rebase the description on the final full diff, using `pr-body.md` as the
   proposed replacement. Recheck source tag/head and CI before publication.
5. The contributor writes replies to OzGav and the follow-up from MarvinSchenkel,
   explaining the completed changes in their own words. Do not resolve human
   questions merely because their line became outdated.
6. Once the code and description have been reviewed by the contributor, mark
   ready for review and ask OzGav for a new review. Only upstream maintainers can
   provide the approval and merge; `CHANGES_REQUESTED` does not disappear when
   discussion threads are resolved.
