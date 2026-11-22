$syspython="python.exe"
$ve="$HOME\.virtualenvs\colorama"
$bin="$ve\Scripts"
$version = & $syspython -c "import colorama; print(colorama.__version__)"
if ($LASTEXITCODE -ne 0) { throw "Could not determine the release version" }

# Upload to the test PyPI.
& $bin\twine.exe upload --repository testpypi dist\colorama-*
if (!$?) {
    Write-Host "  > Expect a 400 if package was already uploaded"
}

# Import from outside the checkout, in a fresh environment for each format.
New-Item -ItemType Directory -Force sandbox | Out-Null
Push-Location sandbox
try {
    foreach ($artifact in @("wheel", "sdist")) {
        & $syspython -m venv --clear "venv-$artifact"
        if ($LASTEXITCODE -ne 0) { throw "Could not create $artifact environment" }
        $python = ".\venv-$artifact\Scripts\python.exe"
        $format = if ($artifact -eq "wheel") { "--only-binary=colorama" } else { "--no-binary=colorama" }
        & $python -m pip --quiet install --no-cache-dir $format --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple "colorama==$version"
        if ($LASTEXITCODE -ne 0) { throw "Could not install the $artifact release" }
        & $python -c "import colorama; assert colorama.__version__ == '$version'; colorama.init(); print(colorama.Fore.GREEN + 'OK: Colorama', colorama.__version__, 'from $artifact test pypi install:', colorama.__file__)"
        if ($LASTEXITCODE -ne 0) { throw "The $artifact release smoke test failed" }
    }
} finally {
    Pop-Location
}
