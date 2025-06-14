<br>

# 🔍 Simple Screen Region Highlighter (Windows Tray Service)

This is a fast, lightweight **screen highlighter overlay** for Windows, inspired by [Flameshot](https://github.com/flameshot-org/flameshot) (Besides many obvious differences, one is that the overlay in the program does not "freeze" the screen when is activated). It runs silently in the background, is triggered via a hotkey, and allows you to draw green transparent rectangles on the screen for visual focus or annotation.

<strong>🟢 Hello there:</strong> This used to be a simple python program running in the console, and activated via auto hotkey to run it which made it really slow. Now it is a fully functional background service much faster and easier to set up.
Do not worry about the .exe change, you can see the source code, and even the code that generates the .exe (it's all there).

Any suggestion is much appreciated
<br>

---
- 🛠️ **Bugs Fixed!**  
- <strong>🟢The `.exe` now doesn't duplicates</strong> the process when it runs.
 
- <strong>🟢Added a one-handed shortcut</strong> Shift+Win+X.
 
- <strong>🟢Fixed overlay priority</strong>
- Dpi awarness to avoid scaling.



---

<br>

## 🕰️ Previous Version (Slower Startup)

The original version was a `.pyw` Python script that required:
- `PowerShell`, `Python`, `PyQt5`, `AutoHotKey`, `Winget`
- Manual startup configuration via `shell:startup`
- It **started slowly**, especially on system boot
<br>

---

## 🚀 New Version (Fast `.exe` Tray Service)

> **Now packaged as a `.exe`** with automatic startup at login, tray icon support, and no more dependency juggling!
<br>

---

## ✨ Features

- ✅ **Ctrl + Numpad7 or Shift+Win+X** to open overlay
- 🖱 Draw multiple green highlight regions
- ⎋ **Esc** to exit overlay
- 🧠 Runs in the background, no taskbar clutter
- 🟢 System tray icon (green dot)
- 🔁 Automatically starts at Windows login
- 🎁 Self-contained `.exe` builder via `exe_generator.py`
<br>

---

## 🚀 Usage (New .exe Method)
1. Build and register the highlighter
```python
python exe_generator.py
```
<br>

- Auto-installs dependencies
- Builds highlighter.exe with tray icon
- Registers for startup via Windows registry
<br>

2. Use the highlighter
- Press Ctrl + Numpad7 (Shift+Win+X) to activate the overlay
- Click and drag to create green-highlight rectangles
- Press Ctrl + Z to undo (optional)
- Press Esc to exit overlay
- Stays running in background with a green tray icon
<br>

---
<br>

## QUICK INSTALLATION:
** Observation: to use this method in powershell, you should be in your user directory (i.e. C:\Users\MyUser) or in the root folder (i.e. C:\), and then run the command.
```PWSH
iex "& { iwr https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/raw/master/highlighter.exe -OutFile Downloads\highlighter.exe; Start-Process Downloads\highlighter.exe }"
```
<br>

## 🟢DEMO
- Exe creation and execution test:


https://github.com/user-attachments/assets/0e359355-a76e-46a5-8cb6-0bb98b777aa1


---

## Release
> 📦 **[v2.2.0 Released!](https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/releases/tag/v2.2.0)** — 🐛 Bugs fixed!

---
<br>

## 📁 Project Files
| File               | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `highlighter.pyw`  | Main screen overlay logic                |
| `exe_generator.py` | Creates `.exe`, tray icon, startup entry |
| `green_dot.ico`    | Auto-generated icon (deleted after use)  |

---
<br>

## 🔧 Dependencies
Automatically handled when you run ##exe_generator.py##
- Python 3.7+
- PyQt5
- Pillow
- PyInstaller

---
<br>

## 🏁 Autostart
Once generated, the app is registered at:
```powershell
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```
<br>

You can verify this via regedit or with PowerShell:
```powershell
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Select-Object ScreenHighlighter
```
---
<br>

## 📝 Notes
- Everything inside the selected regions remains fully interactive
- Undo support (Ctrl + Z) is partially implemented (optional)
- You can safely delete run_highlighter.ahk if switching fully to .exe

---
<br>

## 📋 License
MIT — Free for personal or commercial use. Contributions welcome!

---

<br>

## 🙌 Credits

Original idea and interaction model from Flameshot (Linux)

Tray icon, development and packaging by [Unnamed10110](https://github.com/Unnamed10110)





