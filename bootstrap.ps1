$syspython="python3.8.exe"
$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"

echo "Create $syspython virtualenv $ve"
& $syspython -m venv --clear "$ve"
& $bin\python.exe -m pip install --upgrade pip
& $bin\python.exe -m pip install -r requirements.txt -r requirements-dev.txt

