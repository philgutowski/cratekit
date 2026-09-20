# U96 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/141`. Two files and not one because the driver
runs in the foreground under a ten minute tool ceiling, and a zero row costs a
full suite run. Null control 0 of 9359 in both, no collect drift, every restore
verified against `git show HEAD`.

**`u96-a.md`**, 16 rows over the recovery verb in `session/restore_cli.py`, each
with `tests/test_restore_cli.py` as its subset. All 16 killed. They cover the
acceptance flag at both layers, the held session on the plan and on the run, the
mirror being pulled, the plan being spent a half at a time, the second rekordbox
check, the skipped database half, the rehearsal flag, the rerun step on both of
its edges, which half a failure names, the completed halves, the required
target, and the two report fields for a database that was never on the volume.

**`u96-b.md`**, 6 rows: the registry entry's absent library check, and a fixed
SAMPLE of five engine guards in `core/restore.py`, which are not this unit's
diff and are here because this unit is their first caller. All 6 killed, on the
second run.

22 rows in all, under the cap of 25. Nothing was dropped to fit. Not mutated and
worth saying: `target=held.authorises` against the raw argument, because the two
are equal by construction and no test could tell them apart, and the wording of
the rekordbox sentence, which one assertion holds by substring.

## The one zero, and it was the important one

**C5 killed nothing on the first run, subset and full suite both.** The mutation
makes `assert_library_volume_is_gone` answer "gone" for a library that is
mounted and is the recorded volume. That is the gate that keeps a bare metal
recovery apart from a live restore, and its own docstring says so in capitals.

Three tests assert that refusal, one in the engine's suite since it landed and
two of this unit's, and all three passed under the mutation. Each used a target
beside the configured root. The stub check refuses that shape too, and its
sentence says the target is "the empty folder an unmounted volume leaves
behind". The assertions looked for the word "mounted". So the stub check was
holding up all three, and the identity gate was covered by another guard, which
is METHOD's "a guard covered by another guard is a guard nothing covers", found
through a substring rather than through the code.

The repair was to the tests. The mount probe answers yes in all three, so the
stub check cannot be what refuses, and each assertion names the identity gate's
own sentence. The table in the repository is the second run: C5 kills 3. The
first run's table was not kept, and this paragraph is its record.
