# U34 mutation tables

Two mutation tables were lost during this unit by living only in a chat
transcript. This file exists so the next one is not, and so a later reader can
tell a guard that is held from a guard that merely looks held.

Every row is one revert applied ALONE to the shipped file, followed by the suite,
followed by a restore verified against a checksum. A row's number is the count of
FAILING TESTS, which pytest already counts one parametrized case at a time.

**Node ids come from a pytest plugin's report objects, never from the
`FAILED <id> - <message>` line.** That separator appears INSIDE parametrized ids
in this repository, so splitting on it collapses two rows into one; a driver on
another branch undercounted a row by exactly that. The plugin reads
`report.nodeid` off the report object.

**A REVERT THAT LEAVES NO ARTIFACT IS NOT A MEASUREMENT.** If a line is added and
then deleted inside one round, the deletion is invisible to review: neither the
line nor its absence exists at `HEAD~1`, so "it measured zero" is a written
explanation rather than something anyone can re-run. Either do not add it, or put
the revert in this table with its spelling written out. Round five deleted
`_assigned`'s empty-owner return and a `global`/`nonlocal` subtraction on exactly
that basis and neither is checkable. Round six adopts the rule and adds no
unrecorded deletion.

## Round 6

Forty one rows, every one a guard, constant, condition or assertion this round
adds or changes, plus eleven of the earlier rounds' re-run against the new code.
**No row killed zero.** Five rows measured zero on the first pass and each one was
FIXED rather than argued: four by writing the driver the guard was missing, one by
collapsing a fact that had been written out in two places.

Counts are scoped to `tests/modules/test_reports.py`, which nothing else in the
suite imports. Four rows were re-measured against the whole `tests` tree to check
the scoping and every one gave the same figure both ways: Q01 7, R05 8, N21 91,
M35 25.

Baseline before the round: 3397 passed, 15 skipped, 3412 collected.
Baseline after: 3434 passed, 15 skipped, 3449 collected.

Thirty seven tests are added and none removed, verified by collecting node ids
with a plugin and diffing them against `HEAD~1`. **Every one of the 37 is killed
by at least one revert**, checked by taking the union of the failing ids across
all 41 rows and subtracting.

### F1: an object key that did not carry its owner

`self` is a parameter, so it means a different object in every method of every
class, and an object key is carried file-wide. Keyed on the bare spelling, one
class binding `self.config` to the module made every other class's `self.config`
a finding, including `def go(self): return self.config.load` in a class whose
constructor takes `config` as an argument.

| id | what was reverted | deaths |
|-|-|-|
| Q01 | `_receiver_key` ignores the owning class, so two `self` in one file share one key | 7 |
| Q02 | `_method_instance` keys on the literal name `self` instead of the FIRST POSITIONAL parameter | 1 |
| Q03 | `_method_instance` stops exempting a `staticmethod`, so an ordinary parameter called `self` becomes an instance | 1 |
| Q04 | `_method_instance` reads a `classmethod`'s first parameter as an instance, so `cls.mod` finds a constructor's binding | 1 |
| Q12 | `_member_scope` stops extending the class path for a NESTED class, so `A.B` and a sibling `B` are one owner | 1 |
| Q13 | `_member_scope` stops dropping the instance when a nested scope takes that name back | 1 |
| Q14 | `_member_scope` stops carrying the instance into a nested scope, so a closure over `self` loses it | 1 |
| Q15 | a method's RETURNED value is keyed without its class, colliding with a module level function of the same name | 1 |

### F2: a class body that bound nothing its methods could reach

`self.mod = config` in a constructor fired and had a test. `mod = config` in the
class body was the same assignment one indent apart, and it created no object key
at all: the body was walked as part of the scope around it, so it bound the bare
name `mod` at MODULE level and neither `self.mod` nor `Keeper.mod` ever existed.
A class body is a scope now, with the one rule of its own that Python gives it.

| id | what was reverted | deaths |
|-|-|-|
| Q06 | `ast.ClassDef` dropped from `_SCOPES`, which is the reading round five shipped | 14 |
| Q07 | `_walk_bindings` stops writing the `<Class>.<name>` attribute key | 4 |
| Q08 | `_walk_bindings` stops writing the `<Class>::self.<name>` key | 4 |
| Q09 | `_handed_to_members` hands a class's methods the table the CLASS built rather than the one it inherited | 1 |
| Q11 | `_defined_here` stops reading a `ClassDef`, so a class no longer takes its own name | 1 |
| Q16 | the audit stops naming a `ClassDef` as its own owner, so every method's `self` renders unqualified | 1 |

### F3: rule 5's receiver, read off the expression instead of the table

The round before built a binding table that follows `alias = config` and then did
not ask it about `table = vars(Path)`. Two ordinary lines wrote a file with ruff,
both structural guards and the audit green, and so did the `dict()`, spread,
returned, stored, default-argument, loop and `globals()` spellings of the same
binding. There is ONE place a receiver resolves now, `_bound_value`, and rule 1
and rule 5 both ask it.

| id | what was reverted | deaths |
|-|-|-|
| R05 | RULE 5 READS ITS RECEIVER INLINE AGAIN, which is what round five shipped: `_namespace_of` off the subscript's own `value`, table never asked | 8 |
| R06 | rule 5 drops the namespace requirement, comparing every constant subscript key against the mutation set, which is round four's receiver free rule | 28 |
| R01 | `_namespace_of` stops recognising `__dict__` | 6 |
| R02 | `_namespace_of` stops recognising `vars()` | 11 |
| R03 | `_namespace_of` stops reading through a `dict()` copy | 1 |
| R04 | `_namespace_of` stops reading through a `{**...}` spread literal | 1 |
| R07 | `_namespace_reads` stops reporting a key it CANNOT READ, so `Path.__dict__["write" + "_text"]` is quiet | 2 |
| R08 | `_namespace_reads` reports an unreadable key with the reflection switch OFF too, so `vars(spec)[field]` is a writer in the audit | 1 |
| R09 | `_call_mutations` drops the namespace ASKED branch, so `Path.__dict__.get("write_text")` and `vars(x).pop(...)` are quiet | 2 |
| R10 | `_returned_value` hands back modules only, so a helper returning an attribute mapping binds nothing | 1 |
| R11 | `_namespace_reads` drops the OWNER read, so `vars(config)["save"]`, named only in `QUALIFIED_MUTATIONS`, is missed | 1 |
| R12 | `_global_aliases` answers nothing, so a module reached through `globals()["config"]` is unresolved | 1 |

The five further spellings the verifier measured quiet are each held above rather
than closed one at a time: `Path.__dict__.get(...)` by R09, `dict(vars(Path))` by
R03, `{**vars(Path)}` by R04, the concatenated key by R07, and
`globals()["config"]` by R12.

### F4: a read reported as a write

`_READING_FLAGS` holds bare names and `_flag_names` could only produce one from
`os.O_RDONLY`, so `from os import O_RDONLY` followed by `os.open(str(path),
O_RDONLY)` was an unreadable flag set and therefore a finding. The real
`cratekit/core/jobs.py` happens to spell it dotted, which is the only reason this
was not live in the tree.

| id | what was reverted | deaths |
|-|-|-|
| T01 | `_flag_names` stops reading a BARE NAME, so an imported `os` flag is unreadable | 1 |
| T02 | `_flag_names` answers a READING flag for an expression it cannot read at all, so `os.open(p, chosen())` reads | 1 |

Every WRITING flag still fires in the bare spelling, and a flag held in a variable
still fires: reading a name is not the same act as accepting one. Six writing
spellings and four reading ones are asserted beside each other in
`test_a_module_level_open_does_not_have_its_file_read_as_its_mode`.

### F5: rule 4's computed half had no false positive row

`test_the_audit_stays_quiet_on_a_reflective_read_nothing_calls` survived all 68 of
round five's reverts. It is not vacuous, but nothing in that table made `invoked`
LARGER, so the direction it asserts was held by no row.

| id | what was reverted | deaths |
|-|-|-|
| U01 | `_invoked_reads` answers with EVERY reflective read rather than only the ones whose result is called | 4 |

### F6: B09 measures 2, not 1

Re-measured with the verifier's exact spelling,
`if (id(node) in invoked and name == "getattr") or reflection:`, against round
six's code.

| id | what was reverted | round 5 recorded | round 6 measured |
|-|-|-|-|
| B09 | a computed `__getattribute__` is gated on the reflection switch again instead of on its result being called | 1 | 2 |

The description was accurate and the count was low. That revert changes behaviour
in TWO places, not one: with the switch on, a computed `__getattribute__` that
nothing calls starts firing, and with the switch off, a computed
`__getattribute__` whose result IS called stops firing. Round five's row named
only the second. Both are driven, which is why it is 2.

### The earlier rounds' rows, re-run against round six's code

| id | what was reverted | round 5 | round 6 |
|-|-|-|-|
| S16 | `_visible_bindings` adds the scope's own bindings BEFORE shadowing instead of after | 19 | 37 |
| N21 | `mutations_in` stops descending into NESTED SCOPES | 64 | 91 |
| N22 | `_receiver_module` answers an UNRESOLVED name with itself | 20 | 20 |
| N05 | the rebinding sweep removed, imports only | 15 | 31 |
| M35 | `write_text` dropped from `FILESYSTEM_MUTATIONS` | 13 | 25 |
| N12 | the ASSIGNMENT rebinding branch removed | 12 | 27 |
| S01 | `_names_taken` reverted to PARAMETERS ONLY, the flat table round four shipped | 11 | 11 |
| C01 | `_called_keys` answers nothing | 8 | 8 |
| S09 | `_bound_here` stops reading a PARAMETER LIST | 7 | 10 |
| C05 | `_invoked_reads` stops reading a read BOUND TO A NAME the file calls | 6 | 6 |
| C09 | `_invoked_reads` stops reading the INLINE spelling | 5 | 5 |

Every one still dies. The counts that rose are the rows this round's 37 tests
drive directly; the ones that did not rise are held by the same tests as before.

**X10 is still not re-runnable and is still not guessed.** Round five's verifier
measured it at 16, which matches round four's figure, so the number is settled and
the record is no longer open on it. What does not exist anywhere in this
repository is its DEFINITION, so this round could not apply it and did not invent
one. The 16 above the line is that verifier's measurement, attributed rather than
claimed.

### Two numbers in round five's record corrected

Both corrections are round five's verifier's measurements, recorded here rather
than re-derived, and attributed for that reason.

- **N05 is 8 old plus 7 new, not 9 plus 6.** Round five wrote that its higher
  counts were the round's 48 new tests, which is right for seven rows and wrong
  for this one. Deselecting exactly the 48 new node ids gave 8 against round
  four's tests rather than the 9 round four measured, because
  `EVASIVE_ALLOWLISTED_WRITER_FROM_A_CALL` is now held independently by
  `_returned_module` and S19.
- **Round four's recorded N22 does not reproduce against round four's own code
  and tests.** The round five column is correct and the round four column is not.

### Five zero rows fixed rather than argued

- **Q04** measured zero because the fixture asked whether a classmethod could read
  an instance attribute, which is broken code either way. The driver it got is a
  class attribute OVERRIDDEN per instance and read from a classmethod, which is
  ordinary and runnable, and where reading `cls` as an instance makes an ordinary
  method a write to the library.
- **Q15** measured zero because nothing spelled the collision. The driver is a
  method `_mod` returning the module beside a module level `_mod` that does not,
  with both directions asserted.
- **R11** measured zero because every namespace fixture used a name in
  `FILESYSTEM_MUTATIONS`. The driver is `vars(config)["save"]`, a generic writer
  named only by the module it belongs to, with `vars(view)["save"]` beside it.
- **T02**'s first spelling was a no-op once `_flag_names` read a bare name, so it
  was respelled as the fallback answering a reading flag and driven by
  `os.open(p, chosen())`.
- **Q09 was not a missing driver, it was a duplicated fact.** "A class body's
  names are not visible inside its methods" was written out in `_walk_bindings`
  and again in `mutations_in`. The binding-walk copy measured zero because names
  do not leave their scope, so only the mutation-walk copy could be observed. Both
  are now one call to `_handed_to_members`, which is one line to revert and
  measures 1. A zero row is what a duplicated fact looks like from here.

### What was measured against the real tree, not against a fixture

- Every shape in F1, F2 and F3 is appended to the REAL
  `src/cratekit/modules/reports/aging.py`, read from disk. All six findings were
  found that way and all six are driven that way.
- The `os.open` row is driven against the real `src/cratekit/core/jobs.py`, whose
  line 788 opens a directory read only for an fsync.
- Rule 5's cost was re-measured across all 75 files under `src` with the binding
  now in play: ONE namespace expression exists in the tree, `state = vars(obj)` at
  `src/cratekit/core/rb_writer.py` line 1840, and it is quiet. It is bound, so the
  rule sees it, and every lookup through it is `state.items()`, which carries no
  constant key.
- Real tree today: 4 governed modules walked, 0 offenders, 0 forbidden imports;
  7 admitted modules audited, 0 unnamed writers. The eighth admitted module is
  `SANCTIONED_PERSISTENCE`, which R12 licenses to write and which the audit skips
  by name.

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

Round six renamed two of the functions these rows name: `_bound_module` is
`_bound_value`, `_returned_module` is `_returned_value`, and `S08`'s fact moved
from `_bound_here` to `_defined_here` when a class body became a scope (round
six's Q11).

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

Round six replaced `_namespace_owner` with `_namespace_of` and moved the
resolution into the binding table, so B06 is R06, B07 is R01 and B08 is R02.

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
| B09 | THE DUNDER. a computed `__getattribute__` is gated on the reflection switch again instead of on its result being called | 1, round six measured 2 |
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

Round six's T02 is B16 respelled: once `_flag_names` reads a bare NAME, B16's
old spelling no longer changed any answer.

### Round four's rows, re-run against round five's code

| id | what was reverted | round 4 | round 5 |
|-|-|-|-|
| N01 | `_receiver_key` stops rendering an ATTRIBUTE CHAIN | 1, verifier measured 2 | 4 |
| N08 | container literal ELEMENTS no longer bound | 1, verifier measured 2 | 4 |
| N05 | the rebinding sweep removed, imports only | 9, re-measured as 8 | 15 |
| N12 | the ASSIGNMENT rebinding branch removed | 5 | 12 |
| N21 | `mutations_in` stops descending into NESTED SCOPES | 50, verifier measured 51 | 64 |
| N22 | `_receiver_module` answers an UNRESOLVED name with itself | 8, does not reproduce | 20 |
| N23 | rule 5 removed outright | 3 | 3 |
| N26 | the computed half gated on the switch, not on being called | 3 | 18 |
| M35 | `write_text` dropped from `FILESYSTEM_MUTATIONS` | 13 | 13 |

### Two zero rows fixed rather than argued, and one line deleted

- The four rows that measured zero on the first pass were C10, C12, C13 and C14,
  all in the new reflection machinery. Each was a real mechanism with no fixture
  driving it, and each got the fixture: a read bound through a conditional, a
  read bound by a walrus or an annotated assignment, a read bound to a name used
  ONLY as a decorator, and a read inside a nested function whose result is called
  from the scope around it. S07, S08, S11, S13, S17, S20 and S22 were the same
  story in the shadow list and got the same answer.
- `_assigned` used to return an empty owner so the caller could tell "bound to
  something unreadable" from "not bound". **This deletion is not checkable**: the
  line was added and removed inside one round, so neither it nor its absence is
  at `HEAD~1`. Round six restates what `_assigned` actually does in its docstring
  rather than repeating the claim: a NAME comes back whether or not it resolved,
  and only an unreadable TARGET comes back with nothing.
- The `global` and `nonlocal` subtraction in `_names_taken` was deleted on the
  same unrecorded basis. The REASONING checks out and was independently
  re-measured: `global config` followed by `config = dict(raw)` is taken back by
  the `Assign`, quiet in that scope and still firing in a sibling function. The
  MEASUREMENT that justified the deletion does not exist.
- X17 and X18, the two `continue` statements whose comments claimed they
  prevented double reporting, are gone. The rule chain in `mutations_in` is
  `if`/`elif` now, so the claim is true by structure rather than by comment, and
  it was re-checked: the chain is four disjoint node types and nothing double
  reports.

### What was measured against the real tree, not against a fixture

- Every one of the ten false positive shapes and the three missed writes is
  appended to the REAL `src/cratekit/modules/reports/aging.py`, read from disk.
- The `os.open` row is driven against the real `src/cratekit/core/jobs.py`, whose
  line 788 opens a directory read only for an fsync and was reported as a write.
- Rule 5's cost was measured by walking all 75 files under `src`: zero namespace
  subscripts spelling a filesystem verb.
- Real tree at the end of round five: 4 governed modules walked, 0 offenders, 0
  forbidden imports; 8 admitted modules audited, 0 unnamed writers.
