
winget install --id Microsoft.Powershell --source winget --accept-package-agreements --accept-source-agreements

$ahkUrl = "https://www.autohotkey.com/download/ahk-install.exe"
$installer = "$env:TEMP\ahk-install.exe"

Invoke-WebRequest -Uri $ahkUrl -OutFile $installer
Start-Process -FilePath $installer -ArgumentList "/silent" -Wait
Remove-Item $installer

Write-Host "AutoHotkey v2 installation completed."