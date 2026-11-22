"""Core: the foundation, domain, and infrastructure layers of Cratekit.

Deliberately empty of imports: a re-exporting initializer would import every
module under here, optional extras included, and break even the help screen
on a slim install (KTD7). Layers are decided by ``tests/test_layering.py``;
imports point downward only (KTD23).
"""
