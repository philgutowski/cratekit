# Mutation tables for item 4 of the five-places residual, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/171`. The unit closes the fourth item of the
residual finding titled "Five places where", the one about an unreadable
presence index answering as nothing recorded.

**`r118-a.md`**, 12 rows over `core/secrets.py` at `b4a2e6e`, subset the nine
test files importing `cratekit.core.secrets`, null control 0 of 9127, no collect
drift, every restore verified against `git show HEAD:`. 11 killed, one zero.

**`r118-b.md`**, 6 rows at `b4a2e6e`, one over `core/cause.py`, three over
`cli/setup.py` with `tests/test_doctor.py` as their subset, and two over the
existing guards around the credential cycle in `core/secrets.py`. Null control 0
of 9127, no collect drift, every restore verified. 5 killed, one zero.

**`r118-c.md`**, the two zero rows re-measured at `449c25d` after the test they
were both missing was written. Null control 0 of 9128, every restore verified.
Both killed.

18 distinct mutations and two re-measures, 20 driver rows against the cap of 25.
Nothing was dropped for the cap.

## The two zeros had one cause between them

- **A7, the remedy the unreadable branch declares**, substituted for
  `set-credential`, the advice this whole finding exists to stop. Killed nothing.
- **B1, the exit code `credential-index-unreadable` maps to**, moved from
  `PRECONDITION` to `INTERNAL`, so a sidecar the person can repair is reported as
  a defect to file. Killed nothing.

Both are user facing, so under `docs/METHOD.md` each owed a composite. Neither
needed one, because looking at them found the gap rather than an inert mutation.

`cause.classified` replaces the slug and the remedy of any refusal whose DECLARED
cause chain carries an EACCES or EPERM `OSError`, which is right and is the
machinery the third item of the same finding bought. Every test reaching the
unreadable branch reached it by patching a read to raise `PermissionError`, so on
every path the suite covered, the branch's own slug, act and code were discarded
before anything could observe them. The mutations were not inert. They were
unreachable through the arrangement the suite happened to use.

An index path that is a DIRECTORY raises `IsADirectoryError`, errno 21, which no
classification claims. `test_an_index_refused_for_something_other_than_a_permission_keeps_its_own_act`
drives that on a real filesystem, with no patched reader at all, and pins the
slug, the remedy and the reserved code. `r118-c` then kills A7 at 1 and B1 at 2.

That is worth carrying past this unit: a zero on a guard that sits under a
classification layer may be measuring the layer rather than the guard. Ask which
arrangement the suite reaches the guard through before writing a composite.

## What the kills say

The three states are held apart from three directions. Reverting the whole reader
to the old blanket (A1) kills 10. Removing only the ENOENT leg, so a fresh
installation refuses and cannot be set up, kills 171, which is the largest number
in the table and the right shape: the empty answer for a missing index is load
bearing for most of the suite, and it is the half of this fix that had to stay.
The JSON half (A3, 2) and the wrong shape half (A4, 1) each kill on their own, so
neither leans on the other.

The refusal's parts are pinned individually. Dropping the path from the sentence
kills 3, dropping `from exc` so the classification cannot see the kernel's own
refusal kills 3, and collapsing the `damaged` detail into `unreadable` kills 1.

The caller's sentence about the two stores is held per position in the cycle:
the record half using the read sentence kills 1, the remove half using the record
sentence kills 1, and rewording the record sentence so it no longer says the
value reached the keychain kills 1. Those three are the code review's first
finding, and they were written as rows because a message that lies about which
stores were touched is the same class of defect as an answer that lies about what
is recorded.

Both wizard legs kill, the probe at 2 and the write at 1, and the write leg is
the one the first fix round missed. Reporting the probe's refusal as INFO rather
than FAIL kills 2, so setup cannot go quiet over a question it could not answer.

The fixed sample of existing guards both kill: recording the name before the
keychain read back (1), and removing the keychain entry before the index entry
(6), which is the order that once made `exists` answer True for a credential that
was gone.
