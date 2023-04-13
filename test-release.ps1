# Test the currently built release of Colorama from the dist/ dir.
# Run this before making a release.
#
# Uploads package from the dist/ directory to the *test* PyPI.
# Create a fresh virtualenvironment and install colorama from test PyPI.
# Import Colorama and make trivial use of it.

# Exit on error
$ErrorActionPreference = "Stop"

$syspython="python.exe"
$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

# Upload to the test PyPI.
& $bin\twine.exe upload --repository testpypi dist\colorama-*
if(!$?) {
    write-host "  > Expect a 400 if package was already uploaded"
}

# cd elsewhere so we cannot import from local source.
mkdir -force sandbox | out-null
cd sandbox

# Create a temporary disposable virtualenv.
& $syspython -m venv --clear venv

# TODO: What is the windows/powershell equivalent of this:
$version = (Select-String -Path "../colorama/__init__.py" -Pattern "__version__").Line.Split(' ')[2].Replace("'", "")

# Install the package we just uploaded.
# (--extra-index-url for this project's requirements)
venv\Scripts\python -m pip --quiet install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple colorama==$version

# Import and use colorama from the temp virtualenv.
venv\Scripts\python.exe -c @"
import colorama;
colorama.init();
print(colorama.Fore.GREEN + ""OK Colorama "" + colorama.__version__ + "" from test pypi install."")
"@

cd ..
Remove-Item -Recurse -Force sandbox 
