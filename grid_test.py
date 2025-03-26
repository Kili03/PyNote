import sys

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QPushButton, QGraphicsPixmapItem, \
    QGraphicsItem


class GridItem(QGraphicsItem):
    """A vector-based grid that dynamically redraws based on zoom level."""

    def __init__(self, grid_size=20):
        super().__init__()
        self.grid_size = grid_size
        self.grid_pen = QPen(QColor(0, 0, 50, 255), 1)  # Thin pen

    def boundingRect(self):
        """Defines the bounding area of the grid (large enough to cover the scene)."""
        return QRectF(0, 0, 8000, 6000)

    def paint(self, painter, option, widget=None):
        """Draws the grid dynamically within the visible scene area."""
        painter.setPen(self.grid_pen)

        # Ensure widget is a QGraphicsView
        if isinstance(widget, QGraphicsView):
            rect = widget.mapToScene(widget.viewport().rect()).boundingRect()
        else:
            rect = self.boundingRect()

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        # Draw vertical lines
        x = left
        while x < rect.right():
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
            x += self.grid_size

        # Draw horizontal lines
        y = top
        while y < rect.bottom():
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)
            y += self.grid_size

    def set_grid_size(self, new_size):
        """Adjusts the grid size dynamically."""
        self.grid_size = max(5, min(new_size, 100))  # Prevent too small or too large grids
        self.update()  # Redraw the grid



class DrawEraseCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor(255, 255, 255))
        self.setScene(self.scene)

        # Create and add the vector-based grid
        self.grid = GridItem(grid_size=20)
        self.scene.addItem(self.grid)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.drawing = False
        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 3
        self.setSceneRect(0, 0, 8000, 6000)

        self.last_point = QPointF()
        self.setMouseTracking(True)

        # Panning
        self.panning = False
        self.last_pan_point = QPointF()

    def wheelEvent(self, event):
        """Zoom in/out with the mouse wheel and adjust the grid spacing."""
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.scale(factor, factor)

        # Adjust grid size dynamically based on zoom level
        if factor > 1:  # Zooming in
            new_grid_size = self.grid.grid_size * factor
        else:  # Zooming out
            new_grid_size = self.grid.grid_size / factor

        self.grid.set_grid_size(new_grid_size)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = self.mapToScene(event.position().toPoint())
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = True
            self.last_pan_point = event.position()

    def mouseMoveEvent(self, event):
        if self.drawing:
            current_point = self.mapToScene(event.position().toPoint())
            self.scene.addLine(
                self.last_point.x(), self.last_point.y(),
                current_point.x(), current_point.y(),
                QPen(self.pen_color, self.pen_width)
            )
            self.last_point = current_point
        elif self.panning:
            delta = event.position() - self.last_pan_point
            self.last_pan_point = event.position()
            self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value() - delta.x()))
            self.verticalScrollBar().setValue(int(self.verticalScrollBar().value() - delta.y()))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.panning = False

    def erase(self):
        """Erase only drawings while keeping the grid background."""
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):  # Avoid clearing the grid
                continue
            self.scene.removeItem(item)

    def set_pen_color(self, color):
        self.pen_color = color


class DrawingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Movable Grid Drawing App")
        self.setGeometry(100, 100, 900, 700)

        self.canvas = DrawEraseCanvas()

        # Buttons
        self.erase_button = QPushButton("Erase", self)
        self.erase_button.clicked.connect(self.canvas.erase)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.erase_button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DrawingApp()
    window.show()

    sys.exit(app.exec())
