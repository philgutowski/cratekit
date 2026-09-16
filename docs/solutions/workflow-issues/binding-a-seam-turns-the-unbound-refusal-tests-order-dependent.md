---
title: "Binding a seam turns the tests of its unbound refusal order dependent, because a from import ignores a blocked sys.modules entry"
date: 2026-09-16
category: workflow-issues
module: "src/cratekit/label/catalogue.py, src/cratekit/acquire/provider_session.py, tests/conftest.py"
problem_type: workflow_issue
component: seam_design
severity: medium
root_cause: import_semantics
applies_when:
  - "A seam that refused unconditionally gains an implementation, and the refusal must survive for a build where the implementation does not import"
  - "A test simulates the missing module with monkeypatch.setitem(sys.modules, name, None)"
  - "Recording a credential in the isolated keychain is enough for a shipped code path to build a live client"
symptoms:
  - "A refusal test passes alone and in its own file, and fails in the full suite with the bound answer instead"
  - "The failing tests are the ones that ran after any test that imported the implementation module"
related_components:
  - "label"
  - "acquire"
  - "test_harness"
tags:
  - "seam"
  - "import"
  - "test-order"
  - "live-provider-guard"
---
# Binding a seam turns the tests of its unbound refusal order dependent

## Context

U62 bound `label.catalogue.resolve` to `label.tidal_catalogue`. The refusal
`label-catalogue-unbound` had to survive for a build whose adapter does not
import, so the tests that pinned it were rewritten to block the module with
`monkeypatch.setitem(sys.modules, "cratekit.label.tidal_catalogue", None)`.

## The trap

`from cratekit.label import tidal_catalogue` does not consult `sys.modules` for
the submodule once it has been imported anywhere in the process. It finds the
attribute Python set on the `cratekit.label` package and returns it. The block
worked when the refusal tests ran first and silently did nothing after the
adapter's own suite had run, so the targeted runs were green and the full
battery failed two tests. `import cratekit.label.tidal_catalogue` and
`importlib.import_module(name)` both read `sys.modules` and raise on the `None`.

## What to do

Import an optional implementation by NAME, through `importlib.import_module`,
wherever the product asks whether it imports. `catalogue.ADAPTER_MODULE` is the
one spelling of the name.

## The second half, the one that costs money or an account

Binding the seam also removed a structural guarantee: before U62 no test could
reach the provider, because every path refused. After it, any test that records
a provider session and resolves the catalogue would log a real client in. The
guarantee was put back as an autouse fixture in `tests/conftest.py` that replaces
`provider_session.CLIENT_FACTORY` with one that fails the test, the same move
U57 made for the recognition transport. Every future seam that binds a live
client needs the same fixture in the same commit.
