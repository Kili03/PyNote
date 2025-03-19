import sys

from PySide6.QtWidgets import QApplication

from PenControlApp import PenControlApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PenControlApp()
    window.show()
    sys.exit(app.exec())
