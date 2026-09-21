# R-395 mutation notes

The author's own table, 11 rows in `r395.md`, under the 25 row cap. Every row is
a guard this unit added or a call site it moved onto the one source. All eleven
were killed on their subset, so none was promoted to a full suite run.

| Group | Rows | Killed | Zero |
|---|---|---|---|
| environment detection and the two forms, M1 M2 M4 | 3 | 3 | 0 |
| the pipx record, M3 M5 M6 M7 M8 | 5 | 5 | 0 |
| the three call sites back on a literal, M9 M10 M11 | 3 | 3 | 0 |

M7 is the built in review's finding reintroduced: a fallback that drops the
recorded extras kills one test,
`test_a_moved_clone_still_keeps_the_extras_pipx_recorded`, written in the fix
round.

M9 to M11 each kill the existing assertion that now compares the surface to
`extras.install_command`. Those assertions confirm the call site reads the one
source; the exact strings are pinned in `tests/test_install_command.py`.

Not measured: the regular expression that splits a recorded source from its
extras. Its failure shape, a spec it cannot split, falls back to the `.` form,
and M5 and M6 already measure both sides of that choice.
