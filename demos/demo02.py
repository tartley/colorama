#!/usr/bin/python

# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
# SPDX-FileCopyrightText: 2013-2022 Jonathan Hartley & Arnon Yaari
#
# SPDX-License-Identifier: BSD-3-Clause

# Simple demo of changing foreground, background and brightness.

from __future__ import print_function
import fixpath
from colorama import init, Fore, Back, Style

init()

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
