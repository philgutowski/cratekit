"""Guarded entry point, so ``python -m cratekit.cli`` and the console script agree.

The job engine re-invokes ``crate`` as a subprocess (KTD26), and the spawn
start method re-imports this module in the child, so the call sits behind the
name guard.
"""

from cratekit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
