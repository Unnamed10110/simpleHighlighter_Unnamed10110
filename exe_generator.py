import os
import sys
import subprocess
import shutil
import winreg

# --- Auto-install dependencies ---
def install_missing_packages():
    import pkg_resources
    required = {"pillow", "pyinstaller"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print(f"📦 Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

install_missing_packages()

# --- Icon generation ---
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, "green_dot.ico")

def create_icon(path=ICON_PATH, size=64):
    """Create a green dot icon."""
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    radius = size // 2 - 4
    left_up = ((size - 2 * radius) // 2, (size - 2 * radius) // 2)
    right_down = (left_up[0] + 2 * radius, left_up[1] + 2 * radius)
    draw.ellipse([left_up, right_down], fill=(0, 255, 0, 255))
    image.save(path, format='ICO')
    print(f"✅ Icon saved as {path}")

def build_exe(script='highlighter.pyw', icon=ICON_PATH, exe_name='highlighter.exe'):
    script_path = os.path.join(SCRIPT_DIR, script)
    output_exe_path = os.path.join(SCRIPT_DIR, exe_name)

    if not os.path.exists(script_path):
        print(f"❌ Script {script} not found!")
        return

    print("🏗️ Building executable using PyInstaller...")

    args = [
        "pyinstaller",
        "--noconfirm",
        "--windowed",
        "--onefile",  # <-- FORCE single .exe output
        f"--icon={icon}",
        f"--distpath={SCRIPT_DIR}",  # Output .exe right here
        f"--workpath={os.path.join(SCRIPT_DIR, 'build')}",
        f"--specpath={SCRIPT_DIR}",
        script_path,
    ]

    subprocess.run(args, check=True)

    built_exe = os.path.join(SCRIPT_DIR, os.path.splitext(script)[0] + ".exe")
    if os.path.exists(built_exe) and built_exe != output_exe_path:
        shutil.move(built_exe, output_exe_path)
        print(f"✅ Moved to: {output_exe_path}")
    elif os.path.exists(output_exe_path):
        print(f"✅ Executable ready: {output_exe_path}")
    else:
        print("❌ Build succeeded but .exe not found.")

def add_to_startup(app_name="ScreenHighlighter", exe_path=None):
    if exe_path is None:
        exe_path = os.path.join(SCRIPT_DIR, "highlighter.exe")

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg:
            winreg.SetValueEx(reg, app_name, 0, winreg.REG_SZ, exe_path)
        print(f"✅ Added to Windows startup: {exe_path}")
    except Exception as e:
        print(f"❌ Failed to set startup entry: {e}")

def clean_everything_except(exe_name="highlighter.exe"):
    for item in os.listdir(SCRIPT_DIR):
        path = os.path.join(SCRIPT_DIR, item)
        if item == exe_name:
            continue
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif item.endswith((".spec", ".ico", ".log", ".pyc")) or item.startswith("highlighter") and item.endswith(".exe") and item != exe_name:
            os.remove(path)

    print("🧹 Cleaned up all build files, kept only:", exe_name)

if __name__ == "__main__":
    try:
        create_icon()
        build_exe()
        add_to_startup()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during build: {e}")
    finally:
        clean_everything_except("highlighter.exe")
