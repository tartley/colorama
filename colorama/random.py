import random

class color : 
    def __init__(self) -> None:pass
    def Color(text:str): 
        # list color in pyhton ! 
        ResetAll = "\033[0m";Bold       = "\033[1m";Dim        = "\033[2m"
        Underlined = "\033[4m";Blink      = "\033[5m";Reverse    = "\033[7m";Hidden     = "\033[8m" 
        # colors
        Cyan = "\033[36m"  ; Purple = "\033[35m" ; blue = "\033[34" 
        Brown = "\033[33m" ; Dark_Gray = "\033[1;30m"
        CEND      = '\33[0m'
        CBOLD     = '\33[1m'
        CITALIC   = '\33[3m'
        CURL      = '\33[4m'
        CBLINK    = '\33[5m'
        CBLINK2   = '\33[6m'
        CSELECTED = '\33[7m'
        CBLACK  = '\33[30m'
        CRED    = '\33[31m'
        CGREEN  = '\33[32m'
        CYELLOW = '\33[33m'
        CBLUE   = '\33[34m'
        CVIOLET = '\33[35m'
        CBEIGE  = '\33[36m'
        CWHITE  = '\33[37m'
        CBLACKBG  = '\33[40m'
        CREDBG    = '\33[41m'
        CGREENBG  = '\33[42m'
        CYELLOWBG = '\33[43m'
        CBLUEBG   = '\33[44m'
        CVIOLETBG = '\33[45m'
        CBEIGEBG  = '\33[46m'
        CWHITEBG  = '\33[47m'
        CGREY    = '\33[90m'
        CRED2    = '\33[91m'
        CGREEN2  = '\33[92m'
        CYELLOW2 = '\33[93m'
        CBLUE2   = '\33[94m'
        CVIOLET2 = '\33[95m'
        CBEIGE2  = '\33[96m'
        CWHITE2  = '\33[97m'
        CGREYBG  = '\33[100m'
        CREDBG2  = '\33[101m'
        CGREENBG2 = '\33[102m'
        CYELLOWBG2 = '\33[103m'
        CBLUEBG2   = '\33[104m'
        CVIOLETBG2 = '\33[105m'
        CBEIGEBG2  = '\33[106m'
        CWHITEBG2  = '\33[107m'   
        Hidden     = "\033[8m"
        ResetBold       = "\033[21m"
        ResetDim        = "\033[22m"
        ResetUnderlined = "\033[24m"
        ResetBlink      = "\033[25m"
        ResetReverse    = "\033[27m"
        ResetHidden     = "\033[28m"
        Default      = "\033[39m"
        Black        = "\033[30m"
        Red          = "\033[31m"
        Green        = "\033[32m"
        Yellow       = "\033[33m"
        Magenta      = "\033[35m"
        LightGray    = "\033[37m"
        DarkGray     = "\033[90m"
        LightGreen  = "\033[92m"
        LightYellow  = "\033[93m"
        LightBlue    = "\033[94m"
        LightMagenta = "\033[95m"
        LightCyan    = "\033[96m"
        White        = "\033[97m"

        # 'random color : text def color 16 color ' 
        random_ = random.randrange(1,80)
        if random_ == 1 :print(f"\033[39m{ResetAll}{text}")
        elif random_ == 2:print(f"\033[30m{Bold}{text}") 
        elif random_ == 3:print(f"\033[31m{Dim}{text}") 
        elif random_ == 4:print(f"\033[32m{Underlined}{text}") 
        elif random_ == 5:print(f"\033[33m{Blink}{text}") 
        elif random_ == 6:print(f"\033[34m{Reverse}{text}") 
        elif random_ == 7:print(f"\033[35m{ResetAll}{text}") 
        elif random_ == 8:print(f"\033[35m{Bold}{text}") 
        elif random_ == 9:print(f"\033[36m{Dim}{text}") 
        elif random_ == 10:print(f"\033[37m{Underlined}{text}") 
        elif random_ == 11:print(f"\033[90m{Blink}{text}") 
        elif random_ == 12:print(f"\033[91m{Reverse}{text}") 
        elif random_ == 13:print(f"\033[92m{ResetAll}{text}") 
        elif random_ == 14:print(f"\033[93m{Dim}{text}") 
        elif random_ == 15:print(f"\033[94m{Underlined}{text}")  
        elif random_ == 16:print(f"{Cyan}{text}")
        elif random_ == 17:print(f"{Purple}{text}") 
        elif random_ == 18:print(f"{blue}{text}")
        elif random_ == 19:print(f"{Brown}{text}")
        elif random_ == 20:print(f"{Dark_Gray}{text}")
        elif random_ == 21:print(f"{Black}{text}")
        elif random_ == 21:print(f"{Red}{text}")
        elif random_ == 22:print(f"{Green}{text}")
        elif random_ == 23:print(f"{Yellow}{text}")
        elif random_ == 24:print(f"{Magenta}{text}")
        elif random_ == 25:print(f"{LightGray}{text}")
        elif random_ == 26:print(f"{DarkGray}{text}")
        elif random_ == 27:print(f"{LightGreen}{text}")
        elif random_ == 28:print(f"{LightYellow}{text}")
        elif random_ == 29:print(f"{LightBlue}{text}")
        elif random_ == 30:print(f"{LightMagenta}{text}")
        elif random_ == 31:print(f"{White}{text}")
        elif random_ == 32:print(f"{LightCyan}{text}")
        elif random_ == 33:print(f"{Default}{text}")
        elif random_ == 34:print(f"{ResetHidden}{text}")
        elif random_ == 35:print(f"{ResetReverse}{text}")
        elif random_ == 36:print(f"{ResetBlink}{text}")
        elif random_ == 37:print(f"{ResetUnderlined}{text}")
        elif random_ == 38:print(f"{ResetDim}{text}")
        elif random_ == 39:print(f"{ResetBold}{text}")
        elif random_ == 40:print(f"{Hidden}{text}")
        elif random_ == 41:print(f"{CWHITEBG2}{text}")
        elif random_ == 42:print(f"{CBEIGEBG2}{text}")
        elif random_ == 43:print(f"{CVIOLETBG2}{text}")
        elif random_ == 44:print(f"{CBLUEBG2}{text}")
        elif random_ == 45:print(f"{CYELLOWBG2}{text}")
        elif random_ == 46:print(f"{CGREENBG2}{text}")
        elif random_ == 47:print(f"{CREDBG2}{text}")
        elif random_ == 48:print(f"{CGREYBG}{text}")
        elif random_ == 49:print(f"{CWHITE2}{text}")
        elif random_ == 50:print(f"{CBEIGE2}{text}")
        elif random_ == 51:print(f"{CVIOLET2}{text}")
        elif random_ == 52:print(f"{CBLUE2}{text}")
        elif random_ == 53:print(f"{CYELLOW2}{text}")
        elif random_ == 54:print(f"{CGREEN2}{text}")
        elif random_ == 55:print(f"{CRED2}{text}")
        elif random_ == 56:print(f"{CGREY}{text}")
        elif random_ == 57:print(f"{CWHITEBG}{text}")
        elif random_ == 58:print(f"{CBEIGEBG}{text}")
        elif random_ == 59:print(f"{CVIOLETBG}{text}")
        elif random_ == 60:print(f"{CBLUEBG}{text}")
        elif random_ == 61:print(f"{CYELLOWBG}{text}")
        elif random_ == 62:print(f"{CGREENBG}{text}")
        elif random_ == 63:print(f"{CREDBG}{text}")
        elif random_ == 64:print(f"{CBLACKBG}{text}")
        elif random_ == 65:print(f"{CBEIGE}{text}")
        elif random_ == 66:print(f"{CWHITE}{text}")
        elif random_ == 67:print(f"{CVIOLET}{text}")
        elif random_ == 68:print(f"{CBLUE}{text}")
        elif random_ == 69:print(f"{CYELLOW}{text}")
        elif random_ == 70:print(f"{CGREEN}{text}")
        elif random_ == 71:print(f"{CRED}{text}")
        elif random_ == 72:print(f"{CBLACK}{text}")
        elif random_ == 73:print(f"{CSELECTED}{text}")
        elif random_ == 74:print(f"{CBLINK2}{text}")
        elif random_ == 75:print(f"{CBLINK}{text}")
        elif random_ == 76:print(f"{CURL}{text}")
        elif random_ == 77:print(f"{CITALIC}{text}")
        elif random_ == 78:print(f"{CEND}{text}")
        elif random_ == 79:print(f"{CBOLD}{text}")
        
        else:raise ValueError(f'\033[1mError value in text')
        # list color in pyhton ! 
