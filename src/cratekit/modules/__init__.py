"""Feature modules: everything the Feature Inventory marks Module rather than Core.

Empty of imports for the same reason ``cratekit.core`` is. A package initializer
that re-exports its members turns importing one module into importing all of
them, and a feature module is precisely the thing that may need an extra a slim
install does not have (KTD7). The registry reaches modules by dotted path and
imports them lazily; nothing here should make that lazy import eager.
"""
