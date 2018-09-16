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
from time import sleep


def cleanup():
    if HAS_GPIO:
        GPIO.cleanup()


class Scale:
    def __init__(self, dout, pd_sck, scale):
        if HAS_GPIO:
            self.hx711 = HX711(dout, pd_sck, scale)
            self.hx711.tare()

    def get_weight(self, times):
        if HAS_GPIO:
            self.hx711.reset()
            return self.hx711.read(times)
        else:
            return random.uniform(100, 500)

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
        while True:
            if HAS_GPIO:
                if(GPIO.input(self.button_pin) == 0):
                    self.buttonPressed.emit()
                    sleep(1)
            sleep(0.01)
