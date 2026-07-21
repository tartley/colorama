$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

& $bin\python.exe -m pip install --upgrade build
& $bin\python.exe -m build
& $bin\python.exe tools\check_wheel_contents.py (Get-ChildItem dist\*.whl | ForEach-Object FullName)
