import evdev
from PySide6.QtCore import QThread, Signal

class PenButtonListener(QThread):
    button_pressed = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.device_path = self.find_pen_device()

    def find_pen_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        print(evdev.list_devices())
        for device in devices:
            print(device.name)
            if "Pen" in device.name:  # Adjust this based on `evtest` output
                return device.path
        return None

    def run(self):
        if not self.device_path:
            self.button_pressed.emit((-1, -1))
            return

        device = evdev.InputDevice(self.device_path)
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                self.button_pressed.emit((event.value, event.code))

    def stop(self):
        self.running = False