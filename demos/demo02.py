#!/usr/bin/python
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

# Simple demo of changing foreground, background and brightness.

from __future__ import print_function
import fixpath
from colorama import init, Fore, Back, Style

init()

colors = ('green', 'red', 'normal')
styles = ('dim', 'bright', 'normal')

fore = (Fore.GREEN, Fore.RED, Fore.RESET)
back = (Back.GREEN, Back.RED, Back.RESET)
style = (Style.DIM, Style.BRIGHT, Style.NORMAL)

output = [fore[i] + colors[i] for i in range(3)]
output.extend([back[i] + colors[i] for i in range(3)])
output.extend([style[i] + styles[i] for i in range(3)])
print(', '.join(output))
