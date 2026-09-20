---
title: monkeypatch.undo inside a test rolls back the autouse fixtures too
date: 2026-09-20
category: workflow-issues
module: tests/conftest.py
problem_type: testing_gap
component: testing_framework
severity: high
root_cause: shared_fixture_scope
resolution_type: test_fix
applies_when:
  - A test patches something, drives the failure it is about, and then wants the
    patch gone so the assertions afterwards can read the real thing back
  - The test reaches for monkeypatch.undo to get there
  - The suite's isolation, state roots, a fake keychain, a blocked library path,
    comes from autouse fixtures that take the same monkeypatch fixture
tags:
  - monkeypatch
  - autouse
  - test-isolation
  - keychain
  - state-roots
  - false-pass
  - real-machine
---

# monkeypatch.undo inside a test rolls back the autouse fixtures too

## Context

`tests/conftest.py` isolates every test through autouse fixtures that take the
function scoped `monkeypatch`: `_isolate_state_roots` points installation state
at a temp tree, another stands a fake keyring up, another blocks the real
library paths. None of that is visible from inside a test. It just is.

A test for the credential presence index needed a read that fails and then, after
the refusal, needed to read the index file back to prove nothing had been
rewritten. The patch was on `Path.read_text`, so reading the file back meant
getting the patch out of the way first. `monkeypatch.undo()` looks like the tool
for it.

## What actually happens

`monkeypatch` is ONE function scoped fixture instance shared by every fixture and
by the test body. `undo()` takes no argument and reverts EVERY patch recorded on
it, in reverse order, including the ones the autouse fixtures set before the test
body started running. From that line to the end of the test, the test is running
against the real machine.

It does not error, and it does not obviously fail. It failed like this:

```
assert secrets.recorded() == frozenset({secrets.Credential.IDENTIFY_KEY.value})
E   AssertionError: assert frozenset({'identify-key', 'identify-signing-key',
E       'provider-session'}) == frozenset({'identify-key'})
```

That is this developer's own installation state directory, read by a test that
believed it was looking at a temp tree it had written two lines earlier. The
companion assertion was worse: `secrets.get(...)` after the undo returned a real
value out of the real macOS keychain, and the failure message printed it.

Nothing was written, because the write half had already refused. A test whose
arrangement ends in a write rather than a refusal would have written.

## Guidance

Never call `monkeypatch.undo()` inside a test body in this repository. There is
no supported way to undo one patch, so build the patch with its own off switch
and flip that:

```python
def _unreadable_index(monkeypatch, path):
    real = Path.read_text
    armed = True

    def refuse(self, *args, **kwargs):
        if armed and self == path:
            raise PermissionError(13, "Permission denied", str(path))
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refuse)

    def disarm():
        nonlocal armed
        armed = False

    return disarm
```

The patch stays installed for pytest to tear down at the end of the test, which
is where it belongs, and the test controls only its own behaviour. `tests/test_config.py`
uses this for the five presence index tests that read the file back after a
refusal.

Two shapes make this worth a rule rather than a note. The autouse isolation is
invisible from the test, so nothing at the call site suggests `undo()` is
reaching outside the test's own arrangement. And the failure it produces reads as
a bug in the code under test, since the assertion is about product state and the
product state it compares against is real.
