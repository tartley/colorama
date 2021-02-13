$syspython="python3.8.exe"
$ve="$HOME\.virtualenvs\colorama"

remove-item -r -fo * -I build,dist,MANIFEST,colorama.egg-info,$ve,sandbox
& $syspython -Bc "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

