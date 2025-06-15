# 🔍 UnnamedHighlighter (Windows Tray Service)

A fast, lightweight **screen highlighter overlay for Windows**, inspired by [Flameshot](https://github.com/flameshot-org/flameshot)—but with a key difference: the overlay **doesn’t freeze the screen**. It runs quietly in the background and lets you draw green transparent rectangles to highlight or annotate your screen.

> 🟢 Originally a simple Python script launched via AutoHotKey, this tool is now a **fully standalone tray application (.exe)** with faster startup, auto-launch on login, and hotkey activation.

All source code is available, including the script used to generate the `.exe`.  
**Suggestions and contributions are very welcome!**

---

## 🆕 Key Updates

- 🐞 **Bugs fixed**  
- 🟢 **Improved launch time and usability**  
- 🟢 **One-handed hotkey added**: `Shift + Alt + X`  
- 🟢 **Overlay DPI awareness**: no more blurry scaling on HiDPI screens  
- 🟢 **Overlay priority fixed** (always on top)

### Why two processes?
When built with PyInstaller as a single `.exe` file:
```text
- Process 1: Launcher (bootstrap stub)
  • Extracts the app into a temporary folder (e.g., _MEIxxxxxx)
  • Launches Process 2

- Process 2: Actual app
  • Runs the GUI (PyQt5), overlay logic, hotkey handler

- Process 1 stays alive to manage cleanup on exit.
```

---

## ⚡ Hotkey Modes

| Hotkey           | Behavior                                                                 |
|------------------|--------------------------------------------------------------------------|
| `Shift + Alt + X` | Primary hotkey (one-handed). Unfocuses current app first to avoid conflicts. |
| `Ctrl + Numpad 7` | Secondary hotkey. Activates overlay without changing window focus.         |

If a hotkey stops working (usually after system sleep or long uptime), **click the tray icon once** to refresh it. No need to restart the app.

---

## ✨ Features

- 🔹 Activate overlay with hotkey
- 🟩 Draw transparent green rectangles on screen
- ⎋ Press `Esc` to exit overlay
- ↩️ Press `Ctrl + Z` to undo last rectangle
- 🧠 Always running silently in background
- 🟢 Green system tray icon
- 🚀 Auto-starts with Windows
- 📦 Self-contained `.exe` generated via `exe_generator.py`

---

## ⏱️ Old Version (Python + AHK)

The original setup:
- `.pyw` file + AutoHotKey
- Manual startup config (`shell:startup`)
- Required Python, PyQt5, Winget, etc.
- **Slow startup**, especially after boot

---

## 🚀 New Version (`.exe` with Tray Support)

- One-click build via `exe_generator.py`
- No more external dependencies
- Adds registry key for auto-start
- Instantly responsive tray-based background service

---

## 🧪 Usage

1. **Build and install the `.exe`**
   ```bash
   python exe_generator.py
   ```

2. **Use the highlighter**
   - Press hotkey → draw on screen
   - `Esc` → exit overlay
   - `Ctrl + Z` → undo (optional)
   - Tray icon keeps it running
   - Click tray icon once to refresh hotkeys if needed

---

## ⚡ Quick Install (PowerShell)

> 📌 Tip: Run this from your home folder (e.g. `C:\Users\YourName`) or root (`C:\`).

```powershell
iex "& { iwr https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/raw/master/highlighter.exe -OutFile Downloads\highlighter.exe; Start-Process Downloads\highlighter.exe }"
```

---

## 📹 Demo

**Watch `.exe` build and usage demo:**

[🔗 Video Link](https://github.com/user-attachments/assets/0e359355-a76e-46a5-8cb6-0bb98b777aa1)

---

## 📦 Release

> 🏁 **[v2.2.0 Released!](https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/releases/tag/v2.2.0)** — Fast, stable, and streamlined!

---

## 🗂️ Project Structure

| File               | Description                                      |
|--------------------|--------------------------------------------------|
| `highlighter.pyw`  | Main logic for overlay and drawing               |
| `exe_generator.py` | Builds `.exe`, sets up startup and tray icon     |
| `green_dot.ico`    | Icon for tray (generated automatically)          |

---

## 🔧 Dependencies

Handled automatically via `exe_generator.py`

| Dependency      | Purpose                                                  |
|-----------------|----------------------------------------------------------|
| `Python 3.7+`   | Minimum required version                                 |
| `PyQt5`         | GUI: system tray, full-screen overlay, drawing, etc.     |
| `keyboard`      | Global hotkeys                                           |
| `Pillow`        | Generates the tray icon                                  |
| `PyInstaller`   | Creates the standalone `.exe`                            |
| `SetProcessDpiAwareness` / `SetProcessDPIAware` | DPI scaling fix for HiDPI displays |
| `SetWindowPos`  | Forces overlay to stay on top                            |

---

## 🏁 Auto Start (Registry)

After installation, the app is auto-started via:

```reg
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

Check it with PowerShell:

```powershell
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" | Select-Object ScreenHighlighter
```

---

## 📝 Notes

- Selected areas remain **interactive** (click-through)
- `Ctrl + Z` undo is **optional**
- You can remove `run_highlighter.ahk` if using `.exe` only

---

## 📄 License

MIT License — Free for personal and commercial use.  
Pull requests welcome!

---

## 🙌 Credits

- Inspired by: [Flameshot](https://github.com/flameshot-org/flameshot) (Linux)  
- Developed, packaged & tray integration by [Unnamed10110](https://github.com/Unnamed10110)
