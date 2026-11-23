# U303: the table's two zero rows, driven by hand after a test was written

`docs/mutation/u303.md` measured 13 rows at `26d16517`: 11 killed, and two
zero on the full suite, both on the reports shell's module `__getattr__`,
which lets a test read each report engine as an attribute of
`cratekit.cli.reports` now that the shell imports none of them at load. Both
are maintainer facing: no verb reads those attributes, the handlers import
their engine inside the function.

- `R1_engine_name_wrong`, `"library_report": "library"` to `"aging"`.
- `R2_engine_attribute_silent`, the closing `raise AttributeError(...)` to
  `return None`.

`tests/test_cli_contract.py::test_the_reports_shell_reads_each_engine_from_its_own_module_on_first_use`
was written for them. Driven by hand on the tree after it, each mutation
applied alone with `sed`, the test run alone, and the file restored from a
copy:

| row | the test, unmutated | mutated |
|---|---|---|
| R1 | 1 passed | 1 failed |
| R2 | 1 passed | 1 failed |

Both rows are read as killed by hand, not by the driver; the table's one
pass for this unit is spent.
