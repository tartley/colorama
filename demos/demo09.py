from __future__ import print_function
import fixpath
from colorama import Fore, Back, colorama, init


def main():
    print('Before any, ', end='')
    with colorama(Back.RED):
        print('inside one, ', end='')
        with colorama(Back.WHITE, Fore.BLACK):
            print('inside two, ', end='')
        print('context ', end='')
    print('managers.', end='')

if __name__ == '__main__':
    init()
    main()
