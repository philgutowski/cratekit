# U77 mutation tables, read

Four tables. All are the author's own, not independent, and all were measured
by `scripts/mutate.py` on `relay/122`. They are batches rather than one table
because Relay runs every command in the foreground and a 25 row table can pass
the harness ceiling of 600 seconds. Each batch took about three minutes.

**`u77-a.md`**, 9 rows at `b00bd17`, cover the landing engine's guards before
and during the match: the label source filter, the engine's own stale check,
the check made before the first move, the mapping of the writer's defect reason
onto the person's export, the needs review guard, the no landed file guard, the
year guard, the library's name template and the filter to this run's placed
files. The null control killed 0 of 8182, with no collect drift. All 9 killed.

**`u77-b.md`**, 8 rows at `b00bd17`, cover what happens after the moves and in
the tree writer: the deduplicated report, the disk refusal that is reported and
not raised, the index refusal, the single registry read, the unmatched
sentence, the trial id, the empty catalog return and the write order. The null
control killed 0 of 8182. All 8 killed.

**`u77-c.md`**, 8 rows at `b00bd17`, cover the manifest reader and the verb: the
version check, the two boolean tests, the not a manifest refusal, `source_refs`,
the manifest bytes in the gate's digest, the fingerprint handed to the engine
and the warnings for unfiled rows. The null control killed 0 of 8182. All 8
killed. Its `[[dropped]]` block logs four rows considered and ranked below the
cap, with the reason for each.

**`u77-a2.md`**, one row at `7e7a40e`, is `A2_engine_stale_digest` measured
again, so the count stays at 25. The first mutation inverted the test for a
fingerprint being given, which refused every landing that gave none, and 19
tests died for a reason that was not the guard. The second compares the
fingerprint with itself, so only the guard is gone. It kills 1,
`test_a_manifest_rewritten_after_it_was_fingerprinted_is_stale_and_moves_nothing`.
The 19 is recorded as a driver mistake of the author's, not as coverage.

25 rows, 25 killed, no zero. Every row's `head_verified` is true and
`git status` was clean after each batch.

Two rows are a pair on purpose. `C6_gate_manifest_bytes` removes the gate's
check of the manifest's bytes and `A2` removes the engine's, each alone. Both
refuse with `decision-stale`, so before this unit's last test commit one verb
test satisfied by either layer was a test of neither. The verb test now asserts
the gate's own detail and the engine's check is driven through `landing.apply`.

An author's table says the author could not find a guard that kills nothing.
METHOD's measured gap applies: independent tables have found more.
