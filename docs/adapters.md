# Acquisition adapters

An adapter wraps one downloading tool behind the contract in
`src/cratekit/acquire/adapter.py`. The registry, `ADAPTERS` in
`src/cratekit/acquire/__init__.py`, holds two:

| Key | Tool |
|---|---|
| `vendored` | the vendored downloader (default; see [`vendoring.md`](vendoring.md)) |
| `streamrip` | the third-party `streamrip` package, if installed |

The vendored downloader's upstream no longer exists, so when a provider change
breaks it the recovery is switching to another adapter, not patching it.

## The contract

**Per requested track**, exactly one `TrackOutcome`:

| Outcome | Means | The caller |
|---|---|---|
| `acquired` | a file landed | tags, names and files it |
| `unavailable-permanent` | the provider explicitly said not found | quarantines it, never re-queues |
| `unavailable-transient` | anything else that failed; might work later | leaves it queued |
| `refused-by-policy` | it exists and the lossless policy declined it | leaves it queued |

**Per invocation**, exactly one `InvocationOutcome`: `ok`, `auth-failed` (the
provider rejected the session) or `adapter-broken` (the adapter cannot run).

The result types refuse to be built in an illegal shape:

- `acquired` must name its file and state whether it is lossless; a lossy one
  must require the lossy marker. No other outcome may carry a path.
- `refused-by-policy` and every failed invocation must carry a remedy token.
- A failed invocation cannot hold an `unavailable-permanent` result, never
  advances a watermark (`advances_watermark`), quarantines nothing
  (`quarantine_keys`), and re-queues every requested track that did not land,
  including tracks it never reached (`requeue_keys`).
- `auth-failed` must name the other registered adapters as alternatives.
- `dispatch` and `dispatch_invocation` refuse a handler map that misses an
  outcome.

Classification of a per-track failure:

- Permanent only on an explicit not-found: an exception class named
  `*NotFound`, a 404 status, or "404" or "not found" in the text. Server-error
  wording ("503", "service unavailable") is read first and stays transient.
- `AttributeError`, `TypeError` and `NameError` are code defects: the
  invocation becomes `adapter-broken` with the remedy `report-defect`.

Remedy tokens are in `Remedy`. Only the CLI turns a token into a command.

## Settings

Quality, lossless policy, pacing, concurrency and the download destination
live in `AdapterSettings`, frozen in memory for one invocation, and are never
written to a settings file another process shares. Where the wrapped tool has
its own settings, the adapter pushes this run's values into the tool's
in-memory configuration and reads every one back (`verify_applied`); a value
the tool did not take stops the run with `repair-adapter-settings`.

```toml
[acquisition]
adapter = "vendored"           # or "streamrip"
lossless_policy = "strict"     # or "allow_lossy_marked"
quality = "lossless"
concurrency = 1                # simultaneous acquisitions, at least 1
# pacing_delay_s = 6.0         # unset: the adapter's default, 6 s; 0.0: no pacing
```

- The retired key `tidal_dl_ng` still selects `vendored`.
- An unknown key is refused with `choose-known-adapter`, never replaced by the
  default.
- `allow_lossy_marked` keeps a lossy file and marks it; there is no setting
  for an unmarked lossy file.
- `streamrip` not installed: `adapter-broken` with `install-adapter`, naming
  the distribution.

Every landed file's codec is probed whichever adapter landed it: under
`strict` a lossy file is `refused-by-policy`, and under `allow_lossy_marked`
the marker is decided from the file, not the offer.

## Pacing

The bounded pool in `src/cratekit/acquire/download.py` reads its cap and delay
from `AdapterSettings` and declares neither itself. Each delay is jittered by
half its value (six seconds lands between three and nine), from a generator
per run.

| The provider answers | Cratekit |
|---|---|
| 429 rate limited | waits the `Retry-After` hint, jittered upward only, or backs off exponentially; five attempts per track |
| a retry hint longer than the run's ceiling | parks the run |
| 403 forbidden, or a bot challenge | stops the whole run at once and parks it |

An HTTP status decides; with no status, block wording beats rate-limit
wording. A parked run's cause has `retryable` false, which is what a job engine
reads instead of the exit code.

## Credentials

The OS keychain holds the provider session. For one invocation the adapter
writes it to a private file in a private directory, hands the tool that path,
writes back a refreshed session only if it parses as one and differs from the
session it read, and erases the file on every exit path. A download job's
invocation is one drive of the job: the vendored adapter writes the file and
logs in once for every track the drive acquires, never again after the
provider refuses the session, and writes back the session the tool holds when
the drive ends or fails, so a ten track job spends two login calls and four a
track rather than six a track. Each directory is named for its process, and
every new one first removes those a killed process left. The label catalogue
and the outbound account share one login per process. A catalogue open reuses
it only while the keychain still holds the session it was opened from; the
account keeps the adapter it opened until the provider refuses the session,
the session is no longer recorded, or a catalogue open finds it replaced.
A refreshed session the keychain or its index cannot take, or a token file
that cannot be written, never fails the run: the keychain keeps the session it
held, whose refresh token still logs in, and the run says so in a
`provider-session-not-stored` warning. A download says it when its drive
finishes; a verb that opened the catalogue or the account says it whatever its
answer, and keeps the logged in client for the rest of the process. A
rejected or expired session still fails as rejected.

### Signing in to the provider

The vendored adapter accepts only a PKCE session and refuses a device-flow one,
because the provider serves the device-linking client lossy audio. `crate
login` records a session but cannot mint one; the vendored downloader's own
login command does.

1. Mint a PKCE session. It opens a browser and writes
   `~/.config/cratekit-downloader/token.json` (under `$XDG_CONFIG_HOME` when
   set). Run it with the Python inside Cratekit's pipx environment, or plain
   `python` from an active development `.venv`:

   ```bash
   "$(pipx environment --value PIPX_LOCAL_VENVS)/cratekit/bin/python" -c "from cratekit._vendor.downloader.cli import app; app()" login
   ```

2. Record it in the keychain:

   ```bash
   crate login provider-session --from-file ~/.config/cratekit-downloader/token.json
   ```

3. Erase the plaintext file. `crate login` copies it and leaves it in place:

   ```bash
   rm ~/.config/cratekit-downloader/token.json
   ```

   Nothing enforces the erase, and a later download has been measured writing
   this file back (R-212). Check for it after a run.

The patched login reuses a stored token only when it is already PKCE, so a
device-flow token in that file does not stop step 1. A state directory left
under the upstream name, `tidal-dl-ng`, is moved into place the first time the
downloader runs; if both exist the new one wins.

## Adding an adapter

1. Subclass `BaseAdapter` in a new module under `src/cratekit/acquire/` and set
   `name` to its registry key.
2. Override `_source(scope)` to return a `TrackSource`: `authenticate()`,
   `offer(request)` returning an `Offer`, and `fetch(request, destination)`
   returning the landed path. Override `_session_scope()` if the tool needs the
   stored session as a file (`provider_session.materialised_session`).
3. Raise `AdapterAuthFailed` for a rejected session, `AdapterBroken` when the
   tool cannot run, and `LosslessRefused` from `fetch` for a landed file of the
   wrong codec. Any other exception from `offer` or `fetch` is classified per
   track for you.
4. Import the tool inside a method, never at module scope, so the adapter can be
   named while its tool is missing or broken.
5. Add one line to `ADAPTERS`. `tests/test_adapter_contract.py` parametrises
   over it, so registering runs the full conformance suite.

## Provider listings

Every provider listing is read through a wrapper in
`src/cratekit/acquire/listing.py`, one per listing shape; the provider returns
one page, silently, to a call without pagination. No other module calls a
listing method directly, and `tests/test_adapter_listing.py` enforces that from
the source.
