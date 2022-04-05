#!/usr/bin/python

# SPDX-FileCopyrightText: 2013-2022 Jonathan Hartley & Arnon Yaari
#
# SPDX-License-Identifier: BSD-3-Clause

# Demonstrate the difference between colorama initialized with wrapping on and off.
# The point of the demonstration is to show how the ANSI wrapping on Windows can be disabled.
# The unwrapped cases will be interpreted with ANSI on Unix, but not on Windows.

from __future__ import print_function
import sys
import fixpath
from colorama import AnsiToWin32, init, Fore

init()
print('%sWrapped yellow going to stdout, via the default print function.' % Fore.YELLOW)

init(wrap=False)
print('%sUnwrapped CYAN going to stdout, via the default print function.' % Fore.CYAN)
print('%sUnwrapped CYAN, using the file parameter to write via colorama the AnsiToWin32 function.' % Fore.CYAN, file=AnsiToWin32(sys.stdout))
print('%sUnwrapped RED going to stdout, via the default print function.' % Fore.RED)

init()
print('%sWrapped RED going to stdout, via the default print function.' % Fore.RED)
