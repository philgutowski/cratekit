**The cloud lane, set up 2026-10-27 in an attended cloud session, on
`claude/happy-rubin-chqmd5`.** A Claude Code cloud session can now take a
card labelled `cloud` on its own, from a scheduled task, and run METHOD's
pipeline to "Ready for the watcher": `board.py cloud` reads every open cloud
card's comments over REST and names the one to take by state (fresh, a
brainstorm Phillip answered, or a review the watcher posted), the
`cloud-unit` skill is the sequence, the `opus-builder` and `fable-reviewer`
agents fix the models (Opus 5.5 at high effort builds, Fable at high effort
reviews), the project settings fix the effort, and a session hook builds the
venv on a fresh container. `scripts/cloud_battery.py` measures the machine
bound failures of the Linux suite on the base and reads the branch against
them, 167 on this container at `82bdfb3` by its own measure, mostly
`tests/test_doctor.py` and the backup and restore suites, because root reads
every directory. The branch read against that baseline: 167 still failing,
none gone, one newly failing that passed alone three times,
`tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`,
which asserts a fresh file's inode is greater than an older file's: true on
APFS, and on ext4 under a parallel run an inode is reused, so it is the
container's and intermittent, and a cloud session that meets it reruns it
alone before calling it its own. The repo
scan no longer reads the container's mounts as a person's under
`CLAUDE_CODE_REMOTE`; one of them is named `skills`, which flagged nine test
files. `board.py` falls back to REST when GraphQL is refused and parses the
remote when `gh repo view` is, with `gh api --paginate` avoided because the
proxy rejects the numeric paths GitHub's Link header carries. The board
workflow now also runs on an issue opened, edited, labelled or unlabelled, so
a new card is labelled at once. The `file-card` skill files a request as a
unit issue in the brief form with the `cloud` label.

**OWED.** The scheduled task on the cloud environment is created disabled and
is enabled once this lands on `main`, because a fresh session clones `main`
and reads the skills from there. The first unattended run is the proof: one
card taken, one `Started`, one `Plan`, one `Ready for the watcher`, and the
watcher landing it. `BOARD_TOKEN` as a repository secret with the `project`
scope is what lets the board workflow move cards as well as labels; without
it the cards are added by the project's own auto-add workflow and the labels
are the queue. The macOS battery and the full suite were not run here, and
the mutation table for `board.py cloud` is owed to the watcher: the rows are
not written, since this is a chore and not a unit, and the fourteen tests in
`tests/test_board_cloud.py` are what hold it.

**The cloud became the build, 2026-10-27, the same session, on Phillip's
word that Relay and the board lanes are abandoned and only cards that must
be built locally are.** The lane no longer stops for a watcher: the
`cloud-unit` skill now runs the whole pipeline, measures the mutation table
and merges to `main` with the closing trailer. `scripts/mutate.py` takes
`--known-failures`, the base's failing ids from `cloud_battery.py baseline`,
and subtracts them from every run, so its baseline is green net of them and
its table names the file; `tests/test_mutation_driver.py` drives a batch
over a fixture red by one known id to a valid table with that id never
credited, and the same batch with an unrelated id still refused. `board.py
cloud` now reads every open unit and residual card rather than a label, one
held card holds the whole lane, a hold silent for eight hours is offered as
`resume` rather than reported, any session comment refreshes the hold, and a
card that landed while still open is reported. #29 was given the `attended`
label it had lacked, since the queue offered it first by reach. METHOD's Relay
section is a retirement note and its cloud lane section the rule; CLAUDE.md
names the cloud as where the project is built.

**OWED, superseding the paragraph above where they differ.** The first
scheduled run is the proof, fired by hand from this session and watched: the
scheduled task's configuration carries no repository source, so its prompt
tells a session with no checkout to attach and clone the repository itself,
and whether it needs to is measured on that run. `BOARD_TOKEN` is now the only
way the project's cards move, since nothing local runs `board.py sync`. The
merged `cloud/` branches, and this session's own, are pruned locally because
the proxy refuses a branch deletion.
