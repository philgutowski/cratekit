# U74 mutation notes

Two tables, `u74.md` and `u74-b.md`, one light pass split in two so each driver
run finished inside the tool's 600 second ceiling. 24 rows, all 24 killing,
null control 0 of 7896 in each, every restore verified against `HEAD`. This is
the author's table, not an independent one.

Rows cover every guard this unit added. In `sources.py`, the favourites spec's
`inbound_key`, both removed and pointed at the wrong intake key. In
`sync/cli.py`, each of the four halves of the open hearts job selection removed
alone (handler key, `source_id`, library, open state), the in flight guard, the
empty listing guard, the listing refusal recorded rather than raised, the
outbound export refusal caught in the planner rather than raised to `_plan`,
the queue callable bound, the shared run id and the `source_id` on the queued
job, the composer queueing the half, a queue time refusal recorded against its
half, `_filed` counting the half, the half's refusal in the refusal list, its
warning, its summary block, its check row, the check's listed or not wording,
its fail status, the gate screen's answer, and the `sync.next` step counting
the half's job.

Two tests were added BEFORE the table ran, not in answer to a zero, because no
existing test could fail on their guards: an open outbound favourites job,
which carries `source_id` favorites under its own key, does not hold the hearts
(`A3_handler_filter`), and a declined pass with labels off whose only refusal
is the hearts listing is that refusal rather than a no-op
(`B5_inbound_refusal_not_counted`).

`B3_queue_refusal_raised` mutates the one line both halves share in the
composer's queue loop, so its three kills are not the hearts half's alone.

Nothing was dropped for the cap.
