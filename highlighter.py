import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect


class FlameshotOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)

        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        self.start_point = None
        self.end_point = None
        self.rectangles = []

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Step 1: Dim the entire screen
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        # Step 2: "Clear" each rectangle area to show screen behind
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        for rect in self.rectangles:
            painter.fillRect(rect, Qt.transparent)

        # Live preview rectangle
        if self.start_point and self.end_point:
            live_rect = QRect(self.start_point, self.end_point).normalized()
            painter.fillRect(live_rect, Qt.transparent)

        # Step 3: Draw green outlines on top
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()  # Close the application fully
        elif event.key() == Qt.Key_Z and (event.modifiers() & Qt.ControlModifier):
            if self.rectangles:
                self.rectangles.pop()
                self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = FlameshotOverlay()
    sys.exit(app.exec_())