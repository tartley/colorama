from __future__ import print_function
import fixpath
import colorama

# Demonstrate cursor relative movement: UP, DOWN, FORWARD, and BACK in colorama.CURSOR

up = colorama.Cursor.UP
down = colorama.Cursor.DOWN
forward = colorama.Cursor.FORWARD
back = colorama.Cursor.BACK

def main():
    """
    expected output:
    1a2
    aba
    3a4
    """
    colorama.init()
    print("aaa")
    print("aaa")
    print("aaa")
    print(forward() + up(2) + "b" + up() + back(2) + "1" + forward() + "2" + back(3) + down(2) + "3" + forward() + "4")


if __name__ == '__main__':
    main()
