# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from colorama import initialise
from colorama.ansi import Style


class ResetTest(TestCase):
    def test_reset_with_stdout_redirected(self):
        stdout, stderr = StringIO(), StringIO()
        stdout.isatty = lambda: False
        stderr.isatty = lambda: True
        with patch.object(initialise, 'orig_stdout', stdout):
            with patch.object(initialise, 'orig_stderr', stderr):
                with patch('colorama.ansitowin32.winapi_test',
                           return_value=False):
                    initialise.reset_all()
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), Style.RESET_ALL)

    def test_absent_streams_and_shutdown(self):
        with patch.object(initialise, 'orig_stdout', None):
            with patch.object(initialise, 'orig_stderr', None):
                initialise.reset_all()
        with patch.object(initialise, 'AnsiToWin32', None):
            initialise.reset_all()
