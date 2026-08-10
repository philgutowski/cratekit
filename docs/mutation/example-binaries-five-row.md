# Mutation table: example-binaries-five-row

Measured by `scripts/mutate.py` on 2026-08-10 16:43 UTC, branch `tooling/mutation-driver` at `81e0744`. Pass kind: light.

Baseline: green, 3483 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3483 against 3483. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `B1_broken_override_falls_through` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `B2_resolve_refuses_a_broken_override` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `B3_platform_binary_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `B4_unknown_source_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `B5_credential_strip` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |

## Considered and dropped

METHOD caps a light pass at 25 rows. These were ranked below the cap and NOT measured. They are not coverage.

- `B6_fallback_dirs_order`: Reorder fallback_dirs() so PATH wins over the override. Dropped because: ranked below the cap: same guard family as B1, which is measured

## Row definitions

### `B1_broken_override_falls_through`

find() returns a broken per-binary override as if it worked, instead of None. The guard exists so a set-but-broken override never falls through to a different binary.

- File: `src/cratekit/core/binaries.py`
- Surface: user
- Subset: test files importing cratekit.core.binaries
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_find_never_raises_because_doctor_reports_on_all_of_them`

Old text:

```
        return override if _executable(Path(override)) else None

```

New text:

```
        return override

```

### `B2_resolve_refuses_a_broken_override`

Delete resolve()'s explicit refusal for a set-but-broken override, so it falls through to the generic not-found path with the wrong remedy.

- File: `src/cratekit/core/binaries.py`
- Surface: user
- Subset: test files importing cratekit.core.binaries
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
    if override and not _executable(Path(override)):
        raise BinaryNotFound(
            f"{env_var(name)} is set to {override!r}, which is not an executable "
            f"file. Fix or unset the override; falling through to PATH would run "
            f"a different binary than the one you named.",
            binary=name,
            remedy=Remedy.FIX_BINARY_OVERRIDE,
        )

```

New text:

```
(empty)
```

### `B3_platform_binary_remedy`

A platform-provided binary reports INSTALL_BINARY instead of UNSUPPORTED_PLATFORM, so the CLI would tell a user to install something the operating system ships.

- File: `src/cratekit/core/binaries.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.binaries
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
            remedy=Remedy.UNSUPPORTED_PLATFORM,

```

New text:

```
            remedy=Remedy.INSTALL_BINARY,

```

### `B4_unknown_source_remedy`

Collapse the two None-hint cases onto one remedy token, which is the exact distinction the docstring says must not live in a None-check on a second attribute.

- File: `src/cratekit/core/binaries.py`
- Surface: maintainer
- Subset: test files importing cratekit.core.binaries
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,

```

New text:

```
        remedy=Remedy.INSTALL_BINARY,

```

### `B5_credential_strip`

subprocess_env() stops stripping Cratekit credentials, so every spawned third-party binary receives a copy and the credential reaches a process listing.

- File: `src/cratekit/core/binaries.py`
- Surface: user
- Subset: test files importing cratekit.core.binaries
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_a_spawned_process_does_not_inherit_an_opted_in_credential`

Old text:

```
        if not key.startswith(secrets.ENV_CREDENTIAL_PREFIX)

```

New text:

```
        if True

```

