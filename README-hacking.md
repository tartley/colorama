# Colorama Development

Help and fixes are welcome!

Although Colorama has no requirements other than the Python standard library,
development requires some Python packages, which are captured in
requirements-dev.txt.

Throughout, if you're on a Mac, you can probably do something similar to the
Linux instructions. Either use the makefile directly, or look in it to see
what commands it executes, and manually execute something similar. PRs to
automate for Mac appreciated! Especially if they just made the existing Linux
Makefile targets work on Mac too.

## Desired changes

Colorama is unexpectedly popular, and is now a transitive dependency of many
popular and high profile projects. If we break backwards compatibility, even in a
subtle way, we can break applications - or pip installs - for lots of people.

In addition, the project already takes more time & energy to maintain than
the maintainers currently have available - for example the original author
is now a parent, and no longer uses Windows, so time and motivation for this
project are both much lower than they used to be.

As a result of both the above, we are very conservative in what sorts of
changes we can accept. Generally, we are not keen on new features. Even if
they are small, they still add to the future maintenance burden, increasing
the surface area into which future bugs or compatibility breaks could be
introduced.

This is especially true if they are new ways to generate ANSI codes (e.g.
context managers for handling Fore, Back or Style changes.), since it has
always been Colorama's stance that if you want to print ANSI codes, then yes
we can help out with that in a rudimentary way, but if you want to do advanced
things, then you should be using a different library that specializes in that,
such as Termcolor, Blessings, or Rich. These libraries are much better than
Colorama at generating ANSI codes for colors and the like, and probably
already include the feature you are trying to add to Colorama, plus many
more.

In addition to using those libraries, if you call colorama.init(), then your
fancy new colors, etc, will also work on Windows. This is the main purpose
of Colorama.

The kinds of submissions we would encourage work towards that goal, or fix
bugs, or improve compatibility across operating systems or environements.

## Makefile and PowerShell scripts

Some common commands are captured as Linux makefile targets (which could
perhaps be coaxed into running on OSX in Bash), and as Windows PowerShell
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

## Release checklist

TODO: Add the use of release candidate versions to this checklist.

1. Check the CHANGELOG is updated with everything since the last release.
2. Remove the '-pre' suffix from `__version__` in `colorama/__init.py__.py`.
3. Run the tests locally on your preferred OS, just to save you from doing
   the following time-consuming steps while there are still obvious problems
   in the code:

   * Windows: `./test.ps1`
   * Linux: `make test`

4. Verify you're all committed, merged to master, and pushed to origin (This
   triggers a CI build, which we'll check later on)

5. Build the distributables (sdist and wheel), on either OS:

    * Windows: `.\build.ps1`
    * Linux: `make build`

6. Test the distributables on both OS. Whichever one you do 2nd will get an
   HTTP 400 response on uploading to test.pypi.org, but outputs a message
   saying this is expected and carries on:

   * Windows: `./clean.ps1 && .\bootstrap.ps1 && .\build.ps1 &&
     .\test-release.ps1`
   * Linux: `make clean bootstrap build test-release`

    (This currently only tests the wheel, but
    [should soon test the sdist too](https://github.com/tartley/colorama/issues/286).)

7. Check the [CI builds](https://github.com/tartley/colorama/actions/)
   are complete and all passing.

8. Upload the distributables to PyPI:

   * On Windows: `.\release.ps1`
   * On Linux: `make release`

   This [should soon tag the release for you](https://github.com/tartley/colorama/issues/282). Until then:

9. Tag the current commit with the `__version__` from `colorama/__init__.py`.
   We should start using
   [annotated tags for releases](https://www.tartley.com/posts/til-git-annotated-tags/), so:

       git tag -a -m "" $version
       git push --follow-tags

10. Bump the version number in `colorama/__init__.py`, and add the '-pre'
    suffix again, ready for the next release. Commit and push this (directly to
    master is fine.)
