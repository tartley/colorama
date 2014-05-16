import colorama

up = lambda count: "\x1b[%sA" % str(count)
down = lambda count: "\x1b[%sB" % str(count)
forward = lambda count: "\x1b[%sC" % str(count)
back = lambda count: "\x1b[%sD" % str(count)

def main():
    """
    expected output:
    1a2
    aba
    3a4
    """
    colorama.init()
    print "aaa"
    print "aaa"
    print "aaa"
    print forward(1) + up(2) + "b" + up(1) + back(2) + "1" + forward(1) + "2" + back(3) + down(2) + "3" + forward(1) + "4"


if __name__ == '__main__':
    main()