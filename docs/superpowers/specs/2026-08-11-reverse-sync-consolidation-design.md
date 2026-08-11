# Reverse-Sync Consolidation Design

## Goal

Replace the ten stale or malformed reverse-sync pull requests with one coherent,
tested port based on the current `dev` branch, then retire the superseded drafts.

## Scope

The consolidation covers upstream Music Assistant pull requests 4793, 4487,
4946, 4948, 5017, 5053, 5058, 5370, 5430, and 5464. Existing KION-specific
streaming, library, browse, radio feedback, token, and quality behavior must be
preserved unless an upstream change explicitly replaces the corresponding
contract.

The work does not include unrelated refactoring of the large provider module,
new end-user features beyond those upstream changes, or changes to generated
repository policy and lint configuration.

## Chosen Approach

Port the upstream changes sequentially onto fresh `origin/dev`. Do not reuse the
literal conflict-marker patches from the draft PRs. For each upstream PR, compare
the upstream before/after diff with the current KION implementation and reproduce
only the intended behavior using the repository's current method ordering,
translation, setup-flow, and caching conventions.

This is preferred over either repairing every draft branch independently or
replacing the provider wholesale with the latest upstream copy. Independent
repair would repeatedly resolve the same overlapping regions, while wholesale
replacement would risk losing provider-repository changes that have not been
inlined upstream.

## Delivery Order

1. Refresh parser snapshots for the model serialization introduced by upstream
   PR 4793 and establish a green baseline.
2. Port lazy recommendation rows and Recently Played behavior from PR 4487.
3. Apply the recommendation cleanup, subtitles, and method-order follow-ups from
   PRs 4946 and 4948 as one compatible stage.
4. Move authentication into the interactive setup flow and expose only playback
   options through the provider options contract, incorporating PRs 5017, 5053,
   and 5058.
5. Add single-flight request sharing for ordinary uncached data, regular
   playlists, and My Mix/My Wave, applying the final behavior from PR 5464 over
   the intermediate opt-out introduced and narrowed by PRs 5370 and 5430.
6. Run full verification, complete one release-ready feature specification and
   changelog entry, and prepare one replacement PR.
7. After the replacement branch is published and its PR exists, close the ten
   superseded draft PRs with a short factual pointer to the replacement.

## Components and Contracts

### Recommendations

`get_recommendations()` returns descriptors without loading row contents.
`get_recommendation_items(item_id)` loads only the requested row. Mood and
activity labels remain stable while the selected tag is deterministic for the
same cache interval, so a row subtitle and its contents cannot disagree.
Recently Played continues to expose the provider's listening history without
eagerly fetching unrelated recommendation sources.

### Setup and Options

The setup flow collects and validates the OAuth token. Provider option entries
contain playback and transport settings only. Provider initialization reads the
setup value through the Music Assistant setup-value contract. Login failures use
the KION-specific translated token error. Existing configured instances must
remain loadable after migration.

### Request Sharing

Idempotent cached reads use Music Assistant's cache single-flight behavior so
concurrent requests for the same key share one provider call. Caching remains
split by playlist kind so regular, liked, and My Mix data keep independent cache
keys and lifetimes. My Mix/My Wave reads are shareable in the final state: the
provider-wide lock already serializes rotor state, and the one-shot
`radioStarted` feedback is independently guarded. Explicit cache bypasses still
perform their own fetches.

## Error Handling

Setup errors are returned through translated setup-flow errors without exposing
the token. Unsupported or empty recommendation rows return an empty collection.
Request-sharing changes must preserve the existing provider exceptions and may
not turn failed or cancelled fetches into cached successes.

## Testing

Every behavioral stage follows red-green-refactor TDD. Tests must exercise the
real provider methods, with mocks limited to the external KION API boundary and
Music Assistant cache/server infrastructure where unavoidable.

Required coverage includes:

- updated parser serialization snapshots;
- recommendation descriptors performing no backend I/O;
- per-row recommendation loading calling only its own backend sources;
- setup-flow token collection, retry, translated login failure, and options
  without authentication fields;
- concurrent regular playlist callers sharing one fetch;
- concurrent My Mix/My Wave callers sharing one fetch while preserving cursor
  and one-shot feedback behavior;
- pagination termination and cancellation/error behavior for shared requests.

Final verification consists of the full pytest suite, Ruff format and lint,
mypy, the repository's method-order and upstream parity hooks, and
`pre-commit run --all-files`.

## GitHub Transition

No existing draft PR is modified in place. The replacement PR targets `dev` and
contains the consolidated implementation, tests, completed specification,
changelog, and version change required by repository policy. Existing drafts are
closed only after the replacement PR URL exists, making the transition auditable
and reversible through Git history.
