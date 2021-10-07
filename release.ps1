$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"
$version="$(& $bin\python.exe setup.py --version)"

# Upload to PyPI.
& $bin\twine.exe upload dist\colorama-$version*.tar.gz dist\colorama-$version-*.whl

