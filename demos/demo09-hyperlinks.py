from __future__ import print_function
import fixpath
from colorama import colorama_text, Fore, link


def main():
    """automatically reset stdout"""
    with colorama_text():
        print(Fore.GREEN + 'text is green')
        print(Fore.RESET + 'text is back to normal')
        print('This ' + link('https://google.com', 'link') + ' should be clickable')

    print('text is back to stdout')

if __name__ == '__main__':
    main()
