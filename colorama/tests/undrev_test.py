import colorama
# some ANSI escape sequence for colours and effects.
BLACK = '\u001b[30m'
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
BLUE   = '\u001b[34m'
MAGENTA = '\u001b[35m'
CYAN   = '\u001b[36m'
WHITE  = '\u001b[37m'
RESET  = '\u001b[0m'

BOLD    = '\u001b[1m'
UNDERLINE   = '\u001b[4m'
REVERSE     = '\u001b[7m'


print(RED, "this will be in red")
print(" and this one also")

print()

def colour_print(text: str, effect: str) -> None:
    """
    Print 'text' using the ANSI sequence to change colour, etc
    :param text: The text we want to print
    :param effect: The effect we want. One of the constants
    defined at the start of this module.
    """
    output_string = "{0}{1}{2}".format(effect, text, RESET)
    print(output_string)


# colorama.init()
colour_print("Hello, red", RED)
# Check that the colour was reset.
print("This should be in the default terminal colour")
colour_print("Hello, Blue", BLUE)
colour_print("Hello, Yellow", YELLOW)
colour_print("Hello, Bold", BOLD)
colour_print("Hello, Underline", UNDERLINE)
colour_print("Hello, Reverse", REVERSE)
colour_print("Hello, Black", BLACK)

print(colorama.Style.REVERSE_OFF + colorama.Back.GREEN + "off?" + colorama.Style.RESET_ALL)
print(colorama.Style.REVERSE + colorama.Back.GREEN + "off?" + colorama.Style.RESET_ALL)

print(colorama.Style.REVERSE + colorama.Style.REVERSE_OFF + colorama.Back.GREEN + "off?" + colorama.Style.RESET_ALL)

# colorama.deinit()
