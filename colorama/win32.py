# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

from . import windows_437

# from winbase.h
STDOUT = -11
STDERR = -12

ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

try:
    import ctypes
    from ctypes import LibraryLoader
    windll = LibraryLoader(ctypes.WinDLL)
    from ctypes import wintypes
except (AttributeError, ImportError):
    windll = None
    SetConsoleTextAttribute = lambda *_: None
    winapi_test = lambda *_: None
else:
    from ctypes import byref, Structure, c_char, POINTER

    COORD = wintypes._COORD

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("dwSize", COORD),
            ("dwCursorPosition", COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", COORD),
        ]
        def __str__(self):
            return '(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (
                self.dwSize.Y, self.dwSize.X
                , self.dwCursorPosition.Y, self.dwCursorPosition.X
                , self.wAttributes
                , self.srWindow.Top, self.srWindow.Left, self.srWindow.Bottom, self.srWindow.Right
                , self.dwMaximumWindowSize.Y, self.dwMaximumWindowSize.X
            )

    _GetStdHandle = windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
        wintypes.DWORD,
    ]
    _GetStdHandle.restype = wintypes.HANDLE

    _GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [
        wintypes.HANDLE,
        POINTER(CONSOLE_SCREEN_BUFFER_INFO),
    ]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    _SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    _SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
    ]
    _SetConsoleTextAttribute.restype = wintypes.BOOL

    _SetConsoleCursorPosition = windll.kernel32.SetConsoleCursorPosition
    _SetConsoleCursorPosition.argtypes = [
        wintypes.HANDLE,
        COORD,
    ]
    _SetConsoleCursorPosition.restype = wintypes.BOOL

    _FillConsoleOutputCharacterA = windll.kernel32.FillConsoleOutputCharacterA
    _FillConsoleOutputCharacterA.argtypes = [
        wintypes.HANDLE,
        c_char,
        wintypes.DWORD,
        COORD,
        POINTER(wintypes.DWORD),
    ]
    _FillConsoleOutputCharacterA.restype = wintypes.BOOL

    _FillConsoleOutputAttribute = windll.kernel32.FillConsoleOutputAttribute
    _FillConsoleOutputAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
        wintypes.DWORD,
        COORD,
        POINTER(wintypes.DWORD),
    ]
    _FillConsoleOutputAttribute.restype = wintypes.BOOL

    _SetConsoleTitleW = windll.kernel32.SetConsoleTitleW
    _SetConsoleTitleW.argtypes = [
        wintypes.LPCWSTR
    ]
    _SetConsoleTitleW.restype = wintypes.BOOL

    _GetConsoleMode = windll.kernel32.GetConsoleMode
    _GetConsoleMode.argtypes = [
        wintypes.HANDLE,
        POINTER(wintypes.DWORD)
    ]
    _GetConsoleMode.restype = wintypes.BOOL

    _SetConsoleMode = windll.kernel32.SetConsoleMode
    _SetConsoleMode.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD
    ]
    _SetConsoleMode.restype = wintypes.BOOL

    _GetConsoleOutputCP = windll.kernel32.GetConsoleOutputCP
    _GetConsoleOutputCP.argtypes = []
    _GetConsoleOutputCP.restype = wintypes.UINT

    _GetConsoleCP = windll.kernel32.GetConsoleCP
    _GetConsoleCP.argtypes = []
    _GetConsoleCP.restype = wintypes.UINT

    def _winapi_test(handle):
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = _GetConsoleScreenBufferInfo(
            handle, byref(csbi))
        return bool(success)

    def winapi_test():
        return any(_winapi_test(h) for h in
                   (_GetStdHandle(STDOUT), _GetStdHandle(STDERR)))

    def GetConsoleScreenBufferInfo(stream_id=STDOUT):
        handle = _GetStdHandle(stream_id)
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = _GetConsoleScreenBufferInfo(
            handle, byref(csbi))
        return csbi

    def SetConsoleTextAttribute(stream_id, attrs):
        handle = _GetStdHandle(stream_id)
        return _SetConsoleTextAttribute(handle, attrs)

    def SetConsoleCursorPosition(stream_id, position, adjust=True):
        position = COORD(*position)
        # If the position is out of range, do nothing.
        if position.Y <= 0 or position.X <= 0:
            return
        # Adjust for Windows' SetConsoleCursorPosition:
        #    1. being 0-based, while ANSI is 1-based.
        #    2. expecting (x,y), while ANSI uses (y,x).
        adjusted_position = COORD(position.Y - 1, position.X - 1)
        if adjust:
            # Adjust for viewport's scroll position
            sr = GetConsoleScreenBufferInfo(STDOUT).srWindow
            adjusted_position.Y += sr.Top
            adjusted_position.X += sr.Left
        # Resume normal processing
        handle = _GetStdHandle(stream_id)
        return _SetConsoleCursorPosition(handle, adjusted_position)

    def FillConsoleOutputCharacter(stream_id, char, length, start):
        handle = _GetStdHandle(stream_id)
        char = c_char(char.encode())
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        # Note that this is hard-coded for ANSI (vs wide) bytes.
        success = _FillConsoleOutputCharacterA(
            handle, char, length, start, byref(num_written))
        return num_written.value

    def FillConsoleOutputAttribute(stream_id, attr, length, start):
        ''' FillConsoleOutputAttribute( hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten )'''
        handle = _GetStdHandle(stream_id)
        attribute = wintypes.WORD(attr)
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        # Note that this is hard-coded for ANSI (vs wide) bytes.
        return _FillConsoleOutputAttribute(
            handle, attribute, length, start, byref(num_written))

    def SetConsoleTitle(title):
        return _SetConsoleTitleW(title)

    def GetConsoleMode(handle):
        mode = wintypes.DWORD()
        success = _GetConsoleMode(handle, byref(mode))
        if not success:
            raise ctypes.WinError()
        return mode.value

    def SetConsoleMode(handle, mode):
        success = _SetConsoleMode(handle, mode)
        if not success:
            raise ctypes.WinError()

    def GetConsoleCP():
        codepage = _GetConsoleCP()
        if not codepage:
            raise ctypes.WinError()
        return codepage

    def GetConsoleOutputCP():
        codepage = _GetConsoleOutputCP()
        if not codepage:
            raise ctypes.WinError()
        return codepage

# https://learn.microsoft.com/en-us/windows/win32/intl/code-page-identifiers
MICROSOFT_CODEPAGE_ENCODING = {
  437: 'x-windows-437',

  708: 'iso-8859-6',
  709: 'iso-9036',
  932: 'shift_jis',
  936: 'gb2312',
  950: 'big5',
  1047: 'x-ebcdic-latin1',
  1140: 'x-ebcdic-us-ca-eu',
  1141: 'x-ebcdic-de-eu',
  1142: 'x-ebcdic-dk-no-eu',
  1143: 'x-ebcdic-fi-se-eu',
  1144: 'x-ebcdic-it-eu',
  1145: 'x-ebcdic-es-eu',
  1146: 'x-ebcdic-gb-eu',
  1147: 'x-ebcdic-fr-eu',
  1148: 'x-ebcdic-int-eu',
  1149: 'x-ebcdic-is-eu',
  1200: 'utf-16le',
  1201: 'utf-16be',
  1250: 'windows-1250',
  1251: 'windows-1251',
  1252: 'windows-1252',
  1253: 'windows-1253',
  1254: 'windows-1254',
  1255: 'windows-1255',
  1256: 'windows-1256',
  1257: 'windows-1257',
  1258: 'windows-1258',
  1361: 'johab',
  10000: 'macintosh',
  10001: 'x-mac-japanese',
  10002: 'x-mac-trad-chinese',
  10003: 'x-mac-korean',
  10004: 'mac-arabic',
  10005: 'x-mac-hebrew',
  10006: 'mac-greek',
  10007: 'mac-cyrillic',
  10008: 'x-mac-simp-chinese',
  10010: 'mac-romanian',
  10017: 'x-mac-ukrainian',
  10021: 'x-mac-thai',
  10029: 'mac-centeuro',
  10079: 'mac-iceland',
  10081: 'mac-turkish',
  10082: 'mac-croatian',
  12000: 'utf-32le',
  12001: 'utf-32be',
  20000: 'x-chinese-cns',
  20001: 'x-cp20001',
  20002: 'x-chinese-eten',
  20105: 'x-ia5',
  20106: 'x-ia5-german',
  20107: 'x-ia5-swedish',
  20108: 'x-ia5-norwegian',
  20127: 'us-ascii',
  20277: 'x-ebcdic-dk-no',
  20278: 'x-ebcdic-fi-se',
  20280: 'x-ebcdic-it',
  20284: 'x-ebcdic-es',
  20285: 'x-ebcdic-gb',
  20290: 'x-ebcdic-jp-kana',
  20297: 'x-ebcdic-fr',
  20420: 'x-ebcdic-ar1',
  20423: 'x-ebcdic-gr',
  20833: 'x-ebcdic-koreanextended',
  20838: 'x-ebcdic-thai',
  20866: 'koi8-r',
  20932: 'euc-jp',
  20936: 'x-cp20936',
  20949: 'x-cp20949',
  21866: 'koi8-u',
  28591: 'iso-8859-1',
  28592: 'iso-8859-2',
  28593: 'iso-8859-3',
  28594: 'iso-8859-4',
  28595: 'iso-8859-5',
  28596: 'iso-8859-6',
  28597: 'iso-8859-7',
  28598: 'iso-8859-8',
  28599: 'iso-8859-9',
  28603: 'iso-8859-13',
  28605: 'iso-8859-15',
  38598: 'iso-8859-8-i',
  50220: 'iso-2022-jp',
  50221: 'csiso2022jp',
  50222: 'iso-2022-jp',
  50225: 'iso-2022-kr',
  50227: 'x-cp50227',
  51932: 'euc-jp',
  51936: 'euc-cn',
  51949: 'euc-kr',
  52936: 'hz-gb-2312',
  54936: 'gb18030',
  57002: 'x-iscii-de',
  57003: 'x-iscii-be',
  57004: 'x-iscii-ta',
  57005: 'x-iscii-te',
  57006: 'x-iscii-as',
  57007: 'x-iscii-or',
  57008: 'x-iscii-ka',
  57009: 'x-iscii-ma',
  57010: 'x-iscii-gu',
  57011: 'x-iscii-pa',
  65000: 'utf-7',
  65001: 'utf-8'}
