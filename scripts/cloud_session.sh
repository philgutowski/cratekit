#!/bin/sh
# SessionStart hook for a Claude Code cloud session on this repository.
#
# A cloud container is a fresh clone with no venv, so the battery cannot run
# until one exists. This builds it, once, with the interpreter the project
# supports, and tells the session what it found. Locally it does nothing: a
# laptop has its venv already and CLAUDE_CODE_REMOTE is unset there.
#
# Stdout reaches the model as context. Facts only, briefly.
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}" || exit 0

# On Phillip's Mac: show the attended cards, the work only that machine can
# do, so a local session opens on them. Never fails the session start.
if [ -z "$CLAUDE_CODE_REMOTE" ]; then
    if [ -x .venv/bin/python ]; then
        out=$(timeout 20 .venv/bin/python scripts/board.py local 2>/dev/null) && {
            printf '%s\n' "Cratekit local work, from the board's attended cards:"
            printf '%s\n' "$out"
            printf '%s\n' "Offer Phillip the first ready card; each card's body says what to run and when it is done, and METHOD's local attended work section says how to branch and commit it without colliding with the cloud."
        }
    fi
    exit 0
fi

note() { printf '%s\n' "$*"; }

if [ ! -x .venv/bin/python ]; then
    if command -v uv >/dev/null 2>&1; then
        uv venv --python 3.12 .venv >/dev/null 2>&1 \
            && uv pip install --python .venv/bin/python -e '.[dev]' >/dev/null 2>&1
    else
        python3.12 -m venv .venv >/dev/null 2>&1 \
            && .venv/bin/pip install -q -e '.[dev]' >/dev/null 2>&1
    fi
fi

if .venv/bin/python -c 'import cratekit, pytest, xdist' >/dev/null 2>&1; then
    note "Cratekit cloud session: .venv is built with the dev extras; run every tool through .venv/bin/."
else
    note "Cratekit cloud session: .venv could not be built by the session hook. Build it by hand: uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -e '.[dev]'."
fi
note "This is a cloud container, where Cratekit is built: the cloud-unit skill is the pipeline and scripts/board.py cloud the queue. GitHub GraphQL is refused here, so gh issue, gh repo and gh project fail; gh api on repos/... REST paths works. The Linux suite carries about 170 machine bound failures; scripts/cloud_battery.py tells yours from the machine's, and scripts/mutate.py --known-failures subtracts them."
exit 0
