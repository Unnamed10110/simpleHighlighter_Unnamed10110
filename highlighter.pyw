import sys
import threading
import os
import ctypes
import time
import winreg
import traceback

# DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Register at startup if running as compiled EXE
def register_startup(app_name="ScreenHighlighter"):
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        except Exception as e:
            print(f"[Startup Registration] Failed: {e}")

# Auto-install dependencies if missing
try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QSystemTrayIcon, QMenu, QAction
    )
    from PyQt5.QtGui import QPainter, QPen, QColor, QIcon, QPixmap
    from PyQt5.QtCore import Qt, QRect, pyqtSignal, QObject
    import win32con
    import win32gui
    import win32api
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "pywin32"])
    if not getattr(sys, 'frozen', False):
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        sys.exit(1)

def click_taskbar():
    # Sends Windows + T to focus taskbar (same as your original keyboard.send)
    # Using win32api to simulate keys:
    win32api.keybd_event(win32con.VK_LWIN, 0, 0, 0)
    win32api.keybd_event(ord('T'), 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(ord('T'), 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_LWIN, 0, win32con.KEYEVENTF_KEYUP, 0)

def generate_green_dot_icon(size=64):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(0, 255, 0))
    painter.setPen(Qt.NoPen)
    radius = size // 2 - 4
    painter.drawEllipse((size - 2 * radius) // 2, (size - 2 * radius) // 2, 2 * radius, 2 * radius)
    painter.end()
    return QIcon(pixmap)

class TriggerSignals(QObject):
    show_overlay = pyqtSignal()
    hide_overlay = pyqtSignal()

class FlameshotOverlay(QWidget):
    def __init__(self, trigger_signals):
        super().__init__()
        self.trigger = trigger_signals
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        self.start_point = None
        self.end_point = None
        self.rectangles = []

        self.trigger.show_overlay.connect(self.activate_overlay)
        self.trigger.hide_overlay.connect(self.close)

    def make_window_topmost(self):
        hwnd = self.winId().__int__()
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_SHOWWINDOW = 0x0040
        ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                          SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

    def activate_overlay(self):
        self.rectangles.clear()
        self.start_point = None
        self.end_point = None
        self.show()
        self.make_window_topmost()
        self.installEventFilter(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        for rect in self.rectangles:
            painter.fillRect(rect, Qt.transparent)

        if self.start_point and self.end_point:
            live_rect = QRect(self.start_point, self.end_point).normalized()
            painter.fillRect(live_rect, Qt.transparent)

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for rect in self.rectangles:
            painter.drawRect(rect)

        if self.start_point and self.end_point:
            painter.drawRect(live_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = QRect(self.start_point, self.end_point).normalized()
            self.rectangles.append(rect)
            self.start_point = None
            self.end_point = None
            self.update()

    def undo_last_rectangle(self):
        if self.rectangles:
            self.rectangles.pop()
            self.update()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.trigger.hide_overlay.emit()
                return True
            elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
                self.undo_last_rectangle()
                return True
        return super().eventFilter(obj, event)

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.signals = TriggerSignals()
        self.overlay = FlameshotOverlay(self.signals)

        self.tray = QSystemTrayIcon()
        icon = generate_green_dot_icon()
        self.tray.setIcon(icon)
        self.tray.setToolTip("Screen Highlighter")

        menu = QMenu()
        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.handle_tray_click)
        self.tray.show()

        self.hotkeys_registered = False
        self.running = True
        self.listener_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.listener_thread.start()

        sys.exit(self.app.exec_())

    def handle_tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            # Recover hotkeys on tray icon click (optional)
            self.recover_hotkeys()

    def recover_hotkeys(self):
        self.unregister_hotkeys()
        self.register_hotkeys()

    def activate_overlay_without_click(self):
        self.signals.show_overlay.emit()

    def delayed_taskbar_click_then_overlay(self):
        time.sleep(0.1)
        click_taskbar()
        time.sleep(0.05)
        self.signals.show_overlay.emit()

    def register_hotkeys(self):
        if self.hotkeys_registered:
            return
        # Modifiers for RegisterHotKey
        MOD_CONTROL = 0x0002
        MOD_SHIFT = 0x0004
        MOD_ALT = 0x0001
        VK_NUMPAD7 = 0x67
        VK_X = 0x58

        # Create a message-only window to receive hotkey messages
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = "HotkeyListenerWindow"
        wc.lpfnWndProc = self.wnd_proc
        self.classAtom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindowEx(
            0, self.classAtom, "HotkeyListenerWindow", 0,
            0, 0, 0, 0,
            0, 0, 0, None)

        # Register hotkeys
        if not win32gui.RegisterHotKey(self.hwnd, 1, MOD_CONTROL, VK_NUMPAD7):
            print("[Hotkey Register Error] Ctrl+Numpad7")
        else:
            print("Registered Ctrl+Numpad7")

        if not win32gui.RegisterHotKey(self.hwnd, 2, MOD_SHIFT | MOD_ALT, VK_X):
            print("[Hotkey Register Error] Shift+Alt+X")
        else:
            print("Registered Shift+Alt+X")

        self.hotkeys_registered = True

    def unregister_hotkeys(self):
        if not self.hotkeys_registered:
            return
        try:
            win32gui.UnregisterHotKey(self.hwnd, 1)
            win32gui.UnregisterHotKey(self.hwnd, 2)
            win32gui.DestroyWindow(self.hwnd)
            win32gui.UnregisterClass(self.classAtom, None)
            self.hotkeys_registered = False
            print("Unregistered hotkeys")
        except Exception as e:
            print(f"Error during unregistering hotkeys: {e}")

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_HOTKEY:
            if wparam == 1:
                # Ctrl + Numpad7 pressed
                self.activate_overlay_without_click()
            elif wparam == 2:
                # Shift + Alt + X pressed
                threading.Thread(target=self.delayed_taskbar_click_then_overlay, daemon=True).start()
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def hotkey_listener(self):
        try:
            self.register_hotkeys()
            # Message loop
            while self.running:
                win32gui.PumpWaitingMessages()
                time.sleep(0.01)
        except Exception:
            print("[Hotkey Listener Exception]")
            traceback.print_exc()

    def quit_app(self):
        self.running = False
        self.unregister_hotkeys()
        self.tray.hide()
        self.app.quit()

if __name__ == '__main__':
    register_startup("ScreenHighlighter")
    TrayApp()
