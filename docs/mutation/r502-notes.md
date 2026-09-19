# R-502 mutation table, summary

The author's own table, run with `scripts/mutate.py` on `relay/183`,
2026-09-19. Every zero below reads "the author could not kill it" and nothing
stronger. Full rows are in `r502-a.md`, `r502-a2.md`, `r502-b.md` and
`r502-b2.md`, with the row data beside them.

Twenty one runs over nineteen rows: seventeen over this unit's new guards, two
over existing guards of the same verb, and two reruns after a test was fixed.
Under the cap of 25, so nothing was dropped.

| Row | Guard | Surface | Deaths |
| --- | --- | --- | --- |
| G1 | the recheck call in `_listed` | user | 9 |
| G2 | a row now MATCHED is not kept | user | 6 |
| G3 | a row now SUPPRESSED is not kept | user | 2 |
| G4 | a row now NEEDS_REVIEW is not kept | user | 1 |
| G5 | a question the library raises is adjudicated | user | 1 |
| G6 | an absent music folder refuses | user | 1 |
| G7 | the current configuration, not the frozen one | user | 0, then 1 (a2) |
| G8 | the library is asked only when a row is missing | maintainer | 1 |
| G9 | `missing` counts what is still missing | user | 3 |
| G10 | each since state counted under its own key | user | 6 |
| G11 | the since counts in the summary | user | 9 |
| G12 | the since check names the rows held since | user | 1 |
| G13 | the written line for a job whose rows were all gained | user | 0, then 1 (b2) |
| G14 | the refusal step saying how many rows were gained | user | 1 |
| G15 | the gained count reaches the writer | user | 1 |
| G16 | adjudication under the job's own verb | maintainer | 0 |
| G17 | `intake.missing` declares `library.mounted` to doctor | maintainer | 0 |
| E1 | existing: only missing reports are listed | user | 3 |
| E2 | existing: missing tracks none of which was written refuse | user | 1 |

**G7, zero then killed.** The test moved the library root through the
`CRATEKIT_LIBRARY_ROOT` override, which re-bases a job's frozen configuration
exactly as it re-bases the live one, so the frozen root and the current one
never differed. This is the trap filed at
`docs/solutions/workflow-issues/a-frozen-config-is-frozen-against-the-file-not-against-an-env-override.md`,
met again. The test now drops the override and saves the moved root in the
file. Rerun as `r502-a2`: one death.

**G13, zero then killed.** The all acquired test asserted only that no
download command was named, which the sentence for a job that never had a
missing track also satisfies. It now asserts the gained sentence. Rerun as
`r502-b2`: one death.

**G16, zero, maintainer facing.** The review item's identity does not carry the
handler key, so an answer is read back whichever key adjudicates; the key only
labels an item the recheck newly offers.

**G17, zero, maintainer facing.** `intake.playlist` declares `library.mounted`
under the same feature rows, so doctor already requires the check for any
profile holding this verb, and the declaration changes no report today.
