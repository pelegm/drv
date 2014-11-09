"""
.. conftest.py

Local conftest.py plugins contain directory-specific hook implementations.
Session and test running activities will invoke all hooks defined in
conftest.py files closer to the root of the filesystem.
"""

## Test tools
import pytest


def pytest_addoption(parser):
    parser.addoption("--slow", action="store_true", help="run slow tests")



def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getoption("--slow"):
        pytest.skip("need --slow option to run")

