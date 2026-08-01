"""Marks ``tests`` as a package so test modules can import shared helpers by
absolute path (``from tests.xml_fixtures import ...``).

Without this, pytest inserts each test directory onto ``sys.path`` and the
helpers would have to be imported by bare name, which reads as though they came
from the installed package. They did not, and the distinction matters: nothing in
here ships.
"""
