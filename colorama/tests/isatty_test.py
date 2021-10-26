# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import sys
from io import StringIO
from unittest import TestCase, main, skipUnless

from mock import patch, PropertyMock

from ..ansitowin32 import StreamWrapper, AnsiToWin32, is_msys_cygwin_tty, FileNameInfo
from .utils import pycharm, replace_by, replace_original_by, StreamTTY, StreamNonTTY, StreamNonTTYWithFileNo


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
    def test_falseNotOnWindows(self):
        self.assertFalse(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

    def test_falseForIoString(self):
        self.assertFalse(is_msys_cygwin_tty(StringIO()))

    @skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch("ctypes.windll.kernel32", None)
    def test_falseIfKernelModuleUnavailable(self):
        self.assertFalse(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

    @skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch("ctypes.windll.kernel32.GetFileInformationByHandleEx", return_value=0)
    @patch("msvcrt.get_osfhandle", return_value=10)
    def test_falseIfWin32CallFails(self, mock_win32_call, mock_handle_call):
        self.assertFalse(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

    @skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch("ctypes.windll.kernel32.GetFileInformationByHandleEx", return_value=1)
    @patch("msvcrt.get_osfhandle", return_value=1000)
    def test_trueForMsys(self, mock_file_call, mock_handle_call):

        with patch.object(FileNameInfo, "FileName", new_callable=PropertyMock) as mock_filename_info:
            mock_filename_info.return_value = r"\msys-0000000000000000-pty3-to-master"
            self.assertTrue(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

    @skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch("ctypes.windll.kernel32.GetFileInformationByHandleEx", return_value=1)
    @patch("msvcrt.get_osfhandle", return_value=1000)
    def test_trueForCygwin(self, mock_file_call, mock_handle_call):

        with patch.object(FileNameInfo, "FileName", new_callable=PropertyMock) as mock_filename_info:
            mock_filename_info.return_value = r"\cygwin-0000000000000000-pty3-to-master"
            self.assertTrue(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

    @skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch("ctypes.windll.kernel32.GetFileInformationByHandleEx", return_value=1)
    @patch("msvcrt.get_osfhandle", return_value=1000)
    def test_falseForAnythingElse(self, mock_file_call, mock_handle_call):

        with patch.object(FileNameInfo, "FileName", new_callable=PropertyMock) as mock_filename_info:
            mock_filename_info.return_value = r"\random-0000000000000000-pty3-to-master"
            self.assertFalse(is_msys_cygwin_tty(StreamNonTTYWithFileNo()))

if __name__ == '__main__':
    main()
