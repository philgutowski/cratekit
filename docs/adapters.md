# Acquisition adapters

Cratekit acquires music through an **adapter**: a small object that wraps one
downloading tool behind one declared contract. This document is the contract and
the procedure for adding or switching one.

The vendored downloader is at `src/cratekit/_vendor/`; why it is vendored at all
is [`vendoring.md`](vendoring.md). This document is about the boundary drawn
around it.

## Why the boundary exists

The vendored downloader's upstream no longer exists, so nothing can be installed
from an index to replace it. When a provider change breaks it, the only recovery
available is to point the product at a **different tool**, and that is only
possible if both tools are reachable through one interface.

R9 therefore requires at least one alternative proven against the interface
**before** launch. An interface with exactly one implementation is a description
of that implementation, and it looks identical to a real interface right up to
the moment it is needed.

## The contract

Two answers, at two scales. Both are types, not conventions.

**Per requested track**, exactly one of:

| Outcome | Means | The caller then |
|---|---|---|
| `acquired` | a file landed | tags, names, and files it |
| `unavailable-permanent` | the provider says it does not exist | quarantines it, never re-queues |
| `unavailable-transient` | it might work later | leaves it queued |
| `refused-by-policy` | it exists and Cratekit declined it | leaves it queued; a policy change alters the answer |

**Per invocation**, exactly one of:

| Outcome | Means |
|---|---|
| `ok` | the adapter ran |
| `auth-failed` | the provider rejected the session |
| `adapter-broken` | the adapter itself cannot run |

The distinction is the whole point. In the system Cratekit replaces, both call
sites raise on any non-zero exit and the tool exits zero when it silently skips a
track, so "nothing was new" and "your session is dead" arrive identically.

Three rules follow, and all three are enforced by the types rather than by
review:

1. **A failed invocation never advances a watermark and never quarantines a
   track.** An adapter that could not run learned nothing about the catalogue.
2. **A failed invocation still reports the full requested set**, so the queue is
   answerable from the result alone.
3. **An acquired lossy file always requires the marker.** There is no
   configuration in which a lossy file goes unmarked (R21), so the combination is
   not validated away, it is unconstructable.

   Read that precisely: the type forbids the combination it can SEE. It cannot
   see a file whose codec nobody read. Until U47 the losslessness on a result
   came from the provider's OFFER and nothing compared it to what actually
   landed, so the invariant governed a correctly classified result and never
   guarded against misclassification. Under strict policy the codec check in the
   vendored adapter now closes that gap at the file. Under
   `allow_lossy_marked` it does not, and R-211 records what is still open there.

## Settings live in the adapter

Quality, pacing, and the download destination are owned by the adapter for the
life of one invocation (KTD20). They are never written to a settings file shared
with another process.

The failure this removes was observed twice in the system Cratekit replaces: a
global settings file, mutated by subprocess calls before every run, reset to
factory defaults by a racing write and by a process kill landing mid-write.
Factory defaults were lossy audio into the tool's own download directory, so a
reset broke the lossless rule and the path convention at once, with no error
until the wrong files turned up or did not.

Where a wrapped tool does keep such a file, the adapter pushes this run's values
into its **in-memory** configuration and then reads them back. A tool that
coerces, ignores, or renames a setting is caught there. Nothing is saved.

## Pacing and concurrency

Acquisition runs through a bounded pool in `src/cratekit/acquire/download.py`.
It reads the cap and the nominal delay from the adapter's settings and declares
neither of its own, which is what keeps "the adapter owns pacing" true rather
than aspirational.

```toml
[acquisition]
concurrency = 1                # simultaneous acquisitions; default 1
pacing_delay_s = 6.0           # omit to take the adapter's own default
```

Omitting `pacing_delay_s` and setting it to `0.0` are **different answers**.
Omitted means the adapter decides, and its default is six seconds. Zero means
pacing is off and is honoured as written.

Each delay is jittered by half its nominal value, so six seconds lands anywhere
in three to nine. The width is not decoration. Two runs on fixed delays arrive
together, trip the provider's limiter together, and back off together, which is
a retry storm built out of politeness. Every run draws from its own generator so
neither has to know the other exists.

### A throttle and a ban are not the same event

This is the distinction the pool exists to draw, and getting it wrong is not a
failed run.

| The provider says | Cratekit | Because |
|---|---|---|
| rate limited (429) | honours the `Retry-After` hint, or backs off exponentially, and keeps trying | the request was legitimate, only the pace was not |
| forbidden (403), or a bot challenge | stops the whole run at once, makes no further request, and parks | retrying into a block is what turns it into a lockout |
| a retry hint longer than the run's ceiling | parks | sleeping on it is indistinguishable from a hung process, and truncating it is the early retry the hint existed to prevent |

Where the evidence is mixed, the blocked reading wins. A bot wall routinely
describes itself in the language of rate limiting, and a false stop costs a
re-run while a false retry can cost the account.

A parked run returns a structured cause with `retryable` set to false. That is
the field a job engine reads, deliberately rather than the exit code: the exit
code's class remedy for anything upstream is "retry later", and this is the one
member of that class where an automatic retry is the harm.

## Credentials

The OS keychain is the system of record. For the life of one invocation the
adapter materialises the stored session into a private file, hands the wrapped
tool that path, writes back whatever the tool refreshed, and erases the file.
Between invocations there is no provider token on disk.

Both the file and its directory are private. A `0600` file inside a
world-writable directory is not protected: any local account can unlink it and
put its own file in its place.

### Authorising the provider, and why it takes two commands

The vendored adapter accepts a PKCE session and refuses anything else. The
provider gates lossless audio behind the PKCE client and serves the
device-linking client lossy, so a device-flow session is not a lesser credential,
it is one that silently downgrades every download (R-196). Every session minted
before 2026-09-01 is a device-flow session, so this is the refusal an existing
installation meets first.

`crate login` does not perform an authorisation flow and is not going to. It
records a value in the keychain. Obtaining a session is an attended act at a
browser, exactly one verb in this product may read standard input, and the
vendored downloader already owns that conversation. So authorising is two
commands rather than one.

Step 1 mints a PKCE session. This opens a browser and writes the tool's own token
file, by default `~/.config/tidal-dl-ng/token.json`. It has to run with the Python
inside Cratekit's own environment, which pipx keeps out of sight, so the command
asks pipx where that is:

```bash
"$(pipx environment --value PIPX_LOCAL_VENVS)/cratekit/bin/python" -c "from cratekit._vendor.tidal_dl_ng.cli import app; app()" login
```

From a development checkout with `.venv` active, plain `python` in place of the
long path does the same job.

Step 2 moves it into the keychain, which is where the adapter reads it from:

```bash
crate login provider-session --from-file ~/.config/tidal-dl-ng/token.json
```

Step 3 erases the plaintext original. Step 2 copies it and does not consume it:

```bash
rm ~/.config/tidal-dl-ng/token.json
```

Step 3 is not tidying. R4's promise is that no provider token sits on disk
between invocations, and this hop is the one moment that is briefly false.
Nothing enforces the erase today; R-212 records that gap.

A device-flow token already sitting in that location does not block step 1. The
patched login reuses a stored session only when it is already PKCE, so the token
being replaced falls through to the mint rather than being reported as a
successful login. Without that, this procedure would be a loop on exactly the
machines that need it.

**What is verified about this procedure and what is not.** Every command above
was checked to exist and resolve: the vendored app exposes `login`, `crate login`
accepts `provider-session` with `--from-file`, and a token file's JSON text
survives the keychain round trip that the adapter reads it back through. The
interactive mint itself has not been run, because it needs real credentials, a
browser and the network. That is R-210, and until it is done this sequence is
correct by construction rather than by observation.

## Switching adapters

`acquisition.adapter` in the configuration file names the adapter, by its
registry key. Nothing else changes: the same requests go in and the same
contract-shaped report comes out.

```toml
[acquisition]
adapter = "tidal_dl_ng"        # the vendored downloader, the default
# adapter = "streamrip"        # the alternative
lossless_policy = "strict"     # or "allow_lossy_marked"
```

Pacing and concurrency travel with the adapter too, and are covered above.

An adapter whose third-party tool is not installed reports `adapter-broken` with
the remedy token `install-adapter` and names the distribution. It does **not**
name the install command: what a user types depends on their platform and package
manager, and only the command-line layer knows either.

## Adding an adapter

1. Subclass `BaseAdapter` in a new module under `src/cratekit/acquire/`. Set
   `name` to the key configuration will record.
2. Implement a source object with `authenticate`, `offer`, and `fetch`. Raise
   `AdapterAuthFailed` when the session is rejected and `AdapterBroken` when the
   tool cannot run. Any other exception from `offer` or `fetch` is a per-track
   failure and is classified for you.
3. Import the third-party tool **inside** a method, never at module scope. An
   adapter that can only be named by importing the tool it wraps cannot be
   offered as the replacement for the tool that just broke.
4. Add one line to `ADAPTERS` in `src/cratekit/acquire/__init__.py`.

Step 4 is the whole cost. The conformance suite derives its parameter set from
that mapping, so the new adapter is exercised against the full contract by being
registered rather than by somebody remembering to test it.

## Provider listings

Every listing the provider exposes is read through a wrapper in
`src/cratekit/acquire/listing.py`, one per listing shape. No other module calls a
listing method directly, and a test enforces that by reading the source.

The reason is specific. The provider's client returns one server page when asked
for a listing without pagination arguments, and it returns it without complaint,
so a truncated answer and a short answer are the same object. Three independently
written call sites in the previous system each had to rediscover this, and one of
them never did.
