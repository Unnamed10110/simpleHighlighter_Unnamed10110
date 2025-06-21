
# 🔍 UnnamedHighlighter (Windows Tray Service)

A fast, lightweight **screen highlighter overlay for Windows**, inspired by [Flameshot](https://github.com/flameshot-org/flameshot)—with a key difference: **it doesn't freeze your screen** when activated.

Runs silently in the background as a system tray app, allowing you to draw green translucent rectangles on your screen using global hotkeys.

> 🟢 Originally a simple Python script + AutoHotKey. Now a **standalone tray `.exe`**, with auto-start, no dependencies at runtime, and self-healing behavior during development.

---

## 🆕 What's New in This Version?

### ✅ Code & App Enhancements

- 📌 **Tray-based background service** with PyQt5
- ⚡ **One-handed hotkey**: `Shift + Alt + X`  
- 🧊 **Overlay is topmost** but click-through-safe  
- 🔁 **Hotkey recovery** via tray icon click  
- 🖼️ **DPI-aware overlay** (fixes blurry HiDPI rendering)  
- 🐛 **Dependency auto-install** if not frozen (`.py` dev mode)  
- 🧠 **Self-registers in Registry** on first run as `.exe`

---

### 🔃 Dependency Changes

| Dependency         | Status    | Purpose                                                              |
|--------------------|-----------|----------------------------------------------------------------------|
| `keyboard`         | ❌ Removed | Was used in early AHK phase; now replaced by native Windows hotkeys (NOW IT DOENS'T MESS UP THE KEYBOARD LAYOUT) |
| `pywin32`          | ✅ Added   | Handles hotkey registration and tray messaging with `win32gui`      |
| `PyQt5`            | ✅ Kept    | Overlay drawing and tray GUI                                        |
| `Pillow`           | ✅ Optional | Only used in older icon generation (now done with `QPixmap`)       |
| `ctypes` + `winreg`| ✅ Built-in | For DPI awareness and auto-start setup                              |
| `PyInstaller`      | ✅ Build-time | For packaging `.exe`                                               |

> 🛠️ Now uses **native Windows hotkeys via `RegisterHotKey`** instead of the cross-platform `keyboard` package.

---

## ⚡ Global Hotkeys

| Hotkey             | Action                                                                 |
|--------------------|------------------------------------------------------------------------|
| `Shift + Alt + X`  | Main shortcut. Temporarily unfocuses window, then opens overlay.       |
| `Ctrl + Numpad 7`  | Secondary shortcut. Opens overlay without touching active window.      |

> 💡 If hotkeys stop working (e.g. after sleep), **click the tray icon once** to recover them.

---

## 🖼️ Features Summary

- ✅ Draw translucent green rectangles anywhere on screen
- 🔒 Overlay stays topmost but won’t hijack input
- 🧠 Tray icon keeps the app running quietly
- 🟢 Click tray icon to restore hotkeys instantly
- ↩️ `Ctrl + Z` to undo last rectangle
- ⎋ `Esc` to close overlay
- 🚀 Auto-starts at boot via registry key
- 📦 Fully self-contained `.exe` (no Python needed to run)

---

## 🔄 Why Two Processes?

When built via PyInstaller:

```text
Process 1: Bootstrapper
  • Extracts app to a temp folder (_MEIxxxxxx)
  • Launches actual GUI process

Process 2: Main App
  • Handles tray icon, overlay GUI, hotkeys

Process 1 remains in background to manage cleanup on exit.
```

---

## ⚙️ Build & Run

### Build `.exe`

```bash
python exe_generator.py
```

> 🪛 Requires Python 3.7+, PyInstaller, and dependencies listed above.

---

### Usage

- Press a hotkey → draw transparent rectangles
- `Ctrl + Z` to undo last shape
- `Esc` to exit overlay
- Tray icon keeps it running
- Click tray icon to **refresh hotkeys**

---

## 🧪 Quick Install via PowerShell

Download and run instantly:

```powershell
iex "& { iwr https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/raw/master/highlighter.exe -OutFile Downloads\highlighter.exe; Start-Process Downloads\highlighter.exe }"
```

> 📝 Tip: Run from a short path like `C:\` or your user folder to avoid long temp paths on first launch.

---

## 🗂️ Project Structure

| File               | Description                                      |
|--------------------|--------------------------------------------------|
| `highlighter.pyw`  | Main logic for overlay and drawing               |
| `exe_generator.py` | Compiles `.exe`, sets registry, adds tray        |
| `green_dot.ico`    | Tray icon (auto-generated if missing)            |

---

## 🏁 Auto Start Behavior

After first run as `.exe`, this registry key is created:

```reg
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\ScreenHighlighter
```

Check or remove it using PowerShell:

```powershell
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Select-Object ScreenHighlighter
```

---

## 📹 Demo

Watch a quick overview of building and using the `.exe`:  

[🔗 Video Link](https://github.com/user-attachments/assets/0e359355-a76e-46a5-8cb6-0bb98b777aa1)

---

## 📝 Notes

- 🧊 Overlays are **non-blocking**, you can click through
- 🔁 Hotkeys automatically recover on tray click
- 📦 `.exe` contains all needed Python files inside
- 🛑 You can safely delete `run_highlighter.ahk` (legacy)

---

## 📄 License

**MIT License** — Free for personal and commercial use.  
Pull requests and feedback welcome!

---

## 🙌 Credits

- 🔥 Inspired by: [Flameshot](https://github.com/flameshot-org/flameshot)
- 🧑‍💻 Developed by: [Unnamed10110](https://github.com/Unnamed10110)
