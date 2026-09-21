# R-598 mutation notes

Two tables, `r598-a` over the engine in `core/session.py` and `r598-b` over the
release verb and the doctor clause. Fourteen rows, under the 25 row light cap,
so nothing was dropped. The author ran both tables, and a zero means the author
could not kill it (METHOD, no independent verifier).

Thirteen rows killed. One zero:

- **B2_no_shown_list_passed, zero on the full suite (9,849 collected).** Mutating
  `only=` to `None` in `release_lock` changes nothing a test can reach. The
  question and the answer are separate invocations, and the answering invocation
  builds its own orphan list a few lines above the sweep. The two lists differ
  only if a record is orphaned inside that single invocation. The guard it
  shadows, row A7, kills at the engine. What would give B2 teeth is binding the
  answer to what the ASKING invocation showed, which needs a digest on the
  declared gate. That is R-648. User facing, and the composite is A7: the
  engine's narrowing is pinned, and the shell's list is only as good as the gate
  binding it, which the ledger now records.
