"""Validate that release wheels contain runtime files only."""

# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE.txt file.

import sys
from pathlib import Path
from zipfile import ZipFile


def main(wheel_paths):
    if not wheel_paths:
        print("no wheel paths supplied", file=sys.stderr)
        return 1

    for wheel_path in wheel_paths:
        with ZipFile(wheel_path) as wheel:
            bundled_tests = [
                name for name in wheel.namelist() if name.startswith("colorama/tests/")
            ]

        if bundled_tests:
            print(f"{wheel_path} contains bundled tests:", file=sys.stderr)
            print("\n".join(bundled_tests), file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main([Path(path) for path in sys.argv[1:]]))
