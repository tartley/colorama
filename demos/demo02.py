#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# Simple demo of changing foreground, background and brightness.

import fixpath

from colorama import Back, Fore, Style, just_fix_windows_console

just_fix_windows_console()

print(Fore.GREEN + 'green, '
    + Fore.RED + 'red, '
    + Fore.RESET + 'normal, '
    , end='')
print(Back.GREEN + 'green, '
    + Back.RED + 'red, '
    + Back.RESET + 'normal, '
    , end='')
print(Style.DIM + 'dim, '
    + Style.BRIGHT + 'bright, '
    + Style.NORMAL + 'normal'
    , end=' ')
print()
