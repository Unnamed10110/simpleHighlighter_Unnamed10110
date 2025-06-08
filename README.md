<blockquote>
<strong>🟢 Hello there:</strong> This used to be a simple python program running in the console, and activated via auto hotkey to run it which made it really slow. Now it is a fully functional background service much faster and easier to set up.
Do not worry about the .exe change, you can see the source code, and even the code that generates the .exe (it's all there).

Any suggestion is much appreciated

</blockquote>

# 🔍 Simple Screen Region Highlighter (Windows Tray Service)

This is a fast, lightweight **screen highlighter overlay** for Windows, inspired by [Flameshot](https://github.com/flameshot-org/flameshot) (Besides many obvious differences, one is that the overlay in the program does not "freeze" the screen when is activated). It runs silently in the background, is triggered via a hotkey, and allows you to draw green transparent rectangles on the screen for visual focus or annotation.

---

## 🕰️ Previous Version (Slower Startup)

The original version was a `.pyw` Python script that required:
- `PowerShell`, `Python`, `PyQt5`, `AutoHotKey`, `Winget`
- Manual startup configuration via `shell:startup`
- It **started slowly**, especially on system boot

---

## 🚀 New Version (Fast `.exe` Tray Service)

> **Now packaged as a `.exe`** with automatic startup at login, tray icon support, and no more dependency juggling!

---

## ✨ Features

- ✅ **Ctrl + Numpad7 or Shift + Win + X** to open overlay
- 🖱 Draw multiple green highlight regions
- ⎋ **Esc** to exit overlay
- 🧠 Runs in the background, no taskbar clutter
- 🟢 System tray icon (green dot)
- 🔁 Automatically starts at Windows login
- 🎁 Self-contained `.exe` builder via `exe_generator.py`

---

## 🚀 Usage (New .exe Method)
1. Build and register the highlighter
```python
python exe_generator.py
```
- Auto-installs dependencies
- Builds highlighter.exe with tray icon
- Registers for startup via Windows registry

2. Use the highlighter
- Press Ctrl + Numpad7 (Shift + Windows + x) to activate the overlay
- Click and drag to create green-highlight rectangles
- Press Ctrl + Z to undo (optional)
- Press Esc to exit overlay
- Stays running in background with a green tray icon

---

## 🟢DEMO
- Exe creation and execution test:


https://github.com/user-attachments/assets/0e359355-a76e-46a5-8cb6-0bb98b777aa1





---

## 📁 Project Files
| File               | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `highlighter.pyw`  | Main screen overlay logic                |
| `exe_generator.py` | Creates `.exe`, tray icon, startup entry |
| `green_dot.ico`    | Auto-generated icon (deleted after use)  |

---

## 🔧 Dependencies
Automatically handled when you run ##exe_generator.py##
- Python 3.7+
- PyQt5
- Pillow
- PyInstaller

---

## 🏁 Autostart
Once generated, the app is registered at:
```powershell
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

You can verify this via regedit or with PowerShell:
```powershell
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Select-Object ScreenHighlighter
```
---

## 📝 Notes
- Everything inside the selected regions remains fully interactive
- Undo support (Ctrl + Z) is partially implemented (optional)
- You can safely delete run_highlighter.ahk if switching fully to .exe

---

## 📋 License
MIT — Free for personal or commercial use. Contributions welcome!

---

## 🙌 Credits

Original idea and interaction model from Flameshot (Linux)

Tray icon, development and packaging by [Unnamed10110](https://github.com/Unnamed10110)





