# Reverse-sync: upstream PR #6382

Ported from music-assistant/server#6382 via provider PR #184.

## Summary

Preserve the complete SetupFlowError when sign-in fails so the setup engine can
resolve its translation owner and positional arguments on the retry form.
Previously the provider reduced the error to a bare translation key or string.

## Validation

The setup-flow regression checks that the retry receives the original error,
including its translation owner and arguments, while retaining the submitted
value for correction. The regression fails with the old string conversion.
