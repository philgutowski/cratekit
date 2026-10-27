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
