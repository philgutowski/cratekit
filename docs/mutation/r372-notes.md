# R-372 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/98` in the foreground. Every row's subset was
the unit's own file, `tests/test_paths_resolved.py`, with `tests/test_metadata_cli.py`
and `tests/test_doctor.py`, and the declaration row added `tests/test_cli_contract.py`.

**`r372-a.md`**, 12 rows over `write/metadata_cli.py`, `core/cause.py` and
`core/rb_writer.py` at `1c594ff`, null control 0 of 9924, no collect drift,
every restore verified against `git show HEAD`. All 12 killed.

**`r372-b.md`**, 13 rows over `cli/doctor.py`, `cli/setup.py` and
`cli/registry.py` at `14c6385`, null control 0 of 9924, every restore
verified. All 13 killed.

25 rows in all, at the cap. Two more were considered and logged as dropped in
`r372-b-rows.toml`: the refusal's wording, which no test pins beyond the counts
and prefixes A7 and the plan test already hold, and the other ten declarations
of the check, of which one is measured in B12 and the unplaced report's is
pinned by its own test.

## Two rows that did not measure the first time

- **A12, the separator.** Refused: the row's old text was retyped with the
  backslash doubled once more than the file spells it. Copied out of the file,
  it kills 7.
- **B4, the volume checks before the read.** Refused: its two lines are shared
  with the taxonomy check, so the site was ambiguous. Widened by the line above
  them, it kills 1.

## The one zero, and what it bought

- **B7, the wizard skipping its own process question.** Zero on the first run,
  because the copy's own assertion refused underneath it and the note that
  refusal produced contained the word the test looked for, `running`. The test
  now asks for the wizard's own sentence, "none was taken and no drive rule was
  offered", and B7 kills 1. **B13 is the composite**: the wizard's question gone
  AND the copy's assertion gone, and the opener spy kills it, so the copy is
  never taken under a running application with either layer alone or with
  both removed.

## What the kills say

The rule is held from both sides of the boundary, A1 at half and A2 at the
coefficient, and from the definition of unmapped, A3, which 17 tests kill
because every fixture with pathless rows would refuse under it. The verb's
refusal is held on the plan, A4, and on the apply alone, A5. The slug's code, A9,
the remedy, A7, and the envelope's outcome beside its cause, A8, are each held.

Doctor is held on the majority, B1, the minority, B2, the process question, B3,
the volume checks, B4, and the copy against the live path, B5, which the opener
spy kills 4 times. Setup is held on every branch that offers nothing, B6, B7,
B8, B9, and on the two things the offer writes, the token, B10, and the answer,
B11.
