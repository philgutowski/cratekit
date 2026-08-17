---
title: A mapping that carries the key bpm is a grid write
date: 2026-08-17
category: workflow-issues
module: tests/test_no_beatgrid_ever.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - An analysis detector is about to return a dict that includes a tempo reading
  - A structured payload is being serialized and the domain attribute is named bpm
  - A string constant under src/ is about to contain a grid token or end in AverageBpm="
  - test_no_module_in_the_package_emits_a_grid is red on a module that writes no tag and no XML
  - A new dict literal under src/ is being keyed with a word from FORBIDDEN_TAG_KEYS
symptoms:
  - test_no_module_in_the_package_emits_a_grid fails
  - The message says the module builds a mapping carrying the tempo key bpm
  - Nothing wrote a file tag or a TEMPO XML element
  - A docstring that interpolates AverageBpm or contains a grid token fails the same guard
  - The whole suite is red because R17 is absolute
related_components:
  - testing_framework
  - documentation
tags:
  - r17
  - beat-grid
  - forbidden-tag-keys
  - ast-walk
  - dict-literal
  - tempo-key
  - guard
  - source-scan
---

# A mapping that carries the key bpm is a grid write

## Context

R17 is the one rule in this package with no configuration flag. Nothing here
writes a beat grid. `tests/test_no_beatgrid_ever.py:1-35` states the reason
and names the five surfaces the suite guards. A wrong grid is worse than no
grid. The detector octave-folds, so a helpful BPM seeds a grid at half or
double time, and every cue point and every loop the user has set against that
track moves. Import gridless and rekordbox derives BPM and grid from the
audio alone.

The five surfaces at `tests/test_no_beatgrid_ever.py:13-30` are:

1. A tempo child element in COLLECTION XML.
2. A real `AverageBpm` in COLLECTION XML. Tracks import with
   `AverageBpm="0.00"` so rekordbox analyses from scratch.
3. A `bpm` or `TBPM` file tag. rekordbox reads file tags on import, so a
   tag write reaches the same place by a longer route.
4. The analysis columns of the database, asserted in
   `tests/test_rb_writer_guard.py`.
5. The ANLZ analysis files on disk.

U25, issue #25, landed `cratekit.analysis.detect`. `analyse_file` measures a
tempo from audio and returns a mapping the rest of the analysis pipeline
consumes. The first return was shaped like `{"bpm": n}`.
`test_no_module_in_the_package_emits_a_grid` at
`tests/test_no_beatgrid_ever.py:230-239` went red. Nothing had written a
mutagen tag. Nothing had emitted XML. The live half of the guard walks every
`src/*.py` through `beatgrid_emission_violations`
(`tests/test_no_beatgrid_ever.py:138-216`) via `_package_modules` (`:219-227`),
which starts at `SRC_ROOT` (`:50`) and never opens `tests/`. The failing
construct was the dict literal in production source.

The dict-literal rule is `tests/test_no_beatgrid_ever.py:205-215`. For every
`ast.Dict`, each constant key is checked against `FORBIDDEN_TAG_KEYS`. A hit
produces the message "builds a mapping carrying the tempo key". The fixture
that pins this shape is `tags.update({'bpm': 124})` at `:259`, labeled
"mapping carrying the tempo key". The comment above the rule (`:205-207`)
says why a separate construct exists: a tempo key inside a dict literal
reaches a tag store through `update(...)` or a keyword-expanded call without
ever being a subscript assignment. The subscript rule at `:170-181` cannot
see it.

`FORBIDDEN_TAG_KEYS` at `tests/test_no_beatgrid_ever.py:64-72` is the set
that makes a mapping a grid write. It includes `bpm`, `BPM`, `Bpm` (Vorbis
comments and loose callers), `TBPM` (the ID3v2 tempo frame by name), `tmpo`
and `TMPO` (the MP4 and M4A tempo atom), `beatgrid` and `beat_grid`, and
`AverageBpm` and `averagebpm` (the rekordbox field by any route). Carrying
any of those spellings as a dict key under `src/` is the violation, even when
the mapping is an internal payload that never reaches mutagen.

The shipped return is now
`{"path": path, "camelot": camelot, "rate": bpm, "energy": None}` at
`src/cratekit/analysis/detect.py:85`. The measured number is still the local
name `bpm`. The key that leaves the function is `rate`.

`src/cratekit/analysis/run.py:50` still accepts both keys:
`payload.get("bpm", payload.get("rate"))`. Tests inject a detect callable
into `run_batch` and never reach `analyse_file`
(`src/cratekit/analysis/detect.py:48-49`). Those injectors live under
`tests/`, so the source walk cannot see them, and they may still return a
mapping keyed `bpm`. The Result constructor reads the old key first and
falls back to `rate`, so injected tests keep working while production source
stays off the forbidden set.

The Result field itself is still named `bpm`.
`src/cratekit/analysis/run.py:26-34` declares `class Result` with
`bpm: int | None = None` at `:30`. That is an attribute name. The walk looks
at string keys and subscripts, not attribute names.

The `detect.py` module docstring at `src/cratekit/analysis/detect.py:1-7` was
reworded so the source does not contain a grid token or an interpolating
`AverageBpm="` prefix. Hash comments are not in the tree. A module
docstring is a string constant. Bare `TEMPO` or `AverageBpm` in a hash
comment does not fail. `src/cratekit/intake/collection_xml.py:36` still
names `AverageBpm` in a hash comment and is legal. The tokens that fail
are `<TEMPO`, `Battito`, `Metro=`, and `Inizio=` (`:54`), or a string whose
stripped value ends in `AverageBpm="` (`:163-168`).

This is the same file, a different construct, from the U37 neighbour. U37,
issue #37, landed `cratekit.intake.collection_xml`, the COLLECTION TRACK
emitter. That unit hit the string-literal half of
`beatgrid_emission_violations`. The token rule at
`tests/test_no_beatgrid_ever.py:157-161` flags any string constant containing
a member of `FORBIDDEN_TOKENS` (`:54`). The interpolation rule at `:163-168`
flags any string constant whose stripped value ends in `AverageBpm="`,
because the value that follows is interpolated and is therefore not the
gridless constant. The fixture for that shape is `:248`. The only legal
`AverageBpm` value is `GRIDLESS_AVERAGE_BPM = '0.00'` at `:130`. The
emitter writes that value at `src/cratekit/intake/collection_xml.py:101`
and names the constant at `:36-38`. U37 was string literals and
interpolation. U25 is a dict key.

## Guidance

Never put a `FORBIDDEN_TAG_KEYS` spelling as a dict key in `src/`, even in
an internal payload that never reaches mutagen. Use `rate`, or another word
that is not on the list. The set at `tests/test_no_beatgrid_ever.py:64-72` is
the list. `bpm`, `BPM`, `Bpm`, `TBPM`, `tmpo`, `TMPO`, `beatgrid`,
`beat_grid`, `AverageBpm`, and `averagebpm` are all on it. A mapping handed
to a tag writer writes just as surely as a subscript does. The scan does not
ask whether the mapping later reaches mutagen. It asks whether the source
built a mapping that carries the key.

Reading a bpm tag is legal. Writing or carrying the key is not.
`test_reading_a_bpm_tag_is_not_a_violation` at
`tests/test_no_beatgrid_ever.py:289-296` pins the read side: `tags.get('bpm')`
and `tags['TBPM']` produce an empty problem list. A guard that forbade
reading would make key detection impossible and would be worked around
within a week, which is worse than no guard.

`Result.bpm` as an attribute is fine. The walk looks at string keys and
subscripts, not attribute names. `src/cratekit/analysis/run.py:30` keeps the
domain word on the dataclass. An attribute cannot be splatted into a tag
call. The serialized key is the thing that can.

`payload.get("bpm")` is a read. The string appears as an argument to `.get`,
not as a dict-literal key and not as a subscript assignment.
`src/cratekit/analysis/run.py:50` uses that shape on purpose so injected
tests that still return the old key keep working. Do not take that fallback
as permission to emit the old key from production source.

The same decision already exists at another serialization boundary.
`src/cratekit/modules/tools/setbuilder.py:888-897` states that the
structured payload field is called `tempo`, not `bpm`, and that this is an
R17 decision rather than a matter of taste. `as_payload` at `:904` writes
`"tempo": plan.anchor.bpm`. `_scored_payload` at `:920` does the same.
`tests/modules/test_tools.py:817-841` imports `FORBIDDEN_TAG_KEYS` from the
invariant suite and asserts that no key in the set-builder payload
intersects that set. When a new serialized mapping leaves `src/`, pick a
word that is not a tag spelling, and if the mapping is load-bearing, assert
the forbidden set against it the way the set-builder does.

Do not invent a second spelling of the gridless constant.
`GRIDLESS_AVERAGE_BPM = '0.00'` at `tests/test_no_beatgrid_ever.py:130` is
the only legal `AverageBpm` value. It is a string, not a number, because the
XML attribute is compared as bytes.
`test_the_gridless_constant_is_not_a_violation` at `:283-286` pins the legal
emission. An interpolated value, even when it happens to be `0.00` at
runtime, fails the suffix rule at `:163-168` because the source no longer
contains the constant.

When writing comments or docstrings under `src/`, do not paste the grid
tokens or an interpolating `AverageBpm="` prefix.
`beatgrid_emission_violations` walks `ast.Constant` string values
(`:156-168`). A docstring is a string constant. A hash comment is not in
the tree. U37 taught the interpolation and token half of this scan. The
`detect.py` docstring at `src/cratekit/analysis/detect.py:1-7` is
conservative wording, not proof that the words `TEMPO` or `AverageBpm`
are themselves forbidden.

If `test_no_module_in_the_package_emits_a_grid` goes red, do not loosen the
assertion. The module docstring at `tests/test_no_beatgrid_ever.py:37` says
so. Rename the key, reword the literal, or stop building the mapping. The
rule is the product.

## Why This Matters

The scan is a source scan rather than an output check
(`tests/test_no_beatgrid_ever.py:141-143`) because it holds for code that
has not been written yet, and because it catches the emitter that would
only fire on some rare branch nobody thought to test. A green suite written
by the author of a dict keyed `bpm` will not see the problem. The author
did not write a tag. The author did not emit XML. The mapping still failed,
and it was right to fail.

Surface 3 is the reason a dict key is enough.
`tests/test_no_beatgrid_ever.py:18-19` says rekordbox reads file tags on
import, so a tag write reaches the same place a grid element does. A
mapping spelled the way a Vorbis comment spells it is one copy-paste from
being handed to a tag writer. `src/cratekit/modules/tools/setbuilder.py:888-897`
states the same cost in the other direction: the invariant guard treats any
mapping carrying that key as a violation, and the cost of being wrong is a
grid seeded at half or double time, which moves every cue point the user
has ever set.

The set is per-container (`tests/test_no_beatgrid_ever.py:59-63`) because a
tempo tag is spelled differently in each container, and a guard that knows
only one spelling protects only one container. Vorbis and Ogg use `BPM`.
ID3 uses the `TBPM` frame. MP4 and M4A use the four-letter atom `tmpo`,
which resembles nothing else on the list and is the reason a key set
assembled by intuition misses it. U25 did not write a tag in any of those
containers. It wrote the Vorbis spelling as an internal key. That is
already the thing the dict-literal rule exists to stop.

U13 is the earlier proof that the scan has to name every construct, not
just the obvious write. `tests/test_no_beatgrid_ever.py:74-84` records that
the downloader vendored in U13 wrote the provider's tempo into every file
it saved, at three sites in one module, and the original guard caught
exactly one of them: the Vorbis subscript. The ID3 site was
`tags.add(TBPM(...))` and the MP4 site keyed on `tmpo`. Both would have
shipped. `FORBIDDEN_FRAME_CONSTRUCTORS` (`:85`) and the `tmpo` members of
`FORBIDDEN_TAG_KEYS` closed those two. The dict-literal rule at `:205-215`
closes the third shape, a mapping that never becomes a subscript.

The read and write distinction is load-bearing. Analysis legitimately
computes tempo from audio. `src/cratekit/core/tags.py:40-47` has no tempo
field in `FIELDS` and `write_tags` raises on any field name it does not
know, so there is no code path from the public tag surface to a tempo
frame. That structural hole is the write side. The read side stays open
because a guard that forbade `tags.get('bpm')` would make key detection
impossible and would be worked around within a week
(`tests/test_no_beatgrid_ever.py:292-293`). Collapsing the two sides into
one ban would force a workaround. Keeping them apart is what makes the
rule survivable.

## When to Apply

Apply this whenever a new dict literal is added under `src/`, especially a
return value, a payload, or anything that will later be handed to `update`,
to a tag writer, or to a keyword-expanded call.

Apply it when naming a field that holds a measured tempo. The domain word
on a dataclass or an attribute can stay `bpm`. The serialized key cannot.
Check the candidate key against `FORBIDDEN_TAG_KEYS` at
`tests/test_no_beatgrid_ever.py:64-72` before it lands. If the mapping is a
public or CLI payload, import that set in the unit's tests the way
`tests/modules/test_tools.py:826` does, rather than restating the list.

Apply it when writing comments, docstrings, or examples under `src/`. The
U37 neighbour failed on string literals and interpolation in the same
scan. Do not paste `<TEMPO`, `Battito`, `Metro=`, or `Inizio=` into a
string constant. Do not write a string whose stripped value ends in
`AverageBpm="`. A hash comment that names `AverageBpm` is fine. The
gridless constant at `tests/test_no_beatgrid_ever.py:130` is the only
legal `AverageBpm` value. Prefer the wording in
`src/cratekit/analysis/detect.py:1-7` when the sentence is about the
rule itself.

Apply it when a test injects a detect callable that returns a mapping.
Injectors under `tests/` are not walked. Production source is. Keep the
dual-read at `src/cratekit/analysis/run.py:50` if injectors still use the
old key. Do not copy the old key back into
`src/cratekit/analysis/detect.py` to make the two sides look the same.

Apply it when reviewing a green analysis or intake suite that never opens
mutagen and never builds XML. That is the situation U25 was in. The live
half of the guard is `test_no_module_in_the_package_emits_a_grid` at
`tests/test_no_beatgrid_ever.py:230-239`. Run it. A mapping carrying a
forbidden key will fail there and nowhere else.

Do not apply this as a ban on reading. `tags.get('bpm')` is legal.
`tags['TBPM']` is legal. A local variable named `bpm` is legal.
`Result.bpm` is legal. `plan.anchor.bpm` is legal. The walk does not look
at those.

## Examples

Illegal in `src/`. A production detector returns the Vorbis spelling as a
key. This is the U25 failure. The dict-literal rule at
`tests/test_no_beatgrid_ever.py:205-215` reports "builds a mapping carrying
the tempo key `'bpm'`".

```
return {"path": path, "camelot": camelot, "bpm": bpm, "energy": None}
```

Legal in `src/`. The same number, a key that is not on `FORBIDDEN_TAG_KEYS`.
This is `src/cratekit/analysis/detect.py:85`.

```
return {"path": path, "camelot": camelot, "rate": bpm, "energy": None}
```

Illegal by fixture. A mapping that never becomes a subscript, handed to
`update`. Pinned at `tests/test_no_beatgrid_ever.py:259`.

```
tags.update({'bpm': 124})
```

Legal read. Analysis reading a file tag. Pinned at
`tests/test_no_beatgrid_ever.py:289-296`.

```
value = tags.get('bpm')
existing = tags['TBPM']
```

Legal attribute, legal dual-read. The Result field keeps the domain word.
The constructor accepts the old key from injectors and the new key from
production. This is `src/cratekit/analysis/run.py:30` and `:50`.

```
bpm: int | None = None
...
bpm=payload.get("bpm", payload.get("rate"))
```

Legal serialization at another boundary. The dataclass attribute is `bpm`.
The payload key is `tempo`. This is
`src/cratekit/modules/tools/setbuilder.py:904` and `:920`.

```
"tempo": plan.anchor.bpm
```

Illegal interpolation, the U37 neighbour. The constant prefix ends in
`AverageBpm="`, so the value that follows is not the gridless constant.
Pinned at `tests/test_no_beatgrid_ever.py:248` and flagged at `:163-168`.

```
X = f'<TRACK AverageBpm="{bpm}"'
```

Legal `AverageBpm` emission, the U37 neighbour. The only legal value,
written as a string, not interpolated. Pinned at
`tests/test_no_beatgrid_ever.py:130` and `:283-286`, emitted at
`src/cratekit/intake/collection_xml.py:101`.

```
Year="0" AverageBpm="0.00"
```

Legal docstring wording after the reword. This is
`src/cratekit/analysis/detect.py:1-7`. It states the rule without containing
`TEMPO` or `AverageBpm`.

```
Read-only detectors. Tempo is measured. It is never emitted as a grid.
```

## Related

- U25, issue #25, is the landing. `cratekit.analysis.detect` now returns
  `rate`. `cratekit.analysis.run` still accepts `bpm` from injectors.
- U37, issue #37, is the neighbour in the same scan file. String constants
  that interpolated `AverageBpm="` or contained a grid token failed
  `beatgrid_emission_violations`. The constant
  `GRIDLESS_AVERAGE_BPM = '0.00'` at `tests/test_no_beatgrid_ever.py:130`
  is the only legal `AverageBpm` value. U37 was string literals and
  interpolation. This learning is a dict key. Same file, different
  construct.
- U13 is the earlier construct gap in the same file. The original guard
  caught a Vorbis subscript and missed `TBPM(...)` construction and the
  `tmpo` atom. `FORBIDDEN_FRAME_CONSTRUCTORS` at
  `tests/test_no_beatgrid_ever.py:85` and the `tmpo` members of
  `FORBIDDEN_TAG_KEYS` closed those. The dict-literal rule is the same kind
  of closure for a mapping that never becomes a subscript.
- `src/cratekit/modules/tools/setbuilder.py:888-897` and
  `tests/modules/test_tools.py:817-841` already apply the serialized-key
  half of this rule at the set-builder payload boundary, using `tempo`
  rather than `bpm`.
- `src/cratekit/core/tags.py:40-47` is the structural write-side hole:
  `FIELDS` has no `bpm` key and no `TBPM` frame, and `write_tags` raises on
  any field name it does not know.
- `src/cratekit/intake/collection_xml.py:36-38` and `:101` are the U37
  emission of the gridless constant.
- R17 itself is stated at `tests/test_no_beatgrid_ever.py:1-37`. If any
  test in that file goes red, do not loosen the assertion.
