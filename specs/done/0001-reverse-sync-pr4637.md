---
id: "0001"
title: "Reverse-sync upstream PR 4637"
size: S
status: done
priority: P1
effort_minutes: 5
---

## Problem Statement

Parser snapshots did not include the `audio_metadata` field added to serialized
Music Assistant tracks, so the provider's expectations no longer described the
model output used by upstream PR 4637.

## Solution Summary

Commit `76b0299` reverse-synced upstream PR 4637 by adding
`audio_metadata: None` to the two affected track snapshots. No provider runtime
code changed. Newer model output supersedes these exact expectations in
specification 0002.

## Acceptance Criteria

1. The minimal-track snapshot contains an `audio_metadata` field.
2. The track-with-artist-and-album snapshot contains an `audio_metadata` field.
3. Both new fields serialize as `None` for the fixtures used at merge time.
4. No provider runtime file changes as part of this reverse-sync.
5. The historical change remains traceable to upstream PR 4637 and commit
   `76b0299`.

## Test Plan

- Run `pytest tests/test_parsers.py` against the model version used by commit
  `76b0299` and verify both updated snapshots match.
- Inspect `tests/__snapshots__/test_parsers.ambr` and verify the only additions
  in that commit are the two `audio_metadata: None` fields.

