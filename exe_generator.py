import os
import sys
import subprocess

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

# --- Import dependencies now that they're installed ---
from PIL import Image, ImageDraw
import shutil
import winreg

ICON_PATH = "green_dot.ico"

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
    if not os.path.exists(script):
        print(f"❌ Script {script} not found in current folder!")
        return

    print("🏗️ Building executable using PyInstaller...")
    subprocess.run([
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--icon={icon}",
        script
    ], check=True)

    # Move the compiled .exe to current directory
    src = os.path.join("dist", os.path.splitext(script)[0] + ".exe")
    dst = os.path.abspath(exe_name)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"✅ Moved {exe_name} to current directory.")
    else:
        print("❌ Build succeeded but .exe not found.")

def add_to_startup(app_name="ScreenHighlighter", exe_path=None):
    if exe_path is None:
        exe_path = os.path.abspath("highlighter.exe")

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg:
            winreg.SetValueEx(reg, app_name, 0, winreg.REG_SZ, exe_path)
        print(f"✅ Added to Windows startup: {exe_path}")
    except Exception as e:
        print(f"❌ Failed to set startup entry: {e}")

def clean_build_artifacts():
    for folder in ["build", "__pycache__", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for file in os.listdir():
        if file.endswith(".spec"):
            os.remove(file)
    if os.path.exists(ICON_PATH):
        os.remove(ICON_PATH)
        print(f"🧹 Removed temporary icon file: {ICON_PATH}")

if __name__ == "__main__":
    try:
        create_icon()
        build_exe()
        add_to_startup()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during process: {e}")
    finally:
        clean_build_artifacts()
