# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import sys
try:
    from unittest2 import TestCase, main
except ImportError:
    from unittest import TestCase, main

from mock import patch

from .utils import platform, redirected_output, replace_by_none

from ..initialise import init
from ..ansitowin32 import StreamWrapper
import os

orig_stdout = sys.stdout
orig_stderr = sys.stderr


class InitTest(TestCase):

    def setUp(self):
        # sanity check
        self.assertNotWrapped()

    def tearDown(self):
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    def assertWrapped(self):
        self.assertIsNot(sys.stdout, orig_stdout, 'stdout should be wrapped')
        self.assertIsNot(sys.stderr, orig_stderr, 'stderr should be wrapped')
        self.assertTrue(isinstance(sys.stdout, StreamWrapper),
            'bad stdout wrapper')
        self.assertTrue(isinstance(sys.stderr, StreamWrapper),
            'bad stderr wrapper')

    def assertNotWrapped(self):
        self.assertIs(sys.stdout, orig_stdout, 'stdout should not be wrapped')
        self.assertIs(sys.stderr, orig_stderr, 'stderr should not be wrapped')

    @patch('colorama.initialise.reset_all')
    @patch('os.environ', dict())
    def testInitWrapsOnWindows(self, _):
        with platform('windows'):
            init()
            self.assertWrapped()

    @patch('colorama.initialise.reset_all')
    @patch('os.environ', dict(TERM=''))
    def testInitDoesntWrapOnEmulatedWindows(self, _):
        with platform('windows'):
            os.environ['TERM']
            init()
            self.assertNotWrapped()

    def testInitDoesntWrapOnNonWindows(self):
        with platform('darwin'):
            init()
            self.assertNotWrapped()

    def testInitDoesntWrapIfNone(self):
        with replace_by_none():
            init()
            # We can't use assertNotWrapped here because replace_by_none
            # changes stdout/stderr already.
            self.assertIsNone(sys.stdout)
            self.assertIsNone(sys.stderr)

    def testInitAutoresetOnWrapsOnAllPlatforms(self):
        with platform('darwin'):
            init(autoreset=True)
            self.assertWrapped()

    def testInitWrapOffDoesntWrapOnWindows(self):
        with platform('windows'):
            init(wrap=False)
            self.assertNotWrapped()

    def testInitWrapOffWillUnwrapIfRequired(self):
        with platform('windows'):
            init()
            init(wrap=False)
            self.assertNotWrapped()

    def testInitWrapOffIncompatibleWithAutoresetOn(self):
        self.assertRaises(ValueError, lambda: init(autoreset=True, wrap=False))

    @patch('colorama.ansitowin32.winterm', None)
    @patch('os.environ', dict())
    def testInitOnlyWrapsOnce(self):
        with platform('windows'):
            init()
            init()
            self.assertWrapped()

    @patch('colorama.win32.SetConsoleTextAttribute')
    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetPassedOn(self, mockATW32, _):
        with platform('windows'):
            init(autoreset=True)
            self.assertEqual(len(mockATW32.call_args_list), 2)
            self.assertEqual(mockATW32.call_args_list[1][1]['autoreset'], True)
            self.assertEqual(mockATW32.call_args_list[0][1]['autoreset'], True)

    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetChangeable(self, mockATW32):
        with platform('windows'):
            init()

            init(autoreset=True)
            self.assertEqual(len(mockATW32.call_args_list), 4)
            self.assertEqual(mockATW32.call_args_list[2][1]['autoreset'], True)
            self.assertEqual(mockATW32.call_args_list[3][1]['autoreset'], True)

            init()
            self.assertEqual(len(mockATW32.call_args_list), 6)
            self.assertEqual(
                mockATW32.call_args_list[4][1]['autoreset'], False)
            self.assertEqual(
                mockATW32.call_args_list[5][1]['autoreset'], False)


    @patch('colorama.initialise.atexit.register')
    def testAtexitRegisteredOnlyOnce(self, mockRegister):
        init()
        self.assertTrue(mockRegister.called)
        mockRegister.reset_mock()
        init()
        self.assertFalse(mockRegister.called)


if __name__ == '__main__':
    main()

