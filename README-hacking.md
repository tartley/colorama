# Colorama Development

Help and fixes are welcome!

Although Colorama has no requirements other than the Python standard library,
development requires some Python packages, which are captured in
requirements-dev.txt.

Some common commands are captured as Linux makefile targets (which could
perhaps be coaxed into running on OSX in Bash), and as Windows Powershell
scripts.

| Task                            | Linux               | Windows              |
|---------------------------------|---------------------|----------------------|
| Create & populate virtualenv.   | `make bootstrap`    | `.\bootstrap.ps1`    |
| Run tests.                      | `make test`         | `.\test.ps1`         |
| Build a wheel.                  | `make build`        | `.\build.ps1`        |
| Test the wheel.                 | `make test-release` | `.\test-release.ps1` |
| Release the wheel on PyPI       | `make release`      | `.\release.ps1`      |
| Clean generated files & builds. | `make clean`        | `.\clean.ps1`        |

The Makefile is self-documenting, so 'make' with no args will describe each
target.

If you use nose to run the tests, you must pass the ``-s`` flag; otherwise,
``nosetests`` applies its own proxy to ``stdout``, which confuses the unit
tests.

## Release checklist

1. Merge to master.
2. Run the tests.
3. Update the CHANGELOG.
4. Remove the '-pre' suffix from `__version__` in `colorama/__init.py__.py`.
5. * On Windows: `./clean.ps1 && .\bootstrap.ps1 && .\build.ps1 && .\test-release.ps1`
   * On Linux: `make clean bootstrap build test-release`
   * On OSX: View the makefile and manually run the equivalent commands for
     each target. PR to automate this welcome!
6. If all is well:
   * On Windwos: `.\release.ps1`
   * On Linux: `make release`
   This will upload the built package to PyPI, tag the current commit with the
   version, and push the tag.
7. Bump the version number in `colorama/__init__.py`, ready for the next
   release, and add the '-pre' suffix again.

