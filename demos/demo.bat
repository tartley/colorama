:: Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.

:: Script to demonstrate features of colorama.

:: This demo is also used to verify correctness visually, because we don't
:: have automated tests.

:: Implemented as a bash script which invokes python so that we can test the
:: behaviour on exit, which resets default colors again.

:: print grid of all colors and brightnesses
python demo01.py

:: Simple demo of changing foreground, background and brightness.
python demo02.py

:: Demonstrate the different behavior when autoreset is True and False.
python demo03.py

:: check that stripped ANSI in redirected stderr does not affect stdout
if exist demo04.out del demo04.out
python demo04.py 2> demo04.out
type demo04.out
if exist demo04.out del demo04.out

:: Demonstrate the difference between colorama initialized with wrapping on and off.
python demo05.py

:: Demonstrate printing colored, random characters at random positions on the screen
python demo06.py

:: Demonstrate cursor relative movement: UP, DOWN, FORWARD, and BACK in colorama.CURSOR
python demo07.py

:: Demonstrate the use of a context manager instead of manually using init and deinit
python demo08.py
