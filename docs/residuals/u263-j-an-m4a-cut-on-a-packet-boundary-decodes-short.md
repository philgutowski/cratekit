---
title: An M4A with its index first, cut exactly on a packet boundary, decodes short through ffmpeg with nothing said
found: at the review of #692, U263, round two, 2026-11-12.
issue: no
---

**The mechanism.** A faststart or fragmented M4A carries its index before
its audio. Cut inside a packet, ffmpeg reports the short packet and the
decode fails; cut exactly on a packet boundary, the index's missing packets
are simply absent, ffmpeg exits 0 with nothing on stderr, and
`decode._ffmpeg_samples` returns the part before the cut. The head measures
key, tempo and energy from that part and the file is renamed.

**Measured cost.** Driven by the review on 450 hand damaged cases over 9
base files: 35 decoded short in silence, every one a cut on a packet
boundary of a faststart or fragmented file, yielding 25 to 99.9 percent of
the frames. A random cut lands on a boundary about once per packet length
in bytes. The vendored downloader tolerates a failed last segment
(`download.py` near line 294), which would cut on a fragment boundary; that
producer was not driven.

**Closes when:** the decoded length is checked against the length the
container declares, and a short decode is undecodable. Ledger only.
