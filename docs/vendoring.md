# Vendoring policy

Cratekit ships one piece of code it did not write, inside its own source tree:
the acquisition downloader, under `src/cratekit/_vendor/`.

This document is the policy. The inventory, the patch list, and the replacement
procedure are in [`vendor/README.md`](../vendor/README.md).

## Why anything is vendored at all

The downloader's upstream was removed from GitHub and from PyPI in December 2025,
together with its author's account. Its documented install command fails. There
is no index left to resolve it from, and no fork on a public index is a drop-in
replacement.

So the choice was not "vendor or depend". It was "vendor or the product does not
install on anybody else's machine". R6 and R8 make that explicit: installation
must not depend on fetching anything that has been removed from public
distribution.

## Why a source tree, and not the alternatives (KTD4)

| Option | Why not |
|---|---|
| `file://` dependency reference | Not portable across installers, and it breaks under `uv`. It also encodes a path from the machine that wrote it, which R1 forbids outright. |
| Git submodule | Points at a repository that no longer exists. A submodule of a deleted remote is a clone that fails. |
| Committed wheel or sdist in the repository | An installer still has to be told to install it, which is a specifier by another name, and a binary blob in the tree is invisible to every text guard the repository runs. |
| **Committed source tree** | Survives `git clone`, editable installs, and Windows. It is plain text, so the portability and secret scans read it like anything else. |

Two rules follow from that decision and are asserted as tests:

1. **The vendored project is never named in a dependency specifier**, anywhere.
   The moment it is, an install asks an index for a package that index deleted,
   and a fresh clone stops working. `tests/test_vendor_import.py` checks every
   dependency group and also scans the repository for install commands naming it.
2. **Transitive dependencies that still exist stay ordinary dependencies.** They
   are declared normally in `pyproject.toml` — with the upper bounds their
   upstream declared, because vendoring moved responsibility for those bounds
   onto Cratekit. No resolver reads the vendored package's metadata any more.

## Licensing (KTD19)

Authored Cratekit code is MIT. Each vendored component keeps its own licence, and
its licence text ships alongside it. The downloader is AGPL-3.0-only, and its
text ships twice: inside the package as data, so it travels with the code it
covers, and at the repository root where a licence audit looks. A test asserts
the two copies are byte-identical, so the duplication cannot drift.

The vendored component's supported interpreter range is where Cratekit's own
`requires-python` comes from. That bound is closed at both ends deliberately:
without a ceiling a resolver installs on an interpreter the vendored tree has
never run on, and the failure surfaces as an unrelated dependency error.

## The scans still run over it. That is the point

`scripts/scan_repo.py` covers vendored trees deliberately, and it is the one
place in this repository where that scope is load-bearing rather than thorough.
Vendored code is code somebody else wrote, copied wholesale, and reviewed less
carefully than authored code, and the known-good copies of this particular
component sit on disk in the same directory as a live OAuth session cache. A scan
bounded to package source would not look at any of it.

The scan earned its keep here. It caught a commented-out plaintext credential
pair in the artifact before it was committed.

The one thing vendored code is exempt from is **style linting**. `ruff` skips
`src/cratekit/_vendor`, because restyling third-party code turns every lint rule
into another patch to re-apply on the next version bump, for no defect. What that
exclusion gives up — a syntax check over the tree — is replaced by a test that
byte compiles every vendored module, which is stronger for the question that
actually matters.

## Patching vendored code

Patching is allowed, and it is not free. Every patch has to be re-applied to
every future version, so each one needs a reason that outlives the person who
wrote it.

The rules:

* A patch is applied by `scripts/revendor_downloader.py`, never by hand. The
  procedure is executable so that it is repeatable.
* Every patch declares the exact text it expects to find, and the script
  **aborts** if that anchor is missing or ambiguous. A patch that silently
  becomes a no-op is worse than no patch, because the tests around it keep
  passing.
* Every patch records the failure it prevents, in `vendor/README.md` and in a
  comment at the site.
* Every patch has a test asserting the patched state, so re-vendoring without
  re-applying it goes red immediately.

Four categories have earned patches so far: removing credential material,
removing behaviour that violates a Cratekit invariant with no configuration flag
(R17, tempo tags), fixing hazards that vendoring itself introduced, such as code
that resolves paths relative to its own location and therefore reads the host
application's files once it has been moved, and **replacing an upstream choice
the provider has since broken, where upstream already ships the working
alternative.**

The fourth was added on 2026-09-01 by U47 and it is the narrowest of the four on
purpose. R-196 found that the provider gates lossless audio behind the PKCE
client and serves the device-linking client lossy, so upstream's login produced
silently degraded downloads. The patch flips which of two calls is live, because
upstream carried the PKCE call beside the one it used as a comment, and adds the
one field its token model drops. No login flow is written into the vendored tree
and no new capability is added; the provider's client library already ships the
handshake.

That boundary is what keeps this from becoming "patch in the features you want".
A patch in this category has to point at an upstream line that already exists and
already works. Anything that would have to be authored here belongs in the
adapter instead, which is the ordering the section below states.

## Replacement, not maintenance

The vendored downloader sits behind the adapter interface in `cratekit.acquire`
(U14) so that an alternative implementation can replace it through configuration
when a provider change breaks it (R9, KTD5).

That ordering is deliberate. When acquisition breaks, the first move is the
adapter, not the vendored source. Patching vendored code is a burden that
compounds at every version bump; swapping an adapter is a configuration key.
