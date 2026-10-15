# r1016, the author's notes

**UNMEASURED.** Eleven rows against the listing change, written in
`r1016-rows.toml`, ten over the new guards and one sample of an existing
one. `scripts/mutate.py` refused the batch before any row ran: the full
baseline was red on one test, `tests/test_portability.py::
test_the_repository_itself_is_clean`, because an installer disk image was
mounted under the assistant app's product name, the word this repository's agent instructions and skills use for it, and the scan reads every mounted volume name as
a personal identifier (the residual this branch files,
`docs/residuals/r1016-a-mounted-installer-image-reddens-the-repository-scan.md`).
The driver scrubs `PYTEST_ADDOPTS` deliberately, so the environmental test
could not be deselected, and a hand rolled driver is forbidden. No row is
reported as a kill or a zero.

Rerun once the image is ejected, from the checkout holding the branch:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/mutate.py docs/mutation/r1016-rows.toml --out-dir docs/mutation

**What was measured instead, and what it is not.** The branch's
`tests/test_adapter_listing.py` was run against `main`'s source in a
detached worktree at `d747a19d`, the source put first on the path: 14 of
its tests failed there and pass on the branch, among them both cost
measurements, the account walk over a counting transport (no single
playlist fetch) and the 624 playlist listing through the real gate (14
requests). That is one composite, the whole change reverted, the shape of
row M1 and M3 together. It says nothing about the rows one guard at a time,
and in particular nothing about M4 (the `dateAdded` move), M6 (items null
read as empty) and M8 (the walk's name in the refusal), each of which a
single test is written to kill and none of which has been measured.

**The author's expectation, not a measurement.** M4 is killed only by
`test_a_listed_playlist_carries_the_fields_the_callers_read`, through
`user_date_added`; no caller reads that field, so a zero there would be a
maintainer facing zero. M10 is killed by the endpoint path the paired client
test pins, and by the counting transport refusing a path it does not serve.
