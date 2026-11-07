# Reading the r1383 mutation table

`r1383.md` measures 19 rows at `b0c08ad3`, net of the container's 161 machine
bound failures, the null control killing none. Seventeen are over the code
R-1383 added to `src/cratekit/sync/pair_cli.py` and two sample U229's landed
steps beside it (M18, M19). 16 were killed and three read zero.

- **M8** (the held tracks left out of the pair's digest, user facing) and
  **M9** (the key put in every digest, maintainer) read zero on the full
  suite: nothing pinned that the hold binds the gate, or that a pair holding
  none digests as before. A direct test on the pair's identity, in the form
  U221's hold uses, was added at `818cbf25`, and both rows were measured again
  alone in `r1383-digest.md`: each killed, one kill on 145 collected.
- **M11** (the warning's scan read whether the plan looked or not,
  maintainer) reads zero: with every record readable the forced read says
  nothing, and with one unread the plan has already read the scan whenever a
  track reached the hold. Its cost is one log read on a plan with nothing
  lacking.

M14 and M15, the order of the hold behind awaiting and a twin's hold, are the
two round one of the review measured at zero; the fix round's tests kill them.
Every row is the author's.
