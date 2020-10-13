$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

& $bin\python.exe -m pip install --upgrade setuptools wheel
& $bin\python.exe setup.py sdist bdist_wheel

