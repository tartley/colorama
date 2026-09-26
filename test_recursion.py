import sys
import colorama

# Simulate a tool calling init() more than once without deinit()
colorama.init()
colorama.init()
colorama.init()

# Build a string with many ANSI codes to trigger deep recursion if the bug exists
big_text = ("\x1b[31mred\x1b[0m " * 5000)

print("Testing large ANSI-heavy write after multiple init() calls...")
sys.stdout.write(big_text)
print("\nSUCCESS: no RecursionError!")