---
title: yt-dlp skips its audio postprocessor when the upload is already the target format
date: 2026-09-19
category: integration-issues
module: "src/cratekit/acquire/fallback.py"
problem_type: integration_issue
component: fallback_fetch
root_cause: wrong_api
resolution_type: code_fix
severity: high
symptoms:
  - "A fetched second source MP3 still carries the uploader's tags, a TBPM frame included, although the argv passes ExtractAudio:-map_metadata -1"
  - "Every test is green, because every test drives the fetcher through a fake runner"
applies_when:
  - "Any argument meant to act on a downloaded file is passed to yt-dlp through --postprocessor-args"
  - "A file this product did not tag is about to be tagged with core.tags.write_tags"
  - "Something has to be REMOVED from a file's tags that the core.tags FIELDS table does not name"
tags:
  - "yt-dlp"
  - "beat-grid"
  - "r17"
  - "tags"
  - "fallback"
---

## The trap

U81 passed `--postprocessor-args "ExtractAudio:-map_metadata -1"` so an
uploader's metadata, a tempo frame included, would never reach a landed file.
It does not apply to every download. yt-dlp's `FFmpegExtractAudioPP.run`, read
at 2026.6.9 `postprocessor/ffmpeg.py:510-514`, takes the copy branch when the
source codec already equals the target, finds the new path equal to the old
one, prints "Not converting audio ...; file is already in target format mp3"
and returns WITHOUT RUNNING FFMPEG. An upload served as MP3, which a
SoundCloud stream often is, keeps every tag it came with, and so does a
`--audio-format best` download in a common format. The built in `/code-review`
found it by reading the installed tool, and no test could have: the fetcher is
only ever driven through a fake runner.

The obvious repair does not exist either. `core.tags.clear_tags` removes only
the fields `FIELDS` names, and `FIELDS` has no tempo field ON PURPOSE (R17), so
the product's own deleter cannot reach the one frame that matters. And
`write_tags` only adds, so tagging the file from the row commits the upload's
TBPM underneath the row's artist and title.

## What to do instead

Treat any file the product did not write as untrusted and strip it whole
before tagging it: `core.tags.strip_tags(path)` removes the entire tag block
through the same `_open` container dispatch as every writer, so an ID3 chunk
inside WAV or AIFF is removed by the class that accounts for the chunk. The
fallback worker calls it before `write_tags`, and
`tests/test_acquire_fallback_fetch.py` drives it on a real MP3 carrying TBPM
and TXXX:BPM frames. Keep the postprocessor argument, it still helps when the
tool converts, but never cite it as the guard.

More generally, an argument routed to a yt-dlp postprocessor runs only when
that postprocessor decides to act. Read its `run` before relying on it.
