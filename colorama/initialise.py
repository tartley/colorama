# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import atexit
import contextlib
import io
import logging
import platform
import sys

from .ansitowin32 import AnsiToWin32
from .win32 import GetConsoleCP, GetConsoleOutputCP, MICROSOFT_CODEPAGE_ENCODING


def _wipe_internal_state_for_tests():
    global orig_stdout, orig_stderr
    orig_stdout = None
    orig_stderr = None

    global wrapped_stdout, wrapped_stderr
    wrapped_stdout = None
    wrapped_stderr = None

    global atexit_done
    atexit_done = False

    global fixed_windows_console
    fixed_windows_console = False

    # no-op if it wasn't registered
    atexit.unregister(reset_all)


def reset_all():
    if AnsiToWin32 is not None:    # Issue #74: objects might become None at exit
        AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):

    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')

    global wrapped_stdout, wrapped_stderr
    global orig_stdout, orig_stderr

    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    if sys.stdout is None:
        wrapped_stdout = None
    else:
        sys.stdout = wrapped_stdout = \
            wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    if sys.stderr is None:
        wrapped_stderr = None
    else:
        sys.stderr = wrapped_stderr = \
            wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def deinit():
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr


def just_fix_windows_console():
    global fixed_windows_console

    if sys.platform != "win32":
        return

    # allow this fix to be run multiple times
    if not (platform.python_implementation() == 'CPython' and sys.version_info >= (3, 6)):
        # CPython is hard-coded to use UTF-16 for Windows Console IO:
        # https://github.com/python/cpython/blob/v3.13.2/Modules/_io/winconsoleio.c#L1092
        # But other implementations tend not to handle this at all:
        # https://github.com/pypy/pypy/issues/2999

        console_encoding_in = MICROSOFT_CODEPAGE_ENCODING[GetConsoleCP()]
        console_encoding_out = MICROSOFT_CODEPAGE_ENCODING[GetConsoleOutputCP()]

        if sys.stderr.isatty() and isinstance(sys.stderr.buffer.raw, io.FileIO):
            sys.stderr.reconfigure(encoding=console_encoding_out)

        if sys.stdout.isatty() and isinstance(sys.stdout.buffer.raw, io.FileIO):
            sys.stdout.reconfigure(encoding=console_encoding_out)

        if sys.stdin.isatty() and isinstance(sys.stdin.buffer.raw, io.FileIO):
            try:
                sys.stdin.reconfigure(encoding=console_encoding_in)
            except io.UnsupportedOperation as exc:
                if sys.stdin.encoding != console_encoding_in:
                    logging.warning(exc)

    if fixed_windows_console:
        return
    if wrapped_stdout is not None or wrapped_stderr is not None:
        # Someone already ran init() and it did stuff, so we won't second-guess them
        return

    # On newer versions of Windows, AnsiToWin32.__init__ will implicitly enable the
    # native ANSI support in the console as a side-effect. We only need to actually
    # replace sys.stdout/stderr if we're in the old-style conversion mode.
    new_stdout = AnsiToWin32(sys.stdout, convert=None, strip=None, autoreset=False)
    if new_stdout.convert:
        sys.stdout = new_stdout
    new_stderr = AnsiToWin32(sys.stderr, convert=None, strip=None, autoreset=False)
    if new_stderr.convert:
        sys.stderr = new_stderr

    fixed_windows_console = True

@contextlib.contextmanager
def colorama_text(*args, **kwargs):
    init(*args, **kwargs)
    try:
        yield
    finally:
        deinit()


def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream,
            convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream


# Use this for initial setup as well, to reduce code duplication
_wipe_internal_state_for_tests()
