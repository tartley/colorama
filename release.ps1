$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

# Upload to PyPI.
& $bin\twine.exe upload dist\colorama-*.tar.gz dist\colorama-*.whl
