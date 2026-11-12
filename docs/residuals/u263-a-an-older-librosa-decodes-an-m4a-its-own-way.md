---
title: On an older librosa an M4A is still decoded by its own fallback, so an M4A's samples depend on the librosa installed
found: at the plan of #692, U263, 2026-11-12.
issue: no
---

**The mechanism.** `analysis/decode.py` calls `librosa.load` first and goes
to ffmpeg only when that raises and libsndfile cannot open the file. librosa
1.0 raises on an M4A, so the M4A is decoded through ffmpeg; 0.10.2 to 0.11
read it through audioread (CoreAudio on macOS, ffmpeg as 16 bit integers on
Linux) and return those samples. The card asked for the same samples
whichever supported librosa is installed; the orchestrator's merge bar asked
that nothing analysed today change. The second won, as the conservative call,
and the question is on the card for Phillip.

**Measured cost.** On this container an AAC M4A decodes to 176,640 samples
at 22,050 Hz through audioread and through ffmpeg alike; their values were
not compared, since AAC is lossy and the fallback quantises to 16 bits. An
ALAC M4A gives the same key and tempo either way. Which librosa the Mac's
installed copy runs is owed to the attended check this unit files.

**Closes when:** Phillip answers the question on #692, or the installed copy
is on librosa 1.0, where only ffmpeg reads an M4A. Ledger only.
