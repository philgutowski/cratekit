---
title: A model wrapper the suite never builds can be the wrong one, and a column read by number passes every fake
date: 2026-09-17
category: integration-issues
module: "src/cratekit/analysis/vocal.py, src/cratekit/analysis/vocals.py, src/cratekit/vocals/cli.py"
problem_type: integration_issue
component: vocal_scoring
root_cause: untested_real_dependency
resolution_type: code_fix
severity: high
symptoms:
  - "Every real track reports vocal-model-unavailable with a hint to install an extra that is installed"
  - "stderr shows wget: command not found during a vocal run"
  - "Scores on a real model bear no relation to what the source system stamped, with male calls on instrumentals"
  - "The queue check for a vocal job fails as internal-error the moment the extra is installed"
applies_when:
  - "A loader constructs a third party model wrapper and no test ever constructs the real one"
  - "A scorer reads output columns by a literal index and every fixture fills exactly those columns"
  - "A third party package does work at import time, such as fetching a file, and a check imports it to see whether it is installed"
tags:
  - "vocals"
  - "panns"
  - "fake-only-proof"
  - "label-table"
  - "r370"
  - "r371"
  - "attended-sitting"
---

# A model wrapper the suite never builds can be the wrong one, and a column read by number passes every fake

## Context

U25 and U58 landed the vocal pass against fakes. `_FakeModel.inference`
returned a `(1, frames, 527)` array with the signal's level in column 0 and
two fractions of it in columns 1 and 2, and `infer_frames` read columns
`(0, 1, 2)` by default. `default_loader` built `panns_inference.AudioTagging`
and no test called it, because the extra is heavy and the tests bind a fake
the way the workers do. Every test was green. The first attended run on the
live library, 2026-09-17, could not score a single track.

Three separate things were wrong, and each one alone would have stopped the
workflow:

1. `AudioTagging` is the clip level wrapper. Its `inference` returns a
   `(clipwise, embedding)` pair and the underlying `Cnn14` has no frame
   output at all. The frame level wrapper is `SoundEventDetection` over
   `Cnn14_DecisionLevelMax`, which is what the source system used and what
   the checkpoint in `~/panns_data` is for.
2. The wrapper's answer to a missing checkpoint is `os.system("wget ...")`.
   This machine has no wget, so the loader raised `FileNotFoundError` after
   the shell printed its complaint, and `vocals._load` reported the model
   unavailable with a hint to install the extra.
3. Columns 0, 1 and 2 of the AudioSet label table are Speech, Male speech
   and Female speech. Singing, Male singing and Female singing are columns
   27, 32 and 33. On a real model the speech read scored four known tracks
   0, 0, 2 and 7 with male calls; the singing read scored 13, 11, 0 and 1
   and matched every gender call the source system had made.

Under those, a fourth: importing `panns_inference` executes its `config`
module, which shells out for the label table when HOME has none and then
raises opening the file it did not fetch. The queue's availability check
imported the package to answer installed or not, so once the extra was in
the venv, every test's redirected HOME turned that check into an internal
error.

## Guidance

- **A loader that builds a third party object needs one test that builds
  it against a fake of the third party module**, asserting the class and
  the arguments, not just that "a loader raised" degrades gracefully. The
  graceful degradation test was green throughout and was the thing hiding
  the defect.
- **Never read a model's output columns by literal index when the model
  carries a label table.** Resolve by name from `model.labels` and pin the
  names. Keep the numeric read only for a fixture with no table, and say so
  in the constant's name, which is what `FIXTURE_CLASS_IDX` is for.
- **Check for the files a wrapper will fetch before asking the wrapper for
  them**, because its fetch is a shell out you do not control. `LABELS` and
  `CHECKPOINT` are checked in `default_loader` for that reason.
- **Answer "is the extra installed" with `importlib.util.find_spec`**, never
  with an import, when the package does work at import time.
- **Redirect the wrapper's stdout** during construction. It prints its
  checkpoint path and device, and stdout is where the JSON envelope goes.
- **Chunked inference has a floor.** A convolutional model that pools its
  time axis cannot take a piece shorter than its pooling depth allows. Fold
  a short tail into the previous piece rather than sending it alone (R-371).

## Why This Matters

The fake driven suite proved the reduction, the chunking, the resume and
the degrade paths, and all of it was correct. What it could not prove was
the one line where the product touches the real dependency, and that line
was wrong three ways. The cost was the whole workflow: a full library
restamp on the shipped code would have written nothing and told the person
to install what was installed. The fix was small. Finding it needed the
extra installed and one real file, which is what an attended sitting is for.

## When to Apply

- Before landing any loader for a heavy optional dependency, torch, a
  model checkpoint, a vendored client.
- When a scorer or parser indexes into a third party output by number.
- When a green suite is the only evidence that a real dependency works.

## Related

- `docs/residual-findings.md`, R-370 and R-371: the findings, with the
  driven numbers.
- `docs/residual-findings.md`, R-133: the attended run this was found in.
- `docs/solutions/workflow-issues/keeping-a-fixture-green-under-a-new-guard-is-not-evidence-the-guard-is-tested.md`:
  the neighbouring lesson about fakes.
- `DJ_tools/src/dj_tools/DJ_analysis/vocal_detect.py`: the source system's
  wrapper and label names, which are the parity target.
