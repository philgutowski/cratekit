# U25 mutation table: measured

**Verdict.** Twenty five rows over the two new shells, measured by
`scripts/mutate.py` in 6131 seconds on a committed tree at `92f8174`.
Eleven killed, thirteen zero on the full suite, one refused. Null
control killed 0 of 7401. Baseline collected 7401.

The author ran the driver. Every zero reads as the author could not
kill it. None has a composite, which METHOD wants for a user facing
zero. That gap is R-341.

## What killed

G1, G3, G4, G20 hold the extras refusal. G6 holds the unchanged rewrite.
G10 and G11 hold the with-vox cut. G12 and G13 hold plan versus apply.
G15 holds `watch_roots` against a hand listed Music folder, promoted
onto the full suite, and the death is
`test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers`.
G24 holds that the apply does not write Rating.

## What did not

G2 is the worker extras check. The queue check (G1) is what a slim
install meets, so dropping the worker copy kills nothing the suite
drives. G9's default cut is unused: the fixture is at voxlevel 80.
G14's closed flag is patched true in every apply test. G7, G8, G16,
G17, G18, G19, G21, G22, G23 name producers the new tests do not
construct.

G25 refused: the old extras message as typed in the row file was not
the file's text, so the mutation never applied.

## The battery this table sits on

7399 passed and 1 skipped after the pin commit, then one more test
landed (the missing My Tag template through the dispatcher) before
the driver ran, which is why the baseline collected 7401.
