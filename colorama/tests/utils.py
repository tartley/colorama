# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from contextlib import contextmanager
from io import StringIO
import sys
import os

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

class StreamTTY(StringIO):
    def isatty(self):
        return True

class StreamNonTTY(StringIO):
    def isatty(self):
        return False

@contextmanager
def osname(name):
    orig = os.name
    os.name = name
    try:
        yield
    finally:
        os.name = orig

@contextmanager
def redirected_output():
    orig = sys.stdout
    sys.stdout = Mock()
    sys.stdout.isatty = lambda: False
    try:
        yield
    finally:
        sys.stdout = orig

@contextmanager
def replace_by(stream):
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

@contextmanager
def replace_original_by(stream):
    orig_stdout = sys.__stdout__
    orig_stderr = sys.__stderr__
    sys.__stdout__ = stream
    sys.__stderr__ = stream
    try:
        yield
    finally:
        sys.__stdout__ = orig_stdout
        sys.__stderr__ = orig_stderr

@contextmanager
def pycharm():
    os.environ["PYCHARM_HOSTED"] = "1"
    non_tty = StreamNonTTY()
    try:
        with replace_by(non_tty), replace_original_by(non_tty):
            yield
    finally:
        del os.environ["PYCHARM_HOSTED"]

