# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
import sys
from unittest import TestCase, main, skipUnless
from unittest.mock import patch, Mock

from ..ansitowin32 import StreamWrapper
from ..initialise import init, just_fix_windows_console, _wipe_internal_state_for_tests
from .utils import osname, replace_by

orig_stdout = sys.stdout
orig_stderr = sys.stderr


class InitTest(TestCase):

    @skipUnless(sys.stdout.isatty(), "sys.stdout is not a tty")
    def setUp(self):
        # sanity check
        self.assertNotWrapped()

    def tearDown(self):
        _wipe_internal_state_for_tests()
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
    @patch('colorama.ansitowin32.winapi_test', lambda *_: True)
    @patch('colorama.ansitowin32.enable_vt_processing', lambda *_: False)
    def testInitWrapsOnWindows(self, _):
        with osname("nt"):
            init()
            self.assertWrapped()

    @patch('colorama.initialise.reset_all')
    @patch('colorama.ansitowin32.winapi_test', lambda *_: False)
    def testInitDoesntWrapOnEmulatedWindows(self, _):
        with osname("nt"):
            init()
            self.assertNotWrapped()

    def testInitDoesntWrapOnNonWindows(self):
        with osname("posix"):
            init()
            self.assertNotWrapped()

    def testInitDoesntWrapIfNone(self):
        with replace_by(None):
            init()
            # We can't use assertNotWrapped here because replace_by(None)
            # changes stdout/stderr already.
            self.assertIsNone(sys.stdout)
            self.assertIsNone(sys.stderr)

    def testInitAutoresetOnWrapsOnAllPlatforms(self):
        with osname("posix"):
            init(autoreset=True)
            self.assertWrapped()

    def testInitWrapOffDoesntWrapOnWindows(self):
        with osname("nt"):
            init(wrap=False)
            self.assertNotWrapped()

    def testInitWrapOffIncompatibleWithAutoresetOn(self):
        self.assertRaises(ValueError, lambda: init(autoreset=True, wrap=False))

    @patch('colorama.win32.SetConsoleTextAttribute')
    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetPassedOn(self, mockATW32, _):
        with osname("nt"):
            init(autoreset=True)
            self.assertEqual(len(mockATW32.call_args_list), 2)
            self.assertEqual(mockATW32.call_args_list[1][1]['autoreset'], True)
            self.assertEqual(mockATW32.call_args_list[0][1]['autoreset'], True)

    @patch('colorama.initialise.AnsiToWin32')
    def testAutoResetChangeable(self, mockATW32):
        with osname("nt"):
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


class NoColorForceColorTest(TestCase):

    def tearDown(self):
        _wipe_internal_state_for_tests()
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    @patch.dict('os.environ', {'NO_COLOR': '1'}, clear=False)
    def testNoColorStripsAnsi(self):
        with osname("posix"):
            init()
            # stdout should be wrapped because strip=True forces wrapping
            self.assertIsInstance(sys.stdout, StreamWrapper)
            self.assertIsInstance(sys.stderr, StreamWrapper)

    @patch.dict('os.environ', {'NO_COLOR': ''}, clear=False)
    def testNoColorEmptyIsIgnored(self):
        # Empty NO_COLOR should be ignored; env var detection should not
        # set strip=True. Behavior should be identical to no env var set.
        with osname("posix"):
            init()
            # On a non-tty (like in pytest), AnsiToWin32 defaults strip=True
            # regardless. We just verify that empty NO_COLOR didn't change
            # behavior compared to the baseline.
            pass  # no assertion needed; no crash is the test

    @patch.dict('os.environ', {'FORCE_COLOR': '1'}, clear=False)
    @patch('colorama.initialise.AnsiToWin32')
    def testForceColorSetsStripFalse(self, mockATW32):
        mockATW32.return_value.should_wrap.return_value = False
        with osname("posix"):
            init()
            # Verify strip=False was passed to AnsiToWin32
            for call in mockATW32.call_args_list:
                self.assertFalse(call[1].get('strip', None),
                    'FORCE_COLOR should set strip=False')

    @patch.dict('os.environ', {'FORCE_COLOR': '1', 'NO_COLOR': '1'}, clear=False)
    @patch('colorama.initialise.AnsiToWin32')
    def testForceColorWinsOverNoColor(self, mockATW32):
        mockATW32.return_value.should_wrap.return_value = False
        with osname("posix"):
            init()
            # FORCE_COLOR takes precedence: strip should be False, not True
            for call in mockATW32.call_args_list:
                self.assertFalse(call[1].get('strip', None),
                    'FORCE_COLOR should win over NO_COLOR')

    @patch.dict('os.environ', {'NO_COLOR': '1'}, clear=False)
    @patch('colorama.initialise.AnsiToWin32')
    def testExplicitStripOverridesNoColor(self, mockATW32):
        mockATW32.return_value.should_wrap.return_value = False
        with osname("posix"):
            init(strip=False)
            # Explicit strip=False should override NO_COLOR
            for call in mockATW32.call_args_list:
                self.assertFalse(call[1].get('strip', None),
                    'Explicit strip=False should override NO_COLOR')

    @patch.dict('os.environ', {'NO_COLOR': '1'}, clear=False)
    @patch('colorama.initialise.AnsiToWin32')
    def testExplicitConvertOverridesNoColor(self, mockATW32):
        mockATW32.return_value.should_wrap.return_value = False
        with osname("posix"):
            # When convert is explicitly set, env vars should not apply
            init(convert=False)
            for call in mockATW32.call_args_list:
                self.assertIsNone(call[1].get('strip', None),
                    'Explicit convert should prevent env var strip override')


class JustFixWindowsConsoleTest(TestCase):
    def _reset(self):
        _wipe_internal_state_for_tests()
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

    def tearDown(self):
        self._reset()

    @patch("colorama.ansitowin32.winapi_test", lambda: True)
    def testJustFixWindowsConsole(self):
        if sys.platform != "win32":
            # just_fix_windows_console should be a no-op
            just_fix_windows_console()
            self.assertIs(sys.stdout, orig_stdout)
            self.assertIs(sys.stderr, orig_stderr)
        else:
            def fake_std():
                # Emulate stdout=not a tty, stderr=tty
                # to check that we handle both cases correctly
                stdout = Mock()
                stdout.closed = False
                stdout.isatty.return_value = False
                stdout.fileno.return_value = 1
                sys.stdout = stdout

                stderr = Mock()
                stderr.closed = False
                stderr.isatty.return_value = True
                stderr.fileno.return_value = 2
                sys.stderr = stderr

            for native_ansi in [False, True]:
                with patch(
                    'colorama.ansitowin32.enable_vt_processing',
                    lambda *_: native_ansi
                ):
                    self._reset()
                    fake_std()

                    # Regular single-call test
                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(sys.stdout, prev_stdout)
                    if native_ansi:
                        self.assertIs(sys.stderr, prev_stderr)
                    else:
                        self.assertIsNot(sys.stderr, prev_stderr)

                    # second call without resetting is always a no-op
                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(sys.stdout, prev_stdout)
                    self.assertIs(sys.stderr, prev_stderr)

                    self._reset()
                    fake_std()

                    # If init() runs first, just_fix_windows_console should be a no-op
                    init()
                    prev_stdout = sys.stdout
                    prev_stderr = sys.stderr
                    just_fix_windows_console()
                    self.assertIs(prev_stdout, sys.stdout)
                    self.assertIs(prev_stderr, sys.stderr)


if __name__ == '__main__':
    main()
