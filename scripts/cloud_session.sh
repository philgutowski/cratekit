#!/bin/sh
# SessionStart hook for a Claude Code cloud session on this repository.
#
# A cloud container is a fresh clone with no venv, so the battery cannot run
# until one exists. This builds it, once, with the interpreter the project
# supports, and tells the session what it found. Locally it does nothing: a
# laptop has its venv already and CLAUDE_CODE_REMOTE is unset there.
#
# Stdout reaches the model as context. Facts only, briefly.
[ -n "$CLAUDE_CODE_REMOTE" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}" || exit 0

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
note "This is a cloud container: GitHub GraphQL is refused here, so gh issue, gh repo and gh project fail; gh api on repos/... REST paths works. scripts/board.py cloud is the queue. The Linux suite carries about 170 machine bound failures; scripts/cloud_battery.py tells yours from the machine's. The cloud-unit skill is the pipeline for a cloud session."
exit 0
