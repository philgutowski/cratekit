# U34 mutation tables

Two mutation tables were lost during this unit by living only in a chat
transcript. This file exists so the next one is not, and so a later reader can
tell a guard that is held from a guard that merely looks held.

Every row is one revert applied ALONE to the shipped file, followed by the suite,
followed by a restore verified against a checksum. A row's number is the count of
FAILING TESTS, which pytest already counts one parametrized case at a time.

## Round 5

Sixty eight rows, every one of them a guard, constant, condition or assertion
this round adds or changes, plus eight of round four's re-run against the new
code. **No row killed zero.** Four rows measured zero on the first pass and each
one was FIXED rather than argued: three by writing the driver the guard was
missing, one by deleting a line that was genuinely inert.

Counts were measured scoped to `tests/modules/test_reports.py`, which nothing
else in the suite imports. Three rows were re-measured against the whole `tests`
tree to check the scoping: M35 gave 13 both ways, N05 gave 15 both ways, N21 gave
64 both ways.

Baseline before the round: 3349 passed, 15 skipped, 3364 collected.
Baseline after: 3397 passed, 15 skipped, 3412 collected.

### The scope fix, which is the round

| id | what was reverted | deaths |
|-|-|-|
| S01 | `_names_taken` reverted to PARAMETERS ONLY, which is the flat table round four shipped: only a parameter can take a name back | 11 |
| S02 | `_bound_here` stops reading a plain ASSIGNMENT target | 3 |
| S03 | `_bound_here` stops reading an AUGMENTED assignment, an ANNOTATED assignment and a WALRUS target | 1 |
| S04 | `_bound_here` stops reading a LOOP or COMPREHENSION target | 2 |
| S05 | `_bound_here` stops reading a WITH target | 1 |
| S06 | `_bound_here` stops reading an EXCEPT target | 1 |
| S07 | `_bound_here` stops reading an IMPORT as a binding, so an import of something else under the same name no longer takes the name | 1 |
| S08 | `_bound_here` stops reading a CLASS definition as a binding | 1 |
| S09 | `_bound_here` stops reading a PARAMETER LIST, which is the one shadow round four already had | 7 |
| X11 | `_bound_here` drops VARARG and KWARG from the parameter list | 2 |
| X12 | `_bound_here` drops KEYWORD ONLY parameters | 1 |
| S10 | `_target_names` stops UNPACKING a tuple or list target | 2 |
| S11 | `_target_names` stops unwrapping a STARRED target | 1 |
| S13 | `_names_taken` stops taking back a NESTED DEFINITION's own name | 1 |
| S21 | `_scope_own_bindings` stops recording a FAILED attempt for a binding `_binds` cannot read, so an import beats a `with`, an `except`, a class and an augmented assignment in the same scope | 1 |
| S22 | `_scope_own_bindings` stops recording a failed attempt for a nested DEFINITION | 1 |
| S14 | `_scope_own_bindings` accepts a name when ANY binding of it resolves rather than when EVERY binding agrees | 3 |
| S15 | `_scope_own_bindings` inner fixed point cut to ONE pass | 4 |
| S16 | `_visible_bindings` adds the scope's own bindings BEFORE shadowing instead of after, so a scope's own alias is shadowed by its own name | 19 |
| S17 | COMPREHENSIONS dropped from `_SCOPES`, so a comprehension target is read in the enclosing scope | 1 |
| S18 | `_walk_bindings` stops carrying OBJECT bindings out of the scope that made them | 3 |
| S19 | `_walk_bindings` stops recording a function's RETURNED module | 2 |
| S20 | `_writer_bindings` outer fixed point cut to ONE pass | 1 |

### The three misses, and the branch that was dead

| id | what was reverted | deaths |
|-|-|-|
| B01 | THE DEAD BRANCH. `_assigned` stops reading a PARALLEL UNPACKING element by element, which is what the branch it replaced looked like it did and never did | 1 |
| B03 | `_bound_module` stops reading a CONDITIONAL expression | 1 |
| B04 | `_bound_module` stops reading a BOOLEAN expression | 1 |
| B05 | `_element_bindings` stops RECURSING into a nested container literal | 1 |
| X13 | `_elements` drops the CONSTANT KEY condition on a dict literal | 1 |
| X16 | `_receiver_key` drops the KEYWORD ARGUMENT condition, so two different calls share one binding | 1 |
| X16b | `_receiver_key` drops the POSITIONAL ARGUMENT condition, the other half of the same identity | 1 |

### Rule 5, with the receiver it shipped without

| id | what was reverted | deaths |
|-|-|-|
| B06 | RULE 5 WITHOUT ITS RECEIVER, which is what round four shipped: every constant subscript compared against the mutation set | 4 |
| B07 | `_namespace_owner` stops recognising `__dict__` | 2 |
| B08 | `_namespace_owner` stops recognising `vars()` | 1 |
| N23 | CONFIRM ROUND 4 N23: rule 5, the namespace subscript, removed outright | 3 |

### The reflection switch, decided on the binding table

| id | what was reverted | deaths |
|-|-|-|
| C01 | `_called_keys` answers nothing, so no reflective read bound to a name is ever seen to be called | 8 |
| C02 | `_invoked_results` answers nothing, so a read RETURNED and then called is not read as called | 1 |
| C03 | `_invoked_reads` stops reading a DECORATOR as a call of its expression | 1 |
| C04 | `_invoked_reads` stops reading a read STORED IN A CONTAINER whose element is called | 1 |
| C05 | `_invoked_reads` stops reading a read BOUND TO A NAME the file calls | 6 |
| C06 | `_invoked_reads` stops reading a read handed to a FACTORY invoked on the spot | 1 |
| C07 | `_invoked_reads` stops reading a read in a CONTAINER LITERAL subscripted and called in place | 1 |
| C08 | `_invoked_reads` stops reading a read RETURNED by a function whose result is called | 3 |
| C09 | `_invoked_reads` stops reading the INLINE spelling, which is the only one round four had | 5 |
| C10 | `_handed_over` stops reading through a CONDITIONAL | 1 |
| C11 | `_reflective_call` stops recognising the ATTRIBUTE spelling, so the bound and unbound dunder are not reflective reads | 2 |
| C12 | `_stored` stops reading an ANNOTATED assignment and a WALRUS as a store | 2 |
| C13 | `_called_keys` stops reading a DECORATOR as a call | 2 |
| C14 | `mutations_in` stops handing INVOKED down into a nested scope, so each scope decides the switch on itself again | 2 |
| C15 | `mutations_in` stops handing LIBRARIES down into a nested scope, so a nested function loses the file's imports | 1 |
| C16 | the audit computes INVOKED from one top level statement instead of from the whole module | 2 |
| C17 | the audit computes LIBRARIES from one top level statement instead of from the whole module | 1 |
| B09 | THE DUNDER. a computed `__getattribute__` is gated on the reflection switch again instead of on its result being called | 1 |
| N26 | CONFIRM ROUND 4 N26: the computed half fires only when the reflection switch is on, never on the result being called | 18 |

### `open`, which was reading the file as the mode

| id | what was reverted | deaths |
|-|-|-|
| B10 | `_library_receiver` always answers `""`, so every module level `open` is read as a bound `Path.open` | 1 |
| B11 | `_imported_modules` answers nothing, so no receiver is ever a module | 1 |
| B12 | `os.open` is read as a mode string again instead of through its FLAGS | 1 |
| B13 | `_os_open_reads` answers True for every `os.open`, so a creating open reads | 1 |
| B14 | `O_RDONLY` dropped from `_READING_FLAGS` | 1 |
| B15 | `_flag_names` stops reading an OR of two flags | 1 |
| B16 | `_flag_names` answers a flag name for anything, so an unreadable flag reads | 1 |
| B17 | `_open_mode` reads position one for a bound call, the round three defect | 1 |

### Round four's rows, re-run against round five's code

| id | what was reverted | round 4 | round 5 |
|-|-|-|-|
| N01 | `_receiver_key` stops rendering an ATTRIBUTE CHAIN | 1, verifier measured 2 | 4 |
| N08 | container literal ELEMENTS no longer bound | 1, verifier measured 2 | 4 |
| N05 | the rebinding sweep removed, imports only | 9 | 15 |
| N12 | the ASSIGNMENT rebinding branch removed | 5 | 12 |
| N21 | `mutations_in` stops descending into NESTED SCOPES | 50, verifier measured 51 | 64 |
| N22 | `_receiver_module` answers an UNRESOLVED name with itself | 8, verifier measured 4 | 20 |
| N23 | rule 5 removed outright | 3 | 3 |
| N26 | the computed half gated on the switch, not on being called | 3 | 18 |
| M35 | `write_text` dropped from `FILESYSTEM_MUTATIONS` | 13 | 13 |

Every one still dies. The counts are HIGHER because this round adds 48 tests, most
of them driving exactly the machinery these rows revert. No number here is
inherited: each was measured against the shipped file.

**X10 could not be confirmed.** It is one of eighteen untabled reverts a verifier
measured at 16 deaths, and its definition was never written into the repository,
so there is no way to re-run it without guessing what it reverted. Guessing and
reporting the guess as a measurement is the defect this file exists to stop. The
other seven confirm rows above were re-runnable because round four's table is in
its commit body.

### Two zero rows fixed rather than argued, and one line deleted

- The four rows that measured zero on the first pass were C10, C12, C13 and C14,
  all in the new reflection machinery. Each was a real mechanism with no fixture
  driving it, and each got the fixture: a read bound through a conditional, a
  read bound by a walrus or an annotated assignment, a read bound to a name used
  ONLY as a decorator, and a read inside a nested function whose result is called
  from the scope around it. S07, S08, S11, S13, S17, S20 and S22 were the same
  story in the shadow list and got the same answer.
- `_assigned` used to return an empty owner so the caller could tell "bound to
  something unreadable" from "not bound". That was a second mechanism doing what
  `_bound_here` already does, it measured zero, and it is gone rather than
  argued. One fact, one place.
- The `global` and `nonlocal` subtraction in `_names_taken` measured zero and was
  also WRONG on inspection: `global config` followed by `config = dict(raw)`
  really does take the name back in that scope. Deleted.
- X17 and X18, the two `continue` statements whose comments claimed they
  prevented double reporting, are gone. The rule chain in `mutations_in` is
  `if`/`elif` now, so the claim is true by structure rather than by comment.

### What was measured against the real tree, not against a fixture

- Every one of the ten false positive shapes and the three missed writes is
  appended to the REAL `src/cratekit/modules/reports/aging.py`, read from disk.
- The `os.open` row is driven against the real `src/cratekit/core/jobs.py`, whose
  line 788 opens a directory read only for an fsync and was reported as a write.
- Rule 5's cost was measured by walking all 75 files under `src`: zero namespace
  subscripts spelling a filesystem verb.
- Real tree today: 4 governed modules walked, 0 offenders, 0 forbidden imports;
  8 admitted modules audited, 0 unnamed writers.
