# U176 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` with `--known-failures .cloud-battery/baseline.txt` on the
cloud container, so each is a Linux measure of a macOS suite, green net of the
167 failures bound to this machine.

**`u176.md`**, 25 rows over `acquire/bandcamp.py` (12) and
`acquire/bandcamp_cli.py` (13) at `d247586`, null control 0 of 14399, every
restore verified against `git show HEAD`. 24 killed on their subsets.

**`u176-c5.md`**, the one zero measured again at `627b1ce`, after the test it
bought. Killed, 1.

## The one zero

- **C5, an empty page ends the listing.** Zero on the full suite at `d247586`,
  because every empty page in the suite's fake account also said
  `more_available: false`, and that guard ended the listing on its own. The
  brief's first scenario is a listing that ends on an empty page, so rather
  than a composite the zero bought a test,
  `test_an_empty_page_ends_the_listing_even_when_it_says_more_is_available`,
  and `u176-c5` measures the same mutation at 1 kill.

## Ranked below the cap

Seven guards were considered and dropped, each covered by a named test and
ranked below the rows above because its failure is a park or a refusal the
envelope still reports, rather than a file staged, lost or fetched twice:

- the three parks in the worker, `_links_for`, `_library_for` and the session
  read, each driven by a resume test in `tests/test_bandcamp_cli.py`;
- the park `_item_failure` makes of a refused session;
- `HELD` in `TO_FETCH`, driven by the compilation scenario;
- the compilation's `Artist - Title` split in `track_wanted`;
- the refused copy's `output-exists` raise, driven by the collision tests.

The review drove its own in memory tables in both rounds, 34 rows then 19,
summarized in the Progress comments on #357 rather than here; the three guards that still
killed nothing there are a residual filed by this unit.
