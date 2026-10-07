# Reverse-sync: upstream PR #6595

Ported from music-assistant/server#6595 via provider PR #188.

## Summary

Use Music Assistant request priorities instead of the removed throttler bypass.
An expired audio URL is refreshed at playback priority, with the caller's
priority restored even when the refresh fails. A request repeated after
reconnecting acquires its own throttler slot.

The snapshot conflict is resolved by applying the incoming changes to the
existing private methods, retaining their order and avoiding duplicate methods.
Snapshot compatibility changes from provider PRs #179 and #182 are included.

## Validation

The reconnect regression fails when the retry does not acquire another slot.
HTTP stream tests exercise a 403 response, playback-priority refresh, delivery
from the new URL, and priority restoration on both success and failure.
