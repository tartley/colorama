# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''

CSI = '\033['
OSC = '\033]'
BEL = '\007'


def code_to_chars(code):
    return CSI + str(code) + 'm'

def set_title(title):
    return OSC + '2;' + title + BEL

def clear_screen(mode=2):
    return CSI + str(mode) + 'J'

def clear_line(mode=2):
    return CSI + str(mode) + 'K'


# This function needs to be able to take ANY given ANSI Color String and return
# It's value as the next incremented color code.
def increment_color(code):
    """ Takes a Given Color Code Defined in a Subclass of AnsiCodes,
    and returns the next modulating non-reseting color.

    :param code: ANSI Color Constant defined in either Fore, Back, or Style.
     These Color Constants come in the form '\033['+ X + 'm', where X is the actual integer that we want.
    :type code: str
    :return: Another ANSI Color Constant defined in the corresponding subclasses
    :rtype: str
    """
    # Extract the number from the code, this strips all the strings away from the number,
    # And allows us to simply convert from string to integer directly
    color_num = int(code.lstrip(CSI).rstrip('m'))

    # Fore Integers are defined 30-37, 90-97. 39 is a reset value, and 38 is a blank
    # Back Integers are defined 40-47, 100-107, 49 is a reset value, and 48 is also a blank
    # Style Integers are defined as 1,2 & 22. 0 is a reset value.

    # We want the Style, Fore, and Back integers to stay in their respective class,
    # Which eliminates the possibility of using a circular buffer.

    # Instead we have to use this spaghetti code logic in order to handle the fringe cases
    # Ensuring that we're incrementing when needed and decrementing to the correct positions.

    # Handle the fringe cases for the Fore and Back ANSI codes to jump to the non-standard codes
    color_num = color_num + 53 if color_num == 47 or color_num == 37 else\
                color_num - 67 if color_num == 107 or color_num == 97 else\
                color_num + 1 if color_num >= 30 and color_num != (39 and 49) else\
                1 if color_num == 22 else\
                2 if color_num == 1 else\
                22 if color_num == 2 else\
                1 if color_num == 0 else color_num + 51

    # At this point, 39 & 49 would be the only ones left
    # So we just add 51 to them bringing them up to 90 or 100

    # Return it as a string prepended with CSI and appended with 'm'
    return CSI + str(color_num) + 'm'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + 'A'
    def DOWN(self, n=1):
        return CSI + str(n) + 'B'
    def FORWARD(self, n=1):
        return CSI + str(n) + 'C'
    def BACK(self, n=1):
        return CSI + str(n) + 'D'
    def POS(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37
    RESET           = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 90
    LIGHTRED_EX     = 91
    LIGHTGREEN_EX   = 92
    LIGHTYELLOW_EX  = 93
    LIGHTBLUE_EX    = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX    = 96
    LIGHTWHITE_EX   = 97


class AnsiBack(AnsiCodes):
    BLACK           = 40
    RED             = 41
    GREEN           = 42
    YELLOW          = 43
    BLUE            = 44
    MAGENTA         = 45
    CYAN            = 46
    WHITE           = 47
    RESET           = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 100
    LIGHTRED_EX     = 101
    LIGHTGREEN_EX   = 102
    LIGHTYELLOW_EX  = 103
    LIGHTBLUE_EX    = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX    = 106
    LIGHTWHITE_EX   = 107


class AnsiStyle(AnsiCodes):
    BRIGHT    = 1
    DIM       = 2
    NORMAL    = 22
    RESET_ALL = 0

Fore   = AnsiFore()
Back   = AnsiBack()
Style  = AnsiStyle()
Cursor = AnsiCursor()
