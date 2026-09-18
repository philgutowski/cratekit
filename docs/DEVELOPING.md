# Developing Cratekit

Working on the product itself. If you only want to run Cratekit against a
library, this is the wrong file: the README installs it and
[`GUIDE.md`](GUIDE.md) runs it, and nothing here is needed for either.

Development and use are separate setups on purpose. A user installs a copy
through pipx that runs from its own environment. A developer works from an
editable install inside the checkout, so an edit takes effect without a
reinstall. Keeping them apart means the copy you run against a real library is
not the one you are halfway through changing.

## The environment

Development uses its own editable environment inside the checkout rather than
pipx. Set it up once, and activate it in each terminal window you work in:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Because it is editable, `crate doctor` treats the checkout as a developer
machine and checks that the commit hooks under Guards are installed. It fails
until they are, which is the intended behaviour here and the reason a user's
install is not editable.

Then:

```bash
ruff check src tests scripts
pytest -q
```

CI runs both on Python 3.12 and 3.13, plus a cold-install job that proves a
clean checkout installs and imports with nothing preinstalled.

## Guards

Set up the commit hooks once per clone. Both hook types matter. A bare
`pre-commit install` writes only the first, and the closing check on commit
messages then silently never runs.

```bash
pip install pre-commit && pre-commit install --hook-type pre-commit --hook-type commit-msg
cp .scan-identity.example .scan-identity
```

Then open `.scan-identity` and list your own drive and account names.
`scripts/scan_repo.py` runs on every commit and again in CI. It scans **every**
tracked path, vendored trees included, for two things: personal literals (a home
directory, a volume, an account, a machine name) and credential-shaped content
(OAuth tokens, API keys, private keys, and filenames that are credential stores
regardless of what is inside them). Nothing here should name a person or carry a
secret, and the hook is what stops one reaching the history, where removing it
becomes a rewrite everybody has to follow.

`.scan-identity` is gitignored and optional. It tells the scan which bare names
are yours, so "the X drive must be mounted" is caught even when X is not
currently plugged in. Path-shaped literals are caught without it.

## Deferred guards

A guard can be written before the module it governs. Such a guard keeps its full
assertion, is never stubbed, and is skipped with a reason naming the unit that
arms it. This prints every skip with the unit that unblocks it:

```bash
pytest -q -rs
```

`tests/_pending.py` is the register and `tests/test_pending_units.py` holds it
accountable: adding a skip without recording it fails the build, and so does
keeping one after its module lands. A skip is a countdown, not a hiding place.
The register is empty today, because every guard has been armed.

## How the work is picked and landed

The rules for a session are not in this file. `CLAUDE.md` at the repository root
is the session contract and names what to read next, `docs/METHOD.md` is the
pipeline and the merge bar, and `docs/BOARD.md` explains the queue that work is
taken from. `AGENTS.md` at the root routes an agent to the same place.
