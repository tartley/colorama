$syspython="python3.8.exe"
$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"
$version="$(& $bin\python.exe setup.py --version)"

# Upload to the test PyPI.
& $bin\twine.exe upload --repository testpypi dist\colorama-$version-*
if(!$?) {
    write-host "  > Expect a 400 if package was already uploaded"
}

# cd elsewhere so we cannot import from local source.
mkdir -force sandbox | out-null
cd sandbox

# Create a temporary disposable virtualenv.
& $syspython -m venv --clear venv

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

