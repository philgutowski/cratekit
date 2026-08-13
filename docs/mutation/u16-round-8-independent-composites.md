# Mutation table: u16-round-8-independent-composites

Measured by `scripts/mutate.py` on 2026-08-13 23:18 UTC, branch `unit/u16-three-state-match-and-missing-review` at `3262bc8`. Pass kind: light.

Baseline: green, 3512 collected. pytest invocations for this batch: 8.

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Null control `NULL_CONTROL`: killed 0, collected 3512 against 3512. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `V23_suppressed_message_reworded` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 3512 | 0 (promoted) | zero |
| `V23c_suppression_code_reworded` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 3512 | 0 (promoted) | zero |
| `V24_approximate_limit_raised` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 330 | 4 | killed |

## Zero rows and what they owe

- `V23_suppressed_message_reworded` (user facing): paired with `V23c_suppression_code_reworded`, which killed 0
- `V23c_suppression_code_reworded` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `V23_suppressed_message_reworded`

The suppression warning message reworded, not appended, to check the sentence is pinned rather than a substring; rerun of the first batch's zero row as the pairs_with anchor

- File: `src/cratekit/acquire/match_cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match_cli
- Ran: `tests/test_match_states.py`
- Collected: 3512 against a baseline of 3512
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    f"{track.wanted.artist} / {track.wanted.title} is suppressed by "
                    f"a tombstone and was not counted missing"

```

New text:

```
                    f"{track.wanted.artist} / {track.wanted.title} was skipped "
                    f"because a tombstone stands over it"

```

### `V23c_suppression_code_reworded`

Composite for V23_suppressed_message_reworded: reword the machine-readable warning CODE the sentence rides on, showing what the warning envelope does hold while the sentence wording holds nothing

- File: `src/cratekit/acquire/match_cli.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match_cli
- Ran: `tests/test_match_states.py`
- Collected: 3512 against a baseline of 3512
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite
- Composite for: `V23_suppressed_message_reworded`

Old text:

```
SUPPRESSED_WARNING = "acquisition-suppressed"

```

New text:

```
SUPPRESSED_WARNING = "suppressed-by-tombstone"

```

### `V24_approximate_limit_raised`

APPROXIMATE_LIMIT coefficient raised from 5 to 10; every test referencing it compares against match.APPROXIMATE_LIMIT itself, so the hunt predicts the value can drift green

- File: `src/cratekit/acquire/match.py`
- Surface: user
- Subset: test files importing cratekit.acquire.match
- Ran: `tests/test_match_states.py`
- Collected: 330 against a baseline of 330
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`

Old text:

```
APPROXIMATE_LIMIT = 5

```

New text:

```
APPROXIMATE_LIMIT = 10

```

