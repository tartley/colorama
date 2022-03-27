$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

& $bin\python.exe -m pip install --upgrade build
& $bin\python.exe -m build
