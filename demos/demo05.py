#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# Demonstrate the difference between colorama initialized with wrapping on and off.
# The point of the demonstration is to show how the ANSI wrapping on Windows can be disabled.
# The unwrapped cases will be interpreted with ANSI on Unix, but not on Windows.

import sys

import fixpath

from colorama import AnsiToWin32, Fore, init

init()
print(f'{Fore.YELLOW}Wrapped yellow going to stdout, via the default print function.')

init(wrap=False)
print(f'{Fore.CYAN}Unwrapped CYAN going to stdout, via the default print function.')
print(f'{Fore.CYAN}Unwrapped CYAN, using the file parameter to write via colorama the AnsiToWin32 function.', file=AnsiToWin32(sys.stdout))
print(f'{Fore.RED}Unwrapped RED going to stdout, via the default print function.')

init()
print(f'{Fore.RED}Wrapped RED going to stdout, via the default print function.')
