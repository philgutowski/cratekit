---
title: "The provider serves lossy audio to the device-flow client, and neither the vendored tool nor the adapter can log in any other way"
date: 2026-08-28
category: integration-issues
module: src/cratekit/_vendor (config.py), src/cratekit/acquire/vendored.py, docs/residual-findings.md
problem_type: integration_issue
component: authentication
severity: critical
resolution_type: documentation_update
root_cause: wrong_api
framework_version: the provider's client library 0.8.11
symptoms:
  - "With `path_binary_ffmpeg` set and `quality_audio=LOSSLESS`, the landed track is 320k AAC, not FLAC"
  - "`playbackinfopostpaywall` returns `HIGH` for a PREMIUM account entitled to `HI_RES_LOSSLESS`, for both `LOSSLESS` and `HI_RES_LOSSLESS` session requests"
  - A PKCE login on the same account, same track, same minute is served genuine LOSSLESS FLAC over the same endpoint
  - "`crate doctor` and the full test battery are both green while the landed file's codec silently violates the requested quality policy"
  - The live DJ_tools pipeline's newest FLAC on disk is dated 2026-07-09, meaning it has likely been silently producing lossy output for weeks
applies_when:
  - "The provider source authenticates via device-flow OAuth (`login_oauth_simple`), which is both the vendored tool's and the client library 0.8.11's default and the only path the vendored `login()` in config.py actually calls (the PKCE call is present only as a comment beside it)"
  - "`quality_audio` is set to `LOSSLESS` or `HI_RES_LOSSLESS` and the account is entitled to it"
  - "`crate doctor` and the test battery are both green, which is not evidence of the landed file's actual codec since nothing checks it against the requested policy"
  - A PKCE-authenticated session is available to compare against, on the same account and track, to isolate the client as the variable
  - DJ_tools or another sibling project reuses this same vendored login path
related_components:
  - vendored_downloader
  - acquire_adapter
tags: [provider, oauth, pkce, device-flow, lossless, audio-quality, vendored-downloader, silent-failure]
---

# The provider serves lossy audio to the device-flow client, and neither the vendored tool nor the adapter can log in any other way

## Problem

A track downloaded through the vendored adapter (`src/cratekit/acquire/vendored.py`, wrapping the vendored downloader under `src/cratekit/_vendor/`) under an explicit `LOSSLESS` quality policy lands as lossy 320k AAC, with every layer that should have caught it (the requested quality setting, `crate doctor`, the green test battery) reporting clean.

## Symptoms

- A track requested at `quality_audio=LOSSLESS` lands as a `.m4a` (AAC, 320kbps) instead of FLAC, with no error, warning, or non-zero exit code anywhere in the pipeline.
- `crate doctor` reports `[ok] binary.ffmpeg: /opt/homebrew/bin/ffmpeg` while the run still degrades to lossy, because doctor checks whether ffmpeg exists on the machine, not whether the vendored tool was told its path.
- Directly probing the client library's `track.get_stream()` at every quality level (`LOW`, `HIGH`, `LOSSLESS`, `HI_RES_LOSSLESS`) returns `HIGH` (AAC) for all three lossless tiers, even though the account's own subscription endpoint (`users/<id>/subscription`) reports `PREMIUM` with `highestSoundQuality: HI_RES` and `premiumAccess: True`.
- The same degradation reproduces against a second, independent, already-persisted session (the live sibling DJ_tools project's provider token, issued 2026-08-01, same client library 0.8.11, same client id), ruling out anything specific to this vendored copy or this run.
- The live DJ_tools pipeline's newest FLAC on disk predates this investigation by about seven weeks (2026-07-09), meaning the same silent lossy degradation had already been happening in production before this session found it.

## What Didn't Work

The first hypothesis was a missing ffmpeg path. The vendored tool logged "FFmpeg path is not set... FLAC cannot be extracted," and `Download.__init__` does in fact gate `extract_flac` and `video_convert_mp4` off when its own `path_binary_ffmpeg` setting is empty (the vendored downloader's `download.py:162`, per `docs/residual-findings.md` R-195). `tool_settings()` in `src/cratekit/acquire/vendored.py:74` only pushes `quality_audio`, `download_base_path`, and `format_track`, never `path_binary_ffmpeg`, which is consistent with that theory and is a real, separate defect (recorded as R-195). Setting `path_binary_ffmpeg` by hand and re-downloading was the next step to test it.

That ruled out ffmpeg as the *cause*, but not the *symptom*: the track still landed as `.m4a`, still AAC, still lossy. Ffmpeg absence explains a lossless stream failing to *extract* to FLAC; it does not explain the stream itself coming back lossy. That distinction is what pointed the investigation away from extraction and toward the stream request itself.

The next false trail to rule out was entitlement. The account's own `users/<id>/subscription` response confirmed `PREMIUM`, `highestSoundQuality: HI_RES`, `premiumAccess: True` — so this was not a plan or account-tier restriction either.

## Solution

The working diagnostic, verified this session, is a PKCE login run against the same account, same track, same minute, in parallel with the device-flow (device-linking / "OAuth simple") login the vendored tool and the adapter actually use. The client library's `Session.pkce_login_url()` produced a URL, browser approval yielded a code, `pkce_get_auth_token()` exchanged it, and `process_auth_token(..., is_pkce_token=True)` completed the session. Under that PKCE session, `track.get_stream()` returned `LOSSLESS`, 16-bit/44.1kHz, over an `application/dash+xml` manifest, the device-flow session, by contrast, was served a BTS manifest and `HIGH` regardless of the requested quality. Driving the vendored `Download` class directly with that PKCE session landed a real FLAC, which confirmed the earlier tempo-tag patch holds on FLAC as well as MP4 (0 tempo tags of 18 total tags on the landed file), the original goal of attended item A1 (issue #49).

This is a diagnostic and workaround technique, not a shipped fix. Per this session's investigation, three things in the vendored config module currently make PKCE unreachable from the adapter's normal login path: the vendored `login()` calls `self.session.login_oauth_simple(fn_print)` with the PKCE call left as a comment (the vendored `config.py:255-257`); `token_persist()` writes exactly four keys, `token_type`, `access_token`, `refresh_token`, `expiry_time`, and does not persist `is_pkce` (the vendored `config.py:173-180`), so even a PKCE-obtained token would reload through `login_token(do_pkce=False)` on the next run and refresh against the wrong client; and the adapter's own reauthentication call, the session object's `login_token()` in `src/cratekit/acquire/vendored.py`, takes no `do_pkce` argument, so it always defaults to device-flow. Landing a real fix means teaching the adapter to authenticate via PKCE and to persist `is_pkce` end to end. That is still open, recorded as **R-196** in `docs/residual-findings.md` ("The provider serves lossy audio to the device-flow client, and neither the vendored tool nor the adapter can log in any other way"), found and recorded 2026-08-28 on `main` at commit `f1a4e5c`. Do not treat R-196 as closed by this session's work; the PKCE probe proved the workaround exists, it did not ship it.

Two related, narrower defects surfaced while driving the PKCE download directly and are tracked separately rather than folded in here: `Download.item()` requires `event_abort`/`event_run` `Event` objects and `progress`/`progress_overall` `rich.progress.Progress` objects that the adapter's `fetch()` does not currently pass, so `fetch()` as written either crashes on its first line or silently returns `(False, "")` (R-197). The ffmpeg-path gap described above under "What Didn't Work" is R-195. Both are cross-references to the same A1 session, not the subject of this doc.

## Why This Works

The root cause is which OAuth client authenticates the session, not the account, the requested quality setting, ffmpeg, or the vendored patches. Per this session's investigation, the provider has at some point after 2026-07-09 restricted lossless and hi-res delivery to sessions authenticated through the PKCE flow, while continuing to accept, and silently downgrade, the device-flow ("OAuth simple") client that the client library 0.8.11 uses by default, the client both the vendored tool and the sibling DJ_tools project log in with. The account's entitlement is real (`HI_RES`, `PREMIUM`), the request is well-formed (`config.quality` set correctly before every probe), and the extraction step works fine when it gets a lossless stream to work with (per R-195, once ffmpeg is configured). None of that matters, because the provider decides delivered quality by which client authenticated the session, and that decision happens upstream of every check this pipeline currently makes. `crate doctor`, the settings pushed by `tool_settings()`, and the offline test battery all validate inputs, is ffmpeg present, is the quality setting correctly threaded, does the code construct the right objects, and none of them inspect the artifact the third-party binary actually wrote to disk. The lossless policy is enforced only going in; nothing checks it against what comes out.

## Prevention

The concrete gap is a missing post-landing check: after `_VendoredSource.fetch()` (`src/cratekit/acquire/vendored.py:254`) returns a path, nothing reads the landed file's actual codec and compares it against the requested policy. That is the seam where the guard belongs — refuse or flag a file that landed lossy under a `LOSSLESS` policy, the same way the adapter already inspects the offer's advertised quality in `offer()`. `docs/residual-findings.md` R-196 names this as the cheap half of the fix that is worth doing even before the PKCE login work lands.

The general principle is worth carrying past this one provider: a green settings check, a green `doctor` check, and a green test battery together say nothing about what a third-party binary actually wrote to disk. Every one of those checks validates an input or a code path; only inspecting the artifact validates the output. Any integration that shells out to, or wraps, an external tool or provider whose behavior can change server-side (a codec, a format, a version, a rate limit) needs an assertion against the landed artifact, not just against the request that produced it. This is the same shape of gap R-197 exposed from a different angle in the same session: `fetch()` is the one method the offline suite structurally cannot exercise (`pragma: no cover`), so any defect that only shows up when a real file actually lands has no test surface today short of an attended run like A1.

Worth a caveat for the next reader of `docs/adapters.md`: that document states the lossless-marker invariant as a type-level guarantee ("An acquired lossy file always requires the marker... not validated away, it is unconstructable"). That guarantee governs whether a *classified* lossy result can go unmarked — it does not, and was never meant to, guard against a file being *misclassified* in the first place because nothing checked its actual codec. Read the two together rather than assuming `adapters.md` alone rules this class of failure out.

## Related Issues

- Issue #49 ("A1: Smoke-test the vendored downloader end to end") — the attended session that produced this finding, closed by commit `f1a4e5c` on `main`, 2026-08-28.
- `docs/residual-findings.md` R-196 (this finding), R-195 (adapter never pushes `path_binary_ffmpeg`), and R-197 (adapter's `fetch()` builds `Download` without the events/progress it requires).
- `docs/adapters.md` — the adapter contract this finding qualifies (see the caveat above).
- `docs/vendoring.md` and `vendor/README.md`, the vendoring policy and inventory for the vendored downloader under `src/cratekit/_vendor/`; `vendor/README.md` already cross-references R-195 through R-197 by number in its smoke-test log line.
