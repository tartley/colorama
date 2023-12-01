from typing_extensions import Final

CSI: str
OSC: str
BEL: str

def code_to_chars(code: int) -> str: ...
def set_title(title: str) -> str: ...
def clear_screen(mode: int = 2) -> str: ...
def clear_line(mode: int = 2) -> str: ...

class AnsiCodes:
    def __init__(self) -> None: ...

class AnsiCursor:
    def UP(self, n: int = 1) -> str: ...
    def DOWN(self, n: int = 1) -> str: ...
    def FORWARD(self, n: int = 1) -> str: ...
    def BACK(self, n: int = 1) -> str: ...
    def POS(self, x: int = 1, y: int = 1) -> str: ...

# All attributes in the following classes are string in instances and int in the class.
# We use str since that is the common case for users.
class AnsiFore(AnsiCodes):
    BLACK: Final = 30
    RED: Final = 31
    GREEN: Final = 32
    YELLOW: Final = 33
    BLUE: Final = 34
    MAGENTA: Final = 35
    CYAN: Final = 36
    WHITE: Final = 37
    RESET: Final = 39
    LIGHTBLACK_EX: Final = 90
    LIGHTRED_EX: Final = 91
    LIGHTGREEN_EX: Final = 92
    LIGHTYELLOW_EX: Final = 93
    LIGHTBLUE_EX: Final = 94
    LIGHTMAGENTA_EX: Final = 95
    LIGHTCYAN_EX: Final = 96
    LIGHTWHITE_EX: Final = 97

class AnsiBack(AnsiCodes):
    BLACK: Final = 40
    RED: Final = 41
    GREEN: Final = 42
    YELLOW: Final = 43
    BLUE: Final = 44
    MAGENTA: Final = 45
    CYAN: Final = 46
    WHITE: Final = 47
    RESET: Final = 49
    LIGHTBLACK_EX: Final = 100
    LIGHTRED_EX: Final = 101
    LIGHTGREEN_EX: Final = 102
    LIGHTYELLOW_EX: Final = 103
    LIGHTBLUE_EX: Final = 104
    LIGHTMAGENTA_EX: Final = 105
    LIGHTCYAN_EX: Final = 106
    LIGHTWHITE_EX: Final = 107

class AnsiStyle(AnsiCodes):
    BRIGHT: Final = 1
    DIM: Final = 2
    NORMAL: Final = 22
    RESET_ALL: Final = 0

Fore: AnsiFore
Back: AnsiBack
Style: AnsiStyle
Cursor: AnsiCursor
