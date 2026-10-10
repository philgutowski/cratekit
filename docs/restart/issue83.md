**The session before, 2026-09-16, #83 on `relay/83`, unattended.** Not a unit. The four
small defects the first attended sitting found are fixed and closed in the
ledger. R-344: `preflight.same_identity` folds the case on both sides of both
identity compares, and setup still records the identity as given, because it is
also the `library_id` jobs and watermarks match exactly. R-346: the prompter
flushes, so setup from a real terminal no longer needs `PYTHONUNBUFFERED=1`.
R-347: an empty secret raises `prompt.NothingEntered` and the credential offer
records it as the INFO note a no gets. R-348: `adapter.raise_if_defect` makes an
`AttributeError`, `TypeError` or `NameError` under an offer or a fetch an
`AdapterBroken` with the adapter's new `report-defect` token, asked before the
vendored token heuristic. Review raised one plausible finding, filed as R-365;
the hunt one file over filed R-366. Mutation tables `docs/mutation/r83.md`, 17
rows, 14 killing, and `r83-round-2.md` after the fold tests moved off an all
digit identity that was its own uppercase, 3 of 3 killing. The two remaining
zeros are maintainer rows, the strip in `normalize_identity` and the sweep's None
guard, which is an equivalent mutation. **Both tables ran in a harness moved
background job.** Each driver call was started in the foreground, outlived the
600 second tool ceiling, and was moved to the background by the harness, and the
session then waited on the output file with nothing edited meanwhile. Every row
reports its restore verified against HEAD and the tree held only the driver's own
output afterwards, which is the same shape
`docs/solutions/workflow-issues/a-relay-task-finished-a-mutation-table-by-backgrounding-the-driver-the-rule-forbids.md`
says is not validated. Phillip may want the tables rerun attended. Main's highest residual was R-366 once
`relay/83` merged. Battery on the committed tree before the record: ruff clean,
`scan_repo.py` exit 0, pytest 7543 passed and 1 skipped in 393 seconds. Do not
take #29.
