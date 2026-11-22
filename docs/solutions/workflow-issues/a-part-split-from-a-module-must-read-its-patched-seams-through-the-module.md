---
title: A part split from a module must read the module's patched seams through the module, or a test's patch silently stops biting
date: 2026-11-22
category: workflow-issues
module: "src/cratekit/core/rb_writer.py, src/cratekit/core/rb_probes.py, src/cratekit/core/session.py, src/cratekit/core/restore.py, src/cratekit/core/restore_perform.py"
problem_type: workflow_issue
component: development_workflow
root_cause: incorrect_assumption
resolution_type: code_fix
severity: medium
tags: [refactor, split, monkeypatch, seams, rb-writer, session, restore]
applies_when:
  - "Moving functions out of a module that tests patch with monkeypatch.setattr(module, name, ...)"
  - "Splitting rb_writer, session, restore or any module the suite reaches through its name"
  - "A re-export keeps every name importable and the suite still goes red, or worse, stays green"
---

## The trap

A re-export keeps `rb_writer.rekordbox_running` importable after the function
moves to a part, so every import still works. But `monkeypatch.setattr(W,
"rekordbox_running", fake)` replaces the attribute on `rb_writer` only. Code
that moved to the part and calls `rekordbox_running()` looks the name up in
the part's own globals, finds the real function, and the patch does nothing.

U300 met three shapes of it on one split:

- `rekordbox_processes_running` resolved its probes with `globals()[name]`,
  which after the move meant the part's globals: two guard tests went red.
- `W._REGISTERED.clear()` and `W._PROCESS_PROBES` read private names the
  narrowed re-export had left out: an `AttributeError`, loud.
- A capacity test patches `restore.os` and `restore.shutil` with a sampler to
  measure the disk's peak during a restore. Moved file operations call their
  own `os` and `shutil`, the sampler sees nothing, the measured peak drops,
  and "the estimate is above the measured peak" passes more easily. Green,
  and weaker. Nothing would have failed.

## What to do

- Before moving anything, list every name patched on the module across the
  suite (`setattr(module, "name"`, `patch.object(module, ...)` and string
  targets `"cratekit.core.module.name"`), and every attribute read off it
  under any alias.
- In the part, read every such name, every name the module still defines and
  every name another part defines through the module at call time: a three
  line `_writer()` that imports the module inside the function, and
  `_writer().name` at each use. Import the part's leaf data directly.
- Read module objects a test patches (`os`, `shutil`, `tempfile`) through the
  module as well, and keep them imported on it.
- After the split, check every attribute anything reads off the module still
  exists, and run a mutation row per lookup that reverts it to the part's own
  name: U300's table is the template (`docs/mutation/u300-rows.toml`).
