from .ansi import Style, Fore


RESET = Style.RESET_ALL

class Color(str):
    color: str
    def __init__(self, msg: str):
        self.msg = msg.strip(RESET).replace(RESET, RESET + self.color)

    def __str__(self) -> str:
        return f"{self.color}{self.msg}{RESET}"

    def __add__(self, other: str) -> str:
        return f"{self}{other}"

    def __radd__(self, other: str) -> str:
        return f"{other}{self}"


class Black(Color):
    color: str = Fore.BLACK


class Red(Color):
    color: str = Fore.RED


class Green(Color):
    color: str = Fore.GREEN


class Yellow(Color):
    color: str = Fore.YELLOW


class Blue(Color):
    color: str = Fore.BLUE


class Magenta(Color):
    color: str = Fore.MAGENTA


class Cyan(Color):
    color: str = Fore.CYAN


class White(Color):
    color: str = Fore.WHITE

