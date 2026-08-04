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

**A ROW'S SPELLING IS PART OF ITS NUMBER.** Two rows in this file carry counts
that do not reproduce, and in both cases the reason is that the revert's exact
text was never written down, so a later round could only guess at it. Round seven
writes every revert out verbatim in `docs/mutation/u34-round-7-reverts.py`, and where
a re-measured count differs from the recorded one it says whether the difference
is the round's new tests, a change in what the row means, or a spelling nobody
can recover.

## Round 8

Thirty six rows: twenty this round adds, two of round seven's RE-SPELLED because
this round edited the lines they anchored on, and fourteen more of the earlier
rounds' re-run unchanged. **No row killed zero.** Two measured zero on the first
pass and each was FIXED rather than argued, one by making the claim it stood for
checkable and one by finding the shape the guard was written for and had never
reached.

Every revert is written out verbatim in `docs/mutation/u34-round-8-reverts.py`.
Counts are scoped to `tests/modules/test_reports.py`, which nothing else in the
suite imports.

Baseline before the round: 3458 passed, 15 skipped. The file collects 285.
Baseline after: 3486 passed, 15 skipped. The file collects 313.

Twenty eight tests are added and none removed, verified by collecting node ids
with a plugin and diffing them against `HEAD`. **Every one of the 28 is killed by
at least one revert**, checked by taking the union of failing ids across all 36
rows and subtracting: 0 uncovered.

### F1: an assignment that could not be read still has to take the key back

**Six ordinary shapes were reported as writes to the library**, every one of them
a subclass overriding an attribute its base binds. Each is two or three lines
appended to the real `aging`, each was quiet at round six and FIRED at round
seven on both `filesystem_mutations` and `_unnamed_writers`, and not one of them
is a write:

```python
class Base:
    def __init__(self):
        self.mod = config


class Row(Base):
    def __init__(self, raw):
        self.mod = dict(raw)      # Base.__init__ is never called

    def go(self, cfg):
        return self.mod.save(cfg)  # reported: line 355: config.save
```

`Row.__init__` assigns `self.mod` to something `_binds` cannot read, so nothing
was written into `declared` for `Row#350::self.mod`. `_carry` then copied
`Base#345::self.mod` down with `setdefault`, and there was nothing for `declared`
to win over in the `{**reached, **declared}` merge.

**The fix already existed thirty lines away.** `_scope_own_bindings` records a
FAILED ATTEMPT for a NAME an assignment took and could not resolve, which is row
S21. The object half of the same table recorded silence. Binding nothing and
taking the key back are two different facts, and silence cannot tell them apart.
The object half records a failed attempt now, on the same rule, and the class
body records one too, so `class Row(Base): mod = None` shadows `class Base: mod =
config` the way it does at runtime.

**BOTH DIRECTIONS ARE MEASURED, which is what round seven did not do.** Round
seven measured only what it lost. Round eight drove the false positive direction
and the miss direction on every change:

| direction | driven | result |
|-|-|-|
| false positive, the six above | 6 shapes against the real `aging`, both guards | all 6 FIRE at `HEAD`, all 6 quiet after |
| miss, this file's own writes | `INHERITED_ATTRIBUTE_REACHES_A_WRITER` 6, `MISSED_WRITES_IN_A_REPORT` 3, `CLASS_ATTRIBUTE_REACHES_A_WRITER`, `NAMESPACE_REACHES_A_WRITER`, `WRITES_A_WIDER_SHADOW_WOULD_LOSE` | every one still FIRES |
| false positive, this file's own controls | `ORDINARY_SHAPES_IN_A_REPORT` 10, `INHERITANCE_STAYS_IN_THE_FAMILY` 5, `SHADOWS_IN_A_SCOPE`, `ORDINARY_MAPPING_LOOKUPS`, `CLASS_BODY_STAYS_IN_THE_CLASS`, `ORDINARY_LOOKUPS_THROUGH_A_BINDING` | every one still quiet |
| miss, new controls this round adds | 5 shapes an override must NOT block: a sibling through a mixin, one class binding twice in each order, a base below an override, a body attribute left alone | every one FIRES |

**The direction of a block is the whole of it.** An override blocks UPWARD, where
a nearer class really does stand between the reader and the farther one, and never
DOWNWARD, where a mixin's `self` is as easily some other subclass. Rows V04 and
V05 are those two directions, and each kills a test the other does not.

### F2: two losses that were never undecidable, and three that are

The residual on a class rebound after its own definition covered six spellings and
had measured one. All six execute with `Keeper.mod is config` confirmed at
runtime, so all six are real writes.

| spelling | at `HEAD` | now | why |
|-|-|-|-|
| `Keeper = dataclass(Keeper)` | quiet | quiet | undecidable, named in the residual |
| `Keeper = type("Keeper", (Keeper,), {})` | quiet | quiet | undecidable, now NAMED rather than implied |
| `Keeper = _wrap(True)(Keeper)` | quiet | quiet | undecidable, now NAMED rather than implied |
| `if True: Keeper = dataclass(Keeper)` | quiet | **FIRES** | a veto inside an arm a run can skip |
| two `class Keeper` in the arms of a conditional | quiet | **FIRES** | only one arm runs, so nothing took the name |
| `Keeper = Keeper` | quiet | **FIRES** | both bindings are the same class |

**The residual called the conditional case correct and it is not.** Its reasoning,
that `Keeper.mod` is an `AttributeError` once a later `class Keeper` takes the
name, is true of two definitions in ONE statement list and false of two arms of a
conditional, where only one runs. That is a judgement transferred from a
measurement to a shape whose premise is false, and the sentence is withdrawn in
the residual.

`if True: Keeper = dataclass(Keeper)` was expected to be undecidable too and is
not, which is a measurement rather than a reading: the rule is applied to the
VETO only, never to the shadow, so a name whose only binding is inside a branch is
still taken and still comes back unresolved. The ten ordinary shadow shapes and
the branch-only controls are all driven and all still quiet.

### The rows

| id | what was reverted | deaths |
|-|-|-|
| V01 | `_scope_own_bindings` object half stops recording a FAILED attempt | 5 |
| V02 | `_walk_bindings` writes a class body attribute only when it RESOLVED | 1 |
| V03 | `_record` lets an unresolved key OVERWRITE a resolved one | 1 |
| V04 | `_carry` carries an unresolved key DOWNWARD too | 1 |
| V05 | `_carry` never carries an unresolved key, upward included | 1 |
| V06 | `_scope_own_bindings` drops a name that did not settle instead of answering it empty | 1 |
| V07 | `_rebound_to_itself` answers nothing | 4 |
| V08 | `_names_taken` stops exempting a self rebinding | 2 |
| V19 | `_scope_own_bindings` stops recording what an IDLE rebinding already held | 2 |
| V20 | an idle rebinding records a FAILED attempt when what it held cannot be read | 2 |
| V09 | `_alternate_classes` records nothing | 1 |
| V10 | `_alternate_classes` calls two definitions in ONE statement list alternates too | 1 |
| V11 | `_sequences` reads the scope's own body only | 1 |
| V12 | `_inherited_attributes` stops carrying an ALTERNATE definition's attributes | 1 |
| V13 | `_branched` answers nothing | 3 |
| V14 | `_branched` counts a `finally` block as skippable | 1 |
| V15 | the citation guard stops exempting the delimited collision passage | 1 |
| V16 | the citation guard stops reading `docs/` | 1 |
| V17 | the handoff's report-verbs citation restored to the NUMBER spelling | 1 |
| V18 | the collision passage's CLOSING marker removed | 1 |

**V01 kills five of the six false positives and V02 kills the sixth.** The class
body attribute is written by a different line from the instance attribute, so the
class-body shape is held by the class-body row. Saying that is the point of
writing the number down.

**Two rows measured zero on the first pass.**

- **V16 measured 0 and was FIXED by making the claim checkable.** Dropping `docs/`
  from the guard's file list killed nothing, because `docs/` was clean by then: the
  guard's WIDTH was not asserted anywhere, only its result. The width is asserted
  now, so a guard that quietly stopped reading a document fails. That is the same
  defect the round is correcting, one level up.
- **V08 measured 0 and was FIXED by finding the shape it was written for.** The
  self-rebinding exemption in `_names_taken` changed no answer, because at module
  scope there is nothing inherited to keep. The shape that needs it is
  `class Keeper: config = config`, the ordinary way a module is pinned as a class
  attribute for injection: it executes with `Keeper.config is config` and it was
  QUIET, a real write missed. An idle rebinding now records what the key already
  held rather than nothing, which closes it and makes the exemption load-bearing.

### The earlier rounds' rows, re-run against round eight's code

Every one of the sixteen still dies. Two had to be RE-SPELLED because round eight
edited the lines they anchored on, and their round seven text now occurs zero
times, which is exactly the failure the reverts file exists to prevent.

| id | round 7 | round 8 | note |
|-|-|-|-|
| N21 | 105 | 118 | |
| S16 | 47 | 60 | |
| N05 | 42 | 54 | |
| R06 | 36 | 49 | |
| N12 | 36 | 46 | |
| M35 | 29 | 29 | |
| N22 | 27 | 32 | |
| Q06 | 20 | 31 | |
| R02 | 16 | 16 | |
| S09 | 14 | 15 | |
| R06b | 13 | 13 | |
| Q01 | 12 | 19 | |
| Q11 | 11 | 17 | |
| S01 | 11 | **3** | RE-SPELLED, and the drop is real. See below |
| S18 | 10 | 14 | RE-SPELLED |
| P14 | 10 | 16 | |

**S01 fell from 11 to 3, and that is a finding rather than a rounding.** Reverting
`_names_taken` to parameters only used to leave a stale import binding live under
every rebound name. It no longer does, because this round makes `_scope_own_bindings`
answer an unsettled name with an EMPTY value instead of with nothing, and
`_visible_bindings` writes that empty answer over the inherited table. The shadow
is now held in two places, and the three tests only `_names_taken` still holds are
exactly the shapes where the scope's own table has nothing to write:

- a loop that rebinds the name, with the rebinding inside the body
- a name whose ONLY binding is inside a branch
- an `except` target

Two mechanisms that overlap on most fixtures and come apart on three is the same
shape round seven found in R14 and R16. They are kept apart rather than collapsed
because the three shapes above are real and only one of the two answers them.

### Coverage of the 28 new tests

All 28 are killed by at least one of the 36 rows. **Twenty are killed by a round
eight row and eight only by an earlier round's row**, and that split is not
accidental: all twenty of round eight's own rows NARROW the guard, while the eight
are controls whose failure mode is a guard that got WIDER. They are held by N22,
R06, N05, N12, N21, S16, S18, S09, P14, Q01, Q06, Q11 and the re-spelled S01.

## Round 7

Sixty eight rows, every one a guard, constant, condition or assertion this round
adds or changes, plus thirty seven of the earlier rounds' re-run against the new
code. **No row killed zero.** Three rows measured zero on the first pass and each
one was FIXED rather than argued: one by adopting the "revert" as the shipped
reading, one by writing the driver the guard had never had, and one pair by
finding the shape where two mechanisms that overlapped on every fixture come
apart.

Counts are scoped to `tests/modules/test_reports.py`, which nothing else in the
suite imports.

Baseline before the round: 3434 passed, 15 skipped, 3449 collected.
Baseline after: 3458 passed, 15 skipped, 3473 collected. The file itself collects
285, up from 261.

Twenty four tests are added and none removed, verified by collecting node ids
with a plugin and diffing them against `HEAD`. **Every one of the 24 is killed by
at least one revert**, checked by taking the union of the failing ids across all
68 rows and subtracting: 0 uncovered.

### F1: the key landed on the class that DECLARES, not the class that REACHES

Round six keyed a class attribute under the class whose body or constructor wrote
the line. Python does not look an attribute up that way. A subclass sees what its
bases bound, and a base's method is handed a subclass as its `self`, so three
ordinary shapes were each two or three lines appended to the real `aging` that
wrote the configuration file with both structural guards and the audit green: a
base class constructor read from a subclass, a writer in a `WriterMixin` over a
binding made in `class Row(WriterMixin).__init__`, and an inherited class body
attribute. **Round five caught all three**, by keying `self.mod` file-wide, and
round six traded that coverage for the `Injected` versus `Holder` fix. A fourth,
`Row.go = _go`, was missed by both.

A class is a value a name is bound to now, `_Class`, carrying its definition site
and the identities of its bases. What a class family reaches is a closure taken
once over the whole file, `_inherited_attributes`, kept in a table SEPARATE from
what each class declared so a derived key is never re-derived from.

| id | what was reverted | deaths |
|-|-|-|
| P01 | `_inherited_attributes` answers nothing, so no class reaches what its family declared | 6 |
| P07 | `_class_of` stops resolving a class's BASES, so every class is its own family | 6 |
| P17 | `_walk_bindings` stops recording who inherits from whom, so the closure has no family to take | 6 |
| P15 | `_bound_value` stops resolving an attribute THROUGH a class, so `Keeper.mod` is only ever a flat spelling | 5 |
| P04 | `_inherited_attributes` resolves an INSTANCE attribute downward only, so a subclass cannot see what its base's constructor bound | 4 |
| P02 | `_inherited_attributes` stops resolving a CLASS attribute through the bases, so `Row.mod` never finds `Base.mod` | 1 |
| P03 | `_inherited_attributes` resolves an INSTANCE attribute upward only, so a mixin's method cannot see what its subclass binds | 1 |
| P05 | `_related` walks ONE HOP instead of transitively, so a grandparent is not a relative | 1 |
| P08 | `_writer_bindings` folds REACHED back into DECLARED, so a derived key is re-derived from | 1 |
| P09 | `_walk_bindings` carries out the scope's whole VIEW rather than its OWN bindings, which is what round six shipped | 1 |
| P10 | `_member_scope` stops reading `_attachments`, so a method attached by `Row.go = _go` is nobody's method | 1 |
| P11 | the audit stops reading `_attachments`, so an attached writer is read as a plain module level function | 1 |
| P12 | the audit stops handing `mutations_in` an INSTANCE, so an attached function's first parameter is nobody's | 1 |

`P06` belongs to the false positive direction and is in the next table, because
what it reverts is the ONLY thing keeping the two directions apart.

#### What this change now MISSES that round six caught, measured

Round six keyed a class attribute as flat TEXT, so a rebinding of the class's
name was invisible to it and every spelling of `Keeper.mod` in the file was one
key. Round seven resolves the name first. Five shapes were run against the real
`aging` on BOTH `HEAD` and this branch to find where the two answers differ.

| shape | round 6 | round 7 | verdict |
|-|-|-|-|
| `Keeper = dataclass(Keeper)` after the class body, then `Keeper.mod.save(cfg)` | FIRES | quiet | **LOST, and it is a real write** |
| the FIRST of two `class Keeper` at module level, then `Keeper.mod.save(cfg)` | FIRES | quiet | correct: the second class has no `mod`, so this is an `AttributeError` |
| a factory's local `class Keeper` read from outside the factory | FIRES | quiet | correct: `NameError` |
| `Outer.Keeper.mod.save(cfg)` where `Outer` is a PARAMETER | FIRES | quiet | correct: this is F4 exactly |
| `@dataclass` written above the class (control) | FIRES | FIRES | held |

**One genuine loss**, and it is filed rather than argued, under the residual
title "A class rebound after its own definition is no longer reachable by name".
Closing it means deciding whether an arbitrary callee hands its argument back,
which is the question the residual titled "One reflective call shape stays out of
reach, and it is named" already declines to answer for
`map(getattr(p, n), items)`. The spelling an author actually writes, the
decorator above the class, is covered and has a fixture in the control row.

### F3 and F4: identity that is not unique, one level further out

A class was a SPELLING in round six: `A.Keeper` for a class nested in a class and
the bare `Keeper` for a class nested in a FUNCTION. Two factories each returning a
`Keeper` therefore shared one root, so one factory's class body decided for the
other's, and an ordinary method reading its own injected argument was reported as
a write to the library. A module level redefinition of a class name was the same
fact. And an object key spelled with a dot was never a NAME, so nothing could
shadow it: `def go(Keeper)` could not take the name back, on a parameter that
really is a different object.

Both are closed by the same move. A class name is an ordinary lexical binding
whose value is a `_Class`, so it shadows and is shadowed like every other name,
and the identity underneath it is the DEFINITION SITE, which two `class Keeper`
statements cannot share.

| id | what was reverted | deaths |
|-|-|-|
| P14 | `_scope_own_bindings` stops recording a nested CLASS as a binding of its own name | 10 |
| P13 | `_class_key` answers the class's NAME, which is round six's identity, so two `class Keeper` are one class | 3 |
| P06 | `_related` reads a family as one CONNECTED COMPONENT, walking both directions at once, so one subclass sees its sibling's binding through their shared base | 2 |

### F2: a namespace is a value that PROPAGATES

`_namespace_of` read four literal spellings, and `_call_mutations`'s ASKED branch
required arguments. Three more spellings passed `forbidden_imports`,
`filesystem_mutations` AND `_unnamed_writers`, all `[]`, and **all three were
executed and confirmed to write a real file**:

    (Path.__dict__ | {})["write_text"](path, decided)     # dict union, zero imports
    vars(Path).copy()["write_text"](path, decided)        # .copy() takes no args, so ASKED never fired
    ChainMap(vars(Path))["write_text"](path, decided)     # "collections" IS in ALLOWED_IMPORTS

`dict(vars(Path))` was R03 and `{**vars(Path)}` was R04, so the first two are the
same act one operator out. Two ROOTS originate a namespace and one propagation
rule carries it: `_mapping_operands` names the OPERAND POSITIONS a mapping can
come out of rather than the operations that produce one.

| id | what was reverted | deaths |
|-|-|-|
| R03 | `_mapping_operands` stops yielding a CALL's ARGUMENTS, so `dict(vars(Path))` and `ChainMap(vars(Path))` carry nothing | 2 |
| R04 | `_mapping_operands` stops yielding a `**` SPREAD value in a dict literal | 1 |
| R13 | `_mapping_operands` stops yielding a BINARY OPERATOR's operands, so a dict union of a type's `__dict__` carries nothing | 1 |
| R14 | `_mapping_operands` stops yielding a method call's RECEIVER, so `vars(Path).copy()` carries nothing | 1 |
| R15 | `_mapping_operands` stops yielding a call's KEYWORD values, so `dict(**vars(Path))` carries nothing | 1 |
| R16 | `_call_mutations`'s namespace ASKED branch requires ARGUMENTS again, so a mapping method that takes none is invisible | 1 |

**R14 and R16 both measured zero on the first pass, and for the same reason:**
`vars(Path).copy()["write_text"]` is caught twice over, by the propagation through
the subscript and by the ASKED branch reporting a key it cannot read, so neither
revert alone changed the answer. They are two different acts and the drivers now
say so. R14 is asserted through the AUDIT, where the reflection switch is off and
the unreadable-key branch cannot answer at all, so only the propagation is left.
R16 is asserted on `vars(Path).popitem()`, which is never subscripted, so only
the ASKED branch can see it.

### F5: R06's description named a rule it is not

Round six's R06 row read "which is round four's receiver free rule". It is not.
R06 drops the namespace REQUIREMENT while keeping `_namespace_reads`, so it still
reads the owner and still reports a key it cannot read. Round four's rule kept
neither: it compared `node.slice.value` against `FILESYSTEM_MUTATIONS` and
nothing else. Both are measured here rather than argued.

| id | what was reverted | round 6 recorded | round 7, round 6's tests only | round 7, all tests |
|-|-|-|-|-|
| R06 | rule 5 drops the namespace requirement, comparing every constant subscript key against the mutation set through `_namespace_reads` | 28 | 28 | 36 |
| R06b | ROUND FOUR'S LITERAL RULE 5, lifted verbatim from `HEAD~3` lines 2185 to 2187: a constant key in `FILESYSTEM_MUTATIONS`, no receiver and no owner read | not measured | 10 | 13 |

The author's own spelling reproduces its recorded 28 exactly. The attribution did
not: under round four's literal spelling the number is 10, and three of round
seven's 24 new tests survive it.

**The revision this text was lifted from is corrected.** Round seven wrote
`HEAD~2`, which was right when it was written and stopped being right the moment
the round committed: `HEAD~2` now resolves to round five. The text is verbatim
`HEAD~3:2185-2187`. A citation written as an offset from a moving head is the
same instability as a residual number, one file over, and this is the second one
this unit produced.

### The earlier rounds' rows, re-run against round seven's code

Every row is re-measured twice: once against the whole file, and once with
exactly the 24 new node ids DESELECTED, so a count that rose can be told apart
from a row that changed meaning.

| id | what was reverted | recorded | 24 new deselected | all tests |
|-|-|-|-|-|
| N21 | `mutations_in` stops descending into NESTED SCOPES | 91 | 91 | 105 |
| S16 | `_visible_bindings` adds the scope's own bindings BEFORE shadowing instead of after | 37 | 37 | 47 |
| R06 | rule 5 drops the namespace requirement | 28 | 28 | 36 |
| N12 | the ASSIGNMENT rebinding branch removed | 27 | 27 | 36 |
| M35 | `write_text` dropped from `FILESYSTEM_MUTATIONS` | 25 | 25 | 29 |
| Q06 | `ast.ClassDef` dropped from `_SCOPES` | 14 | 14 | 20 |
| S01 | `_names_taken` reverted to PARAMETERS ONLY | 11 | 11 | 11 |
| R02 | `_namespace_of` stops recognising `vars()` | 11 | 11 | 16 |
| S09 | `_bound_here` stops reading a PARAMETER LIST | 10 | 10 | 14 |
| C01 | `_called_keys` answers nothing | 8 | 8 | 8 |
| R05 | rule 5 reads its receiver INLINE again | 8 | 8 | 8 |
| Q01 | `_receiver_key` ignores the owning class | 7 | 7 | 12 |
| R01 | `_namespace_of` stops recognising `__dict__` | 6 | 6 | 7 |
| C05 | `_invoked_reads` stops reading a read BOUND TO A NAME the file calls | 6 | 6 | 6 |
| C09 | `_invoked_reads` stops reading the INLINE spelling | 5 | 5 | 5 |
| Q07 | `_walk_bindings` stops writing the `<Class>.<name>` attribute key | 4 | 4 | 6 |
| Q08 | `_walk_bindings` stops writing the `<Class>::self.<name>` key | 4 | 4 | 8 |
| U01 | `_invoked_reads` answers with EVERY reflective read | 4 | 4 | 4 |
| S15 | `_scope_own_bindings` inner fixed point cut to ONE pass | 4 | 4 | 4 |
| S14 | `_scope_own_bindings` accepts a name when ANY binding resolves | 3 | 3 | 4 |
| R07 | `_namespace_reads` stops reporting a key it CANNOT READ | 2 | 2 | 3 |
| R09 | `_call_mutations` drops the namespace ASKED branch | 2 | 2 | 3 |
| B09 | a computed `__getattribute__` gated on the reflection switch | 2 | 2 | 2 |
| R08 | `_namespace_reads` reports an unreadable key with the switch OFF too | 1 | 1 | 2 |
| Q16 | the audit stops naming a `ClassDef` as its own owner | 1 | 1 | 2 |
| R03 | `_mapping_operands` stops yielding a CALL's arguments (was: `_namespace_of` stops reading a `dict()` copy) | 1 | 1 | 2 |
| Q02 Q03 Q04 Q09 Q13 Q14 Q15 R04 R10 R11 R12 T01 T02 S20 S22 | unchanged, one death each | 1 | 1 | 1 |
| S21 | `_scope_own_bindings` stops recording a FAILED attempt for a binding `_binds` cannot read | 1 | **0** | 1 |
| S19 | `_walk_bindings` stops recording a function's RETURNED module | 2 | 4 | 4 |
| S18 | `_walk_bindings` stops carrying OBJECT bindings out of the scope that made them | 3 | 6 | 10 |
| Q11 | `_defined_here` stops reading a `ClassDef` | 1 | 4 | 11 |
| N05 | the rebinding sweep removed, imports only | 31 | 32 | 42 |
| N22 | `_receiver_module` answers an UNRESOLVED name with itself | 20 | 25 | 27 |

The last six need saying out loud rather than leaving in a column.

- **S21 is the one row in this file held ONLY by this round's new test.** Its
  middle column is 0, not the 1 it was grouped under: the single test it kills,
  `test_a_name_bound_twice_in_ONE_scope_settles_to_neither`, is one of round
  seven's own 24 new ids, so deselecting them leaves S21 killing nothing. Applying
  the same spelling to `HEAD~1` also kills 0. That is exactly what the middle
  column exists to separate, and grouping S21 into "unchanged, one death each"
  hid it. **Round eight is the reason this matters:** S21's rule is the one
  extended to the object half of the table, and the row that held it had no
  coverage older than the round that wrote it.
- **Q11 means more than it did.** `_defined_here`'s reading of a `ClassDef` now
  does two jobs: it takes the class's own name back, which is what round six's
  row named, and it is the loop through which a class's `_Class` binding is
  recorded. Reverting it removes both, so three class-attribute shapes that Q12
  used to hold fall to it as well. **Q12 is gone**, because the lexical class
  path it reverted no longer exists; its two drivers are now held by nine rows
  between them, P14 and P15 among them.
- **S18 and S19 rose against round five's figures before this round.** Round six
  did not re-run either. Applied to round six's own code and counted on round
  six's own tests, they measure 6 and 4, the same as here, so the rise is not
  this round's.
- **N05 measures 32 and N22 measures 25 with the same spelling on round six's own
  code and round six's own tests.** The recorded 31 and 20 do not reproduce. The
  cause is not this round: round six recorded no verbatim revert text for either
  row, so the exact spelling that produced those numbers cannot be recovered.
  What is measurable, and is measured, is the DELTA: applying this round's
  spelling to `HEAD` and to round seven gives the identical failing-id set on the
  old tests for both rows, so neither is inflated by this round. Round four's
  recorded N22 already did not reproduce against round four's own code, which
  makes this the second unrecoverable number on that one row.

### Three zero rows fixed rather than argued

- **P16 was not a missing driver, it was a worse reading.** The proposed guard
  recorded one attempt per `ClassDef` NODE, so two `class Keeper` statements in
  one scope disagreed and the name settled to neither. That measured zero,
  because the quiet direction it was written for is already quiet under the
  simpler reading, and it LOSES a real write: the second `class Keeper` really
  does bind the name, and the interpreter lets the last definition win. The
  simpler reading is what shipped, and the redefinition case is held by P13.
- **R14 and R16 overlapped on every fixture**, and the fix was to find where the
  two mechanisms come apart rather than to keep one. Written out above.
- **S21 had no driver at all and still does not, in round five's fixtures.**
  Every shadow fixture in this file puts the import at module level and the
  rebinding inside a function, and there `_names_taken` answers before the failed
  attempt is consulted. The failed attempt is the only thing that answers when
  both bindings are in the SAME scope, and
  `test_a_name_bound_twice_in_ONE_scope_settles_to_neither` is that: a handle
  bound to a name the module also imports, with the write that would otherwise be
  found asserted beside it.

### What was measured against the real tree, not against a fixture

- Every shape in F1, F2, F3 and F4 is appended to the REAL
  `src/cratekit/modules/reports/aging.py`, read from disk, and every one of the
  six findings was both found and driven that way.
- **75 files under `src`. ONE namespace expression in all of them**, `vars(obj)`
  at `src/cratekit/core/rb_writer.py` line 1840, and ZERO names bound to a
  namespace in any module level table. The one lookup through it is
  `state.items()`.
- **The no-argument ASKED branch costs exactly one finding across the whole
  tree**, and it is that `state.items()`, reported only with the reflection
  switch ON. `rb_writer` is neither a governed report module nor on the
  allowlist, so nothing asks it that question today; the audit, which runs with
  the switch off, is silent on it. The four governed modules contain no `vars`
  and no `__dict__` at all. Recorded as a residual rather than left implicit,
  under the title "A namespace method with no argument is an unreadable lookup".
- Real tree today: **4 governed modules walked, 0 offenders, 0 forbidden
  imports; 8 admitted modules, 7 audited with 0 unnamed writers**, the eighth
  skipped by exact name equality with `SANCTIONED_PERSISTENCE`.
- `MappingProxyType(vars(Path))["write_text"]` is now CAUGHT by the propagation,
  and its import is refused as well. `itemgetter` and `getattr_static` stay
  quiet, and each needs a module the allowlist refuses, so neither is live.
- One limit is unchanged and is not this round's:
  `self.mods = [config for _ in range(1)]` followed by `self.mods[0].save(cfg)`
  is quiet, because `_elements` has never read comprehensions. Round five missed
  it identically. Re-measured `[]` and recorded rather than chased.

### The conflict surface against `main`

Measured with `git merge-tree --write-tree main HEAD`, `main` at `183bea9`, which
is well past U32. **Five content conflicts, not none:**

| file | why |
|-|-|
| `docs/residual-findings.md` | append point registry, meant to conflict textually |
| `src/cratekit/cli/registry.py` | append point registry |
| `tests/_pending.py` | append point registry |
| `tests/test_pending_units.py` | append point registry |
| `src/cratekit/core/cause.py` | append point registry |

All five are the registries `CLAUDE.md` says are meant to conflict, so the merge
is resolvable, but "no conflict surface" was false and is corrected here.

[[collision-set]]
**RESIDUAL NUMBERS COLLIDE ACROSS THE MERGE, AND THE SET IS SEVEN.** Measured
against `git merge-base main HEAD`, `af1d7d2`: this branch adds `R-16` through
`R-25` to `docs/residual-findings.md`, and `main` independently added `R-14`
through `R-17` and `R-19` through `R-23`. **Seven** of this branch's numbers name
entirely different findings on `main`: `R-16`, `R-17`, `R-19`, `R-20`, `R-21`,
`R-22` and `R-23`. `R-18`, `R-24` and `R-25` do not collide today.

**Two of the seven were created by the round that wrote the warning.** Round
seven added `R-22`, `R-23`, `R-24` and `R-25`, and `main` already carried `R-22`
and `R-23` when it did. The statement it shipped said five and named `R-16`
through `R-21`, which was the set before round seven's own additions.

**ADDING A RESIDUAL ON A BRANCH IS ITSELF A COLLISION RISK.** Both sides append to
one file from one counter, so a number is only unique until the other side reaches
it: `R-18`, `R-24` and `R-25` are clear only because `main` has not got there yet,
and nothing stops it. A number is not an address on a branch. A title is.
[[/collision-set]]

Every residual citation in this unit's source, docstrings, tests **and docs** is
therefore written as a TITLE and never as a number, and
`test_this_units_residuals_are_cited_by_title_and_never_by_number` checks it
rather than asserting it. The earlier claim covered source, docstrings and tests,
was true of all three, and was false of the handoff document the same commit
wrote, which cited the report-verbs residual twice by number, at
`docs/HANDOFF.md:357` and `:366`. A claim checked over a smaller set than
it covers is the fourth recurring defect, so the check now reads `docs/` and the
passage above is the one delimited exemption.

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
| R06 | rule 5 drops the namespace requirement, comparing every constant subscript key against the mutation set THROUGH `_namespace_reads`, which still reads the owner and still reports a key it cannot read | 28 |
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
  `SANCTIONED_PERSISTENCE`, which the review-queue requirement licenses to write
  and which the audit skips by name.

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
