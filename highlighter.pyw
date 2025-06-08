import sys
import threading
import os

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
    os.execl(sys.executable, sys.executable, *sys.argv)


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

    def activate_overlay(self):
        self.rectangles.clear()
        self.start_point = None
        self.end_point = None
        self.show()
        self.installEventFilter(self)  # Enable keypress detection

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
        self.tray.show()

        self.listener_thread = threading.Thread(target=self.register_hotkey, daemon=True)
        self.listener_thread.start()

        sys.exit(self.app.exec_())

    def register_hotkey(self):
        try:
            keyboard.add_hotkey("ctrl+num 7", lambda: self.signals.show_overlay.emit())
            keyboard.add_hotkey("shift+windows+x", lambda: self.signals.show_overlay.emit())

        except Exception as e:
            print("Hotkey registration failed:", e)

    def quit_app(self):
        keyboard.unhook_all_hotkeys()
        self.tray.hide()
        self.app.quit()


if __name__ == '__main__':
    TrayApp()
