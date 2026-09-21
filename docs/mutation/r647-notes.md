# R-647 mutation notes

One table, `r647-a`, over the cross boot judgment and the machine identity in
`core/session.py`. Seventeen rows, under the 25 row light cap, so nothing was
dropped. The author ran the table, and a zero would mean the author could not
kill it (METHOD, no independent verifier).

All seventeen killed on their subsets (485 collected for the three session
files, 146 for the two probe rows). No zero, so no row was promoted to a full
run.

Two rows were written after the table was drafted rather than before, and say
so here. Drafting B1 showed that no test compared two unknown machine
identities, which are equal as text, and drafting B5 and B6 showed that nothing
told a margin of sixty seconds from thirty or a hundred and twenty. Both tests
landed in `9ddd64b`, before the driver ran.

B11 is the round one review finding put back: comparing a live identifier's
start time with the recorded one. It kills one test, the Linux shape of a
stepped clock, which is written with a start time that moved by the same day as
the boot. That test is a model of psutil's Linux behaviour, not a measurement on
Linux: this suite runs on macOS, where a process start time does not move with
the clock.

B12 restores the rule before this unit, every other boot judged alive, and kills
four tests including the end to end power loss test in
`tests/test_session_cli.py`, which is the ledger entry's cost reproduced.
