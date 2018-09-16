import warnings
import random
try:
    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)
    HAS_GPIO = True
except RuntimeError:
    HAS_GPIO = False
    warnings.warn("Not on a raspberry pi")

from PyQt5.QtCore import QThread, pyqtSignal
from .hx711 import HX711
from time import sleep, clock


def cleanup():
    if HAS_GPIO:
        GPIO.cleanup()


class Scale(QThread):
    done = pyqtSignal(float, arguments=['weight'])

    def __init__(self, dout, pd_sck, scale, n=5):
        self.n = n
        super().__init__()
        if HAS_GPIO:
            self.hx711 = HX711(dout, pd_sck, scale)
            self.hx711.tare()
            self.last_reset = clock()

    def get_weight(self):
        self.start()

    def run(self):
        if HAS_GPIO:
            now = clock()
            if now - self.last_reset > 600:
                self.hx711.reset()
                self.last_reset = now
            self.done.emit(self.hx711.read(self.n))
        else:
            self.done.emit(random.uniform(100, 500))

    def tare(self):
        if HAS_GPIO:
            self.hx711.tare()


class ButtonWatchThread(QThread):

    buttonPressed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button_pin = pin

        if HAS_GPIO:
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def run(self):
        while not self.isInterruptionRequested():
            if HAS_GPIO:
                if not GPIO.input(self.button_pin):
                    self.buttonPressed.emit()
                    sleep(0.5)
            sleep(0.01)
