from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from PenButtonListener import PenButtonListener


class PenControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.event_codes = {
            320: "BTN_TOOL_PEN",
            321: "BTN_TOOL_RUBBER",
            330: "BTN_TOUCH",
            331: "BTN_STYLUS",
            332: "BTN_STYLUS2"
        }
        self.listener = PenButtonListener()
        self.listener.button_pressed.connect(self.on_button_pressed)
        self.listener.start()

    def init_ui(self):
        self.setWindowTitle("Lenovo Pen Button Assign")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        self.label = QLabel("Press your pen button.")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def on_button_pressed(self, info):
        info = info[0], self.event_codes.get(info[1])
        print(info)
        self.label.setText(str(info))

    def closeEvent(self, event):
        self.listener.stop()
        event.accept()
