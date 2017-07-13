from __future__ import print_function
import fixpath
import colorama
import sys
import time

# Demonstrate cursor saving, restoring and positioning: SAVE, RESTORE and POS in colorama.Cursor

save = colorama.Cursor.SAVE
restore = colorama.Cursor.RESTORE
pos = colorama.Cursor.POS

blue = colorama.Back.BLUE
reset = colorama.Back.RESET

def main():
    """
    expected output:
    Current state is shown at top
    Progress is shown at the current cursor position
    """
    colorama.init()
    for i in range(1, 10):
        sys.stdout.write("Step {}: ".format(i))
        for j in range(1, 10):
            sys.stdout.write(str(j))
            sys.stdout.write(save() + pos(10, 1) + blue + "  State {}.{}  ".format(i, j) + restore() + reset)
            sys.stdout.flush()
            time.sleep(0.02)
        print()


if __name__ == '__main__':
    main()
