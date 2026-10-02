# R-834 mutation table, read

One table, the author's and not independent, measured by `scripts/mutate.py`
on `relay/242` at 530e158, after the review's fix round, in the foreground
with nothing else touching the tree.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r834.md`, the private step and the unretried create | 6 | 5 | 1 |

Six rows, under the cap of 25, because the unit's new guards are three: the
call itself, its one retry, and the refusal passed over rather than raised.
M5 samples the existing guard that a create is never retried. M6 points the
private call at an object the create did not return.

**M4 killed nothing, and the guard it reverted is gone.** It removed the
check that the created object offers `set_playlist_private` at all. With the
check gone, the missing call raises inside the retried call, is translated
like any refusal, and is passed over by the same `except`, so the outcome
was identical. Commit 3f1cf97 removed the check as dead code. The guard
that catches an upstream rename of the call is
`test_the_client_library_still_offers_the_private_call_a_create_relies_on`,
which pins it on the client library and is not a mutation row. M6's text
names the line that commit replaced, so the table is the record of 530e158
and was not run again: the remaining five rows name text that is unchanged
apart from M6, whose replacement routes through the same object.
