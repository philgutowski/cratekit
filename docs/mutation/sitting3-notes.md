# Sitting 3 mutation table: measured

**Verdict.** Sixteen rows over the R-370 and R-371 fixes and the review's
fix round, measured by `scripts/mutate.py` on the committed tree at
`9613489`. Fifteen killed, one zero. Null control 0 of 7557. Baseline
collected 7557. The driver ran attended, in one background call that the
session waited on with nothing edited meanwhile.

The author ran the driver. Every zero reads as the author could not kill it.

## What killed

G1 and G2 hold the read by name: a model with no table, or a table missing
a target, is refused rather than read at the first three columns. G4 holds
the frame wrapper against the clip one. G5, G6 and G8 hold readiness: the
loader asks before the library is asked, the label table is checked before
the extra is imported, and the queue refuses a job that could score
nothing. G7 holds the wrapper's chatter off stdout. G9, G10, G11, G14 and
G15 hold the chunk floor: a short tail folds rather than going alone or
being dropped, a lone clip pads on both paths, and the floor rather than
the chunk size decides a fold. G12 holds the columns resolved once at
load. G13 holds the trim of padded frames. G16 holds torch imported for
real at the readiness check.

## What did not

G3 drops `class_idx=columns` from the call in `vocals.analyse`. After the
fix round `infer_frames` resolves the columns from the model's label table
when none are passed, so the mutant and the original compute the same
columns from the same model and the mutation is EQUIVALENT: the cached
value saves a lookup per track and changes no output. Reclassified from a
user facing zero to an equivalent mutation. A composite is not owed for an
equivalent row.

## The battery this table sits on

The driver's preflight ran the full suite twice on `9613489`, 7557
collected, green, before any row was applied.
