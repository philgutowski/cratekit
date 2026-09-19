---
title: "An encrypted library can be built in the suite, so the key path needs no real snapshot"
date: 2026-09-18
category: integration-issues
module: src/cratekit/core/rb_writer.py
problem_type: integration_issue
component: database
severity: high
root_cause: untested_input_shape
resolution_type: code_fix
applies_when:
  - "A code path behaves differently on an encrypted rekordbox database than on a plain one"
  - "Every database the suite builds is plain SQLite, so a constant unlock answer passes every test"
  - "A mutation row on the encryption probe reads zero and the report blames a missing real snapshot"
symptoms:
  - "A verb passes its whole suite and fails at the open on every real library"
  - "open_db refuses with 'file is not a database' only when the key is withheld from an encrypted file"
  - "Mutating unlock_needed to answer 'not encrypted' kills zero tests"
related_components:
  - pyrekordbox
  - sqlcipher3
tags:
  - encryption
  - unlock
  - sqlcipher
  - fixture
  - r-239
---

# An encrypted library can be built in the suite, so the key path needs no real snapshot

## Context

A real rekordbox database is encrypted with SQLCipher. Every database this suite
built was plain SQLite, from `tests/test_rb_writer_db.py::_build_disposable_database`.
So `open_db(..., unlock=False)` passed every test and failed on every real
machine, and five verb sites shipped that way: `route inbox`, `route unplaced`,
`route pending`, `rebuild` and `converge`. U55 measured the gap and could not
close it. Its two mutation rows on the probe read zero, and the report said
only `CRATEKIT_TEST_DB` pointing at a real snapshot could give them an input.
The live database is off limits, so the gap sat open.

## What was not where it looked

The input did not need a real machine. `sqlcipher3` is already installed, since
pyrekordbox requires it through `sqlcipher3-wheels`, and the key the binding
unlocks with is its own default, `pyrekordbox.utils.deobfuscate(BLOB)`. Encrypting
the synthetic database with that key gives a file the binding opens exactly when
asked to unlock it:

```python
from pyrekordbox.db6.database import BLOB
from pyrekordbox.utils import deobfuscate
from sqlcipher3 import dbapi2

key = deobfuscate(BLOB)
conn = dbapi2.connect(str(plain_path))          # no key: reads the plain file
conn.execute(f"ATTACH DATABASE '{enc}' AS encrypted KEY '{key}'")
conn.execute("SELECT sqlcipher_export('encrypted')")
```

The helper is `tests/test_rb_writer_db.py::_encrypt_in_place`. Two traps are
handled inside it. First, fold the plain file out of WAL before exporting. If
you don't, the plain file's `-wal` and `-shm` sidecars survive the swap and sit
beside a file they were never written for. That was avoided rather than driven.
Second, put the encrypted copy back into WAL under its key, since that is the
mode the real database runs in.

Encrypt AFTER any setup that writes through plain `sqlite3`, such as
`_record_locations` in `tests/test_routing_workers.py`. Plain `sqlite3` cannot
read the encrypted file.

## Prove the fixture, not only the fix

A test that opens the encrypted copy successfully proves nothing if the copy was
never encrypted. `test_an_encrypted_database_does_not_open_with_the_key_withheld`
asserts the opposite direction: `open_db(path, unlock=False)` must refuse. Keep
that test with any new use of the helper.

## The fix this enabled

`open_db` and `integrity_ok` default `unlock` to `None`, which asks
`unlock_needed(target)` just before the binding is constructed. No caller in
`src` names an answer, and
`test_no_caller_in_src_answers_the_key_question_for_itself` refuses one by
walking the source. A test that patches `rb_writer.integrity_ok` to
`unlock=False`, as several write suites still do, will refuse an encrypted
capture. Drop the patch in any file that drives an encrypted library.

## What it still does not prove

The key and schema are the binding's and this suite's, not a real machine's. A
real library's cipher settings and schema version are still measured only by
`CRATEKIT_TEST_DB` against a supplied snapshot, which stays attended.
