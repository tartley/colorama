#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# check that stripped ANSI in redirected stderr does not affect stdout
from __future__ import print_function
import sys
import fixpath
from colorama import init, Fore

init()
print(Fore.GREEN + 'GREEN set on stdout. ', end='')
print(Fore.RED + 'RED redirected stderr', file=sys.stderr)
print('Further stdout should be GREEN, i.e., the stderr redirection should not affect stdout.')
