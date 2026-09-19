# R-239 mutation notes

Two tables, `r239-a.md` and `r239-b.md`, one light pass split in two so each
driver run finished inside the tool's 600 second ceiling. 21 rows, 20 killing,
null control 0 in each, every restore verified against `HEAD`. This is the
author's table, not an independent one.

Batch A mutates the opener and its probe: the `None` branch answered with each
constant and removed, both defaults put back to `True` and set to `False`, the
probe's return answered with each constant, and the header constant moved to a
nearby value. Every row kills. The two U55 rows that read ZERO for want of an
encrypted input, "the probe answers not encrypted" and its opposite, now kill 49
and 8 because the suite builds an encrypted disposable database.

Batch B puts each fixed call site back to the answer it gave, or gives a site
that already asked the defect's answer. Every row kills on
`test_no_caller_in_src_answers_the_key_question_for_itself`. Which BEHAVIOUR test
also dies is the finer reading:

- `route inbox`, `route unplaced`, `rebuild` and `converge` each also die on
  their encrypted drive through the command line.
- `route resort` dies with `rebuild`, because its worker opens through
  `rebuild_governed_tree`, not through `routing_cli.py:510`.
- `route pending`, `delete review`, `mytags`, the naming reader, `adopt apply`
  and the session read-back die on the source guard alone. The adoption reader
  also dies on its recorded call assertion. None of these is a zero, and the
  guard is what makes the argument impossible to reintroduce silently; a verb
  level encrypted drive for each was not written.

`A10_unreadable_answers_plain` is zero on the full suite and maintainer facing.
An unreadable file fails the open whichever answer the probe gives, so the
direction changes which refusal a person reads, not whether the open is refused.

One row considered and not run: the source guard and its forward exemption live
in `tests/`, and the driver mutates `src` only. Their refusals are driven by
literal sources instead, four spellings of an answered question, one open that
asks, and two exemption shapes that must not be exempt.
