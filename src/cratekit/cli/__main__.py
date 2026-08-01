"""Guarded entry point, so ``python -m cratekit.cli`` and the console script agree.

KTD26 has the job engine re-invoke ``crate`` as a SUBPROCESS rather than
importing handlers in process, because in-process dispatch would make the engine
import every module and walk straight around the lazy-import stubs: help stays
clean while running a job crashes on a missing dependency. A subprocess needs a
real entry point, and the spawn start method re-imports the entry module in the
child, which is why the call sits behind the name guard rather than at module
level.
"""

from cratekit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
