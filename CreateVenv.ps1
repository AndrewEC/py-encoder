$EnvFolder = "encoder-venv"

if (Test-Path $EnvFolder) {
    Invoke-Expression "./$EnvFolder/Scripts/Activate.ps1"
} else {
    Write-Host "Creating virtual environment: $EnvFolder"
    python -m venv $EnvFolder `
        && Invoke-Expression "./$EnvFolder/Scripts/Activate.ps1" `
        && pip install -r requirements.txt `

    cd package && python setup.py install && cd ..
}