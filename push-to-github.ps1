# Run this script from the repository root
Set-Location -Path "$PSScriptRoot"

$gitHeadPath = Join-Path .git HEAD
if (-not (Test-Path .git) -or -not (Test-Path $gitHeadPath)) {
    git init
    git add .
    git commit -m "Initial project files"
}

git branch -M main

$remoteUrl = 'https://github.com/shraddhau05/-regression-demo.git'
if (-not (git remote | Select-String -SimpleMatch origin)) {
    git remote add origin $remoteUrl
}

git add .
git commit -m "Update regression suite demo and custom agent" -q

git push -u origin main
