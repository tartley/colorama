import sys
import unittest
from unittest.mock import patch, MagicMock
from colorama import init, deinit

class TestColoramaInitialise(unittest.TestCase):

    @patch('colorama.ansitowin32.AnsiToWin32')
    def test_init_deinit(self, mock_ansitowin32):
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # First call to init
        init()
        self.assertIsNotNone(sys.stdout)
        self.assertIsNotNone(sys.stderr)

        # Second call to init
        init()
        self.assertIsNotNone(sys.stdout)
        self.assertIsNotNone(sys.stderr)

        # Call deinit
        deinit()

        # Verify stdout and stderr are restored correctly
        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)

if __name__ == '__main__':
    unittest.main()