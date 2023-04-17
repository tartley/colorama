# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from __future__ import print_function

from random import choice, randint
from string import printable

import fixpath

import colorama
from colorama import Back, Cursor, Fore, Style

# Demonstrate printing colored, random characters at random positions on the screen

# Fore, Back and Style are convenience classes for the constant ANSI strings that set
#     the foreground, background and style. They don't have any magic of their own.
FORES = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
BACKS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]
STYLES = [Style.DIM, Style.NORMAL, Style.BRIGHT]

# This assumes your terminal is 80x24. Ansi minimum coordinate is (1,1).
MINY, MAXY = 1, 24
MINX, MAXX = 1, 80

# set of printable ASCII characters, including a space.
CHARS = ' ' + printable.strip()

PASSES = 1000


def main():
    colorama.just_fix_windows_console()
    def pos(y, x):
        return Cursor.POS(x, y)
    # draw a white border.
    print(Back.WHITE, end='')
    print(f"{pos(MINY, MINX)}{' ' * MAXX}", end='')
    for y in range(MINY, 1 + MAXY):
        print(f'{pos(y, MINX)} {pos(y, MAXX)} ', end='')
    print(f"{pos(MAXY, MINX)}{' ' * MAXX}", end='')
    # draw some blinky lights for a while.
    for _ in range(PASSES):
        print(f'{pos(randint(1 + MINY, MAXY - 1), randint(1 + MINX, MAXX - 1))}{choice(FORES)}{choice(BACKS)}{choice(STYLES)}{choice(CHARS)}', end='')
    # put cursor to top, left, and set color to white-on-black with normal brightness.
    print(f'{pos(MINY, MINX)}{Fore.WHITE}{Back.BLACK}{Style.NORMAL}', end='')


if __name__ == '__main__':
    main()
