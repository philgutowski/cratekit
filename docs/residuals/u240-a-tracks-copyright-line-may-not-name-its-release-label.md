---
title: Tag folder reads a track's copyright line, while the label sweep confirmed the release's, so a track credited to its artist is left to the blocked catalogues
found: at the review of #648, U240, 2026-11-11.
issue: no
---

**The mechanism.** The vendored downloader writes `track.copyright` onto each file (`src/cratekit/_vendor/downloader/download.py`), and `tag folder` names a file's label from that line. The label sweep (`label/tidal_catalogue.py`) confirmed the release on the release's own credit. Where a track's line names its artist or a distributor rather than the label, the file's line names no registered label and the file is asked of the catalogues, which on 2026-11-10 refused everything.

**Measured cost.** Driven by the round one review on a tail step: a staging folder of a file reading `℗ 2023 Rawax` and one reading `℗ 2023 Some Artist`, every catalogue blocked. The first is tagged by its label; the second fails its item and the label go stops at the tag step. How often a real download's track line differs from its release's credit is unmeasured: no live download was read.

**Closes when:** the label go stages each file with the label it was confirmed for (its label tag, as the Bandcamp fetch does), or the rate of differing lines is measured live and found negligible. Ledger only until a live pass shows it.
