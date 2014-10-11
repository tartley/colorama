# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from contextlib import contextmanager
import sys
import os

from mock import Mock

@contextmanager
def osname(name):
    orig = os.name
    os.name = name
    yield
    os.name = orig

@contextmanager
def redirected_output():
    orig = sys.stdout
    sys.stdout = Mock()
    sys.stdout.isatty = lambda: False
    yield
    sys.stdout = orig

@contextmanager
def replace_by_none():
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = None
    sys.stderr = None
    yield
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
