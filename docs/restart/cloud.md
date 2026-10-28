**The cloud lane, set up 2026-10-27 in an attended cloud session, and made
the place Cratekit is built the same day, on Phillip's word that Relay and
the board lanes are abandoned and only cards that must be built locally
are.** A scheduled task on the cloud environment starts a fresh Opus 5.5
session every hour, and the `cloud-unit` skill runs METHOD's whole pipeline
on the card `board.py cloud` names: brainstorm if it is an idea, plan, build,
review with the `fable-reviewer` agent to the merge bar, the mutation table,
the record, the merge to `main` with the closing trailer, and `Landed` on the
card. A card that needs the machine is set aside with the local steps, and a
card labelled `attended` is never offered; #29 was given that label, which it
had lacked, since the queue offered it first by reach.

What carries it. `board.py cloud` reads every open unit and residual card's
comments over REST and states each by its session's last heading (`Started`,
`Resumed`, `Plan`, `Progress`, `Brainstorm`, `Question for Phillip`, `Needs
the machine`, `Withdrawn`, `Landed`), told from Phillip's by the harness
footer: one held card holds the lane, two holds name the earlier as the
keeper, a hold silent for eight hours is offered as `resume`, any session
comment refreshes it, and a landing note read by its first word is never
retaken. `board.py` falls back to REST a numbered page at a time when
GraphQL is refused, because the proxy refuses GraphQL and the numeric paths
in GitHub's `Link` header. `scripts/cloud_battery.py` measures the base's
failures on the container, 167 at `82bdfb3`, and reads a branch against
them; `scripts/mutate.py --known-failures` subtracts the same ids from every
mutation run. The repo scan reads a container's mounts as the harness's
under `CLAUDE_CODE_REMOTE`. The board workflow labels a card on open, edit
and label change. The project settings set the effort to high, the session
hook builds the venv, and `file-card` files a request in the brief form.

Verified here: the battery read against the base, 167 still failing, none
gone, and the one test newly failing at the first pass, a citation rule the
queue's label tripped, fixed. One test, an ext4 inode ordering assertion in
`tests/test_repair_rows.py`, failed once under the parallel run and passed
alone three times. Fable reviewed the cloud-first commits and found nothing
blocking and twelve residuals; one fix round took seven of them (tests for
the known set on the promoted run and the missing file, the indented
comment, a landing note by its first word, the hold posted before
classification with the earlier hold winning a race, the full battery after
a refused push, no hand edits to the baseline file, and this record), and
four are filed as residuals in `docs/residuals/`. The last, that a resumed
mutation batch reports the current known count over rows measured under an
older one, is recorded here and not filed, since no producer was named.

**The first hand fired run, 20:45 UTC, did nothing, and said why.** The
scheduled task was created through the session's own tool, which sets no
repository, so its session started with an empty home, no tool to attach
one, and GitHub refusing it as "access not enabled for this session". A
scheduled task's repositories are set only in its edit dialog at
claude.ai/code/routines, under Repositories, and each is cloned at the start
of every run; the prompt's attach fallback is gone and the task is paused
until the repository is selected there. **`BOARD_TOKEN` is in place**: the
Board workflow ran with it at 20:54 and moved #29 from Ready to Attended. A
classic token needs `repo`, `project`, `read:org` and `read:discussion`,
because `gh project item-edit` refuses without the last two, and the
workflow now sets pipefail, since the first run with the token hid that
refusal behind a green step.

**OWED.** The repository selected on the scheduled task, then a run fired by
hand and watched to its first `Started`. The macOS battery over everything
this lane lands, at Phillip's next local session. The merged `cloud/`
branches and this session's own are pruned locally, because the proxy
refuses a branch deletion.

**Three lanes and a dispatcher, 2026-10-28.** The scheduled task made from
the web dialog came out as a chat task with no repository twice, so a
dispatcher session was created with the repository attached
(`session_012kYvayWTP4cuGa2xftTJ6s`) and the hourly scheduled task "Cratekit
lane dispatch" wakes it; it follows the `cloud-dispatch` skill and starts one
fresh worker per free lane, each created with the repository. The first
worker built R-1031 from 22:06 to 23:45 UTC and landed it. With twenty one
cards ready, `board.py cloud` now runs `CLOUD_LANES` lanes, three, and a
worker sends the dispatcher `Dispatch` when it takes a card and when it frees
one, so no lane waits for the hour. The paused chat task "Cratekit Cloud
Lane" is Phillip's to delete.
