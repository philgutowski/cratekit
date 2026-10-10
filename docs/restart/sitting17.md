**Sitting 17, attended, 2026-09-29, no code.** The session drives rekordbox
through desktop control, by the author's rule change in `CLAUDE.md`. **A8's
verdict is clean**: two rows inserted through the database were accepted by
rekordbox 7.2.19, analysed on request and stable over three launches, so
#224 is buildable. #223 was refused at its gate on a timing test under load
and landed by hand after two green batteries, 10,621 passed and 1 skipped.
Filed **R-757**, **R-758** and **R-759**, on the board bar, and **R-760**,
not on it. **Main's highest residual number is R-760.**

**Last built: R-745, issue #223, `relay/223`, 2026-09-29, landed by hand, see
sitting 17.** `crate export collection FILE` writes a
collection export from a disposable copy of the configured database, with
rekordbox closed, so the verbs that take `--export` no longer wait on
rekordbox's menu. It never replaces a file and never opens the live
database. **The export carries no tempo data**: every row has the gridless
constant and no child element. It carries no cue points and no smart
playlists, and it is not a backup. The file names who wrote it in a comment
ahead of the document element, and claims nothing about which application
last wrote the database, since the database holds no application version.
Every verb that takes `--export` is driven against a file this verb wrote,
nine of them, and the cutover precheck holds for it with no new rule. The
built in review raised ten findings: eight fixed with a test each, one was
the record, one measured and left. **The numbers:** 10,622 collected, 10,621
passed and 1 skipped, ruff clean, `scan_repo.py` exit 0. **The mutation
tables are the author's**, `docs/mutation/r745-a.md` to `r745-c.md`: 25
distinct mutations, 22 killed on the first pass, and each of the 3 zeros
bought a test and was measured again as a kill. Filed **R-751** to
**R-756**. **R-755 meets the board bar and its issue is owed**, since an
issue is created after the merge that carries the entry and this session
does not merge. **Owed at the next attended sitting:** write an export,
take one from rekordbox the same minute, compare track count, playlist
paths and each playlist's membership, and import an intake file spliced
from the written one, which is R-753. **Main's highest residual number is
R-756 once this merges.**
