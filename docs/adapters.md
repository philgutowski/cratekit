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

## Credentials

The OS keychain is the system of record. For the life of one invocation the
adapter materialises the stored session into a private file, hands the wrapped
tool that path, writes back whatever the tool refreshed, and erases the file.
Between invocations there is no provider token on disk.

Both the file and its directory are private. A `0600` file inside a
world-writable directory is not protected: any local account can unlink it and
put its own file in its place.

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
