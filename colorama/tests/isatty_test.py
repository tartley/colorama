# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import sys
from io import StringIO
from unittest import TestCase, main

from mock import patch

from ..ansitowin32 import StreamWrapper, AnsiToWin32, is_msys_cygwin_tty
from .utils import pycharm, replace_by, replace_original_by, StreamTTY, StreamNonTTY


def is_a_tty(stream):
    return StreamWrapper(stream, None).isatty()

class IsattyTest(TestCase):

    def test_TTY(self):
        tty = StreamTTY()
        self.assertTrue(is_a_tty(tty))
        with pycharm():
            self.assertTrue(is_a_tty(tty))

    def test_nonTTY(self):
        non_tty = StreamNonTTY()
        self.assertFalse(is_a_tty(non_tty))
        with pycharm():
            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharm(self):
        with pycharm():
            self.assertTrue(is_a_tty(sys.stderr))
            self.assertTrue(is_a_tty(sys.stdout))

    def test_withPycharmTTYOverride(self):
        tty = StreamTTY()
        with pycharm(), replace_by(tty):
            self.assertTrue(is_a_tty(tty))

    def test_withPycharmNonTTYOverride(self):
        non_tty = StreamNonTTY()
        with pycharm(), replace_by(non_tty):
            self.assertFalse(is_a_tty(non_tty))

    def test_withPycharmNoneOverride(self):
        with pycharm():
            with replace_by(None), replace_original_by(None):
                self.assertFalse(is_a_tty(None))
                self.assertFalse(is_a_tty(StreamNonTTY()))
                self.assertTrue(is_a_tty(StreamTTY()))

    def test_withPycharmStreamWrapped(self):
        with pycharm():
            self.assertTrue(AnsiToWin32(StreamTTY()).stream.isatty())
            self.assertFalse(AnsiToWin32(StreamNonTTY()).stream.isatty())
            self.assertTrue(AnsiToWin32(sys.stdout).stream.isatty())
            self.assertTrue(AnsiToWin32(sys.stderr).stream.isatty())

    @patch("colorama.ansitowin32.is_msys_cygwin_tty", return_value=False)
    def test_isattyCorrectForMintty(self, mock_fn):
        self.assertFalse(is_a_tty(StreamTTY()))
        self.assertFalse(is_a_tty(StreamNonTTY()))
        mock_fn.assert_called_once()

    @patch("colorama.ansitowin32.is_msys_cygwin_tty", return_value=True)
    def test_isattyCorrectForMintty(self, mock_fn):
        self.assertTrue(is_a_tty(StreamNonTTY()))
        self.assertTrue(is_a_tty(StreamTTY()))
        mock_fn.assert_called()

class MinttyTest(TestCase):
    """Tests for the detection of mintty / msys/ cygwin

    They're arguably a little brittle to the exact detection implementation, so can be refactored
    if the implementation changes.
    """

    @patch("colorama.ansitowin32.msvcrt", None)
    @patch("io.StringIO")
    def test_falseNotOnWindows(self, mock_stream):
        mock_stream.fileno.return_value = 10
        self.assertFalse(is_msys_cygwin_tty(mock_stream))

    def test_falseForIoString(self):
        self.assertFalse(is_msys_cygwin_tty(StringIO))

    @patch("colorama.ansitowin32.ctypes.windll.kernel32", None)
    @patch("io.StringIO")
    def test_falseForIoString(self, mock_stream):
        self.assertFalse(is_msys_cygwin_tty(StreamTTY()))

    @patch("colorama.ansitowin32.ctypes.windll.kernel32.GetFileInformationByHandleEx",
           return_value=0)
    @patch("io.StringIO")
    def test_falseForIoString(self, mock_win32_call, mock_stream):
        mock_stream.fileno.return_value = 10
        self.assertFalse(is_msys_cygwin_tty(StreamTTY()))

    @patch("ctypes.windll.kernel32.GetFileInformationByHandleEx",
           return_value=1)
    @patch("io.StringIO")
    def test_falseForIoString(self, mock_file_name, mock_stream):
        mock_stream.fileno.return_value = 10

        with patch("colorama.ansitowin32.FileNameInfo.FileName") as mock_filename_info:
            mock_filename_info.return_value = r"\\msys-0000000000000000-pty3-to-master"
        self.assertTrue(is_msys_cygwin_tty(mock_stream()))

if __name__ == '__main__':
    main()
