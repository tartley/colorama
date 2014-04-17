#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# Demonstrate the different behavior when autoreset is True and False.

from __future__ import print_function
import fixpath
from colorama import init, Fore, Back, Style

init(autoreset=True)
print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + 'Line 1: colored, with autoreset=True')
print('Line 2: When auto reset is True, the color settings need to be set with every print.')

init(autoreset=False)
print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + 'Line 3: colored, with autoreset=False')
print('Line 4: When autoreset=False, the prior color settings linger (this is the default behavior).')
