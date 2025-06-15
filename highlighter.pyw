import sys
import threading
import os
import logging
import ctypes
import time

# --- DPI Awareness: Avoid scaling/overlay issues ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # SYSTEM_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# --- Logging for debugging .exe version ---
logging.basicConfig(
    filename="highlighter.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.debug("🔵 highlighter.pyw started")

# --- Auto-install PyQt5 and keyboard if missing ---
try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QSystemTrayIcon, QMenu, QAction
    )
    from PyQt5.QtGui import QPainter, QPen, QColor, QIcon, QPixmap
    from PyQt5.QtCore import Qt, QRect, pyqtSignal, QObject
    import keyboard
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "keyboard"])
    if not getattr(sys, 'frozen', False):  # Not running as bundled executable
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        sys.exit(1)  # Exit if running as compiled .exe to prevent double processes

def click_taskbar():
    """Simulate a left mouse click on the bottom-center of the screen (taskbar area)."""
    try:
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        x = screen_width // 2
        y = screen_height - 5  # 5 pixels above bottom, should be on taskbar

        # Move cursor
        ctypes.windll.user32.SetCursorPos(x, y)
        # Mouse down (left button)
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        # Mouse up (left button)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
        logging.debug(f"🖱️ Clicked taskbar at ({x},{y}) to unfocus")
    except Exception as e:
        logging.error(f"Failed to click taskbar: {e}")

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
        try:
            hwnd = self.winId().__int__()
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                              SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
            logging.debug("🔝 Overlay set to topmost window")
        except Exception as e:
            logging.error(f"Failed to set window topmost: {e}")

    def activate_overlay(self):
        logging.debug("🟩 Overlay activated")
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
            logging.debug("↩️ Undo last rectangle")
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
        self.tray.show()

        self.listener_thread = threading.Thread(target=self.register_hotkey, daemon=True)
        self.listener_thread.start()

        sys.exit(self.app.exec_())

    def activate_overlay_with_taskbar_click(self):
        try:
            keyboard.block_key('x')  # Block X so it’s not typed
            click_taskbar()
            time.sleep(0.05)
            self.signals.show_overlay.emit()
        finally:
            time.sleep(0.1)
            keyboard.unblock_key('x')

    def register_hotkey(self):
        try:
            logging.debug("⌨️ Registering hotkeys")
            keyboard.add_hotkey("ctrl+num 7", self.activate_overlay_with_taskbar_click, suppress=True)
            keyboard.add_hotkey("shift+windows+x", self.activate_overlay_with_taskbar_click, suppress=True)
        except Exception:
            logging.exception("Hotkey registration failed")

    def quit_app(self):
        logging.debug("❌ Quitting application")
        keyboard.unhook_all_hotkeys()
        self.tray.hide()
        self.app.quit()


if __name__ == '__main__':
    try:
        TrayApp()
    except Exception:
        logging.exception("Unhandled exception in main")
