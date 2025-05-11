Write-Host "============================="
Write-Host "🔧 Installing PowerShell Core..."
Write-Host "============================="
winget install --id Microsoft.Powershell --source winget --accept-package-agreements --accept-source-agreements

Write-Host "`n============================="
Write-Host "🐍 Installing Python..."
Write-Host "============================="

$installDir = "C:\Python"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.14.0/python-3.14.0b1.exe"
$installerPath = "$env:TEMP\python-installer.exe"
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 TargetDir=$installDir PrependPath=1" -Wait
Remove-Item $installerPath
& "$installDir\python.exe" --version


$v = Split-Path (Get-Command python).Source
Write-Host "✅ Python installed in: $v"

Write-Host "`n============================="
Write-Host "⚙️ Installing AutoHotkey v2..."
Write-Host "============================="
$ahkUrl = "https://www.autohotkey.com/download/ahk-install.exe"
winget install AutoHotkey.AutoHotkey
Write-Host "✅ AutoHotkey v2 installation completed."

Write-Host "`n============================="
Write-Host "📂 Selecting folder to save highlighter.py..."
Write-Host "============================="
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = "Select a folder to save highlighter.py"
$dialog.ShowNewFolderButton = $true
$aux = ""

if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $folder = $dialog.SelectedPath
    $url = "https://raw.githubusercontent.com/Unnamed10110/simpleHighlighter_Unnamed10110/master/highlighter.py"
    $filePath = Join-Path $folder "highlighter.py"
    Invoke-WebRequest -Uri $url -OutFile $filePath
    $scriptPath = $filePath
    $aux = Split-Path $scriptPath -Parent
    Write-Host "✅ Downloaded to: $scriptPath"
} else {
    Write-Host "❌ Operation cancelled by user."
    exit
}

Write-Host "`n============================="
Write-Host "📝 Creating run_highlighter.ahk..."
Write-Host "============================="
$ahkFile = Join-Path $aux "run_highlighter.ahk"
$ahkContent = @"
^Numpad7::
{
    pythonPath := "$v\\pythonw.exe"
    scriptPath := "$scriptPath"
    Run pythonPath ' "' scriptPath '"'
}
"@
Set-Content -Path $ahkFile -Value $ahkContent -Encoding UTF8
Write-Host "✅ AHK script created at: $ahkFile"

Write-Host "`n============================="
Write-Host "🔗 Associating .ahk files with AutoHotkey v2..."
Write-Host "============================="
$ahk2Path = "C:\Users\$env:USERNAME\AppData\Local\Programs\AutoHotkey\v2\AutoHotkey64.exe"
cmd.exe /c "assoc .ahk=AutoHotkeyScript"
cmd.exe /c "ftype AutoHotkeyScript=""$ahk2Path"" ""%1"""
Write-Host "✅ .ahk association complete."

Write-Host "`n============================="
Write-Host "🚀 Launching highlighter..."
Write-Host "============================="
Write-Host "RUN: $aux\run_highlighter.ahk"
& $ahk2Path "$aux\run_highlighter.ahk"
