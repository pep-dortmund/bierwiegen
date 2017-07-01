import warnings
import random
try:
    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)
    HAS_GPIO = True
except RuntimeError:
    HAS_GPIO = False
    warnings.warn("Not on a raspberry pi")

from threading import Thread, Event
from .hx711 import HX711


def cleanup():
    if HAS_GPIO:
        GPIO.cleanup()


class Scale:
    def __init__(self, dout, pd_sck):
        if HAS_GPIO:
            self.hx711 = HX711(dout, pd_sck)
            self.hx711.set_reading_format("LSB", "MSB")
            self.hx711.set_reference_unit(693.21)
            self.hx711.reset()
            self.hx711.tare()

    def get_weight(self, times):
        if HAS_GPIO:
            self.hx711.reset()
            return self.hx711.get_weight(times)
        else:
            return random.uniform(100, 500)

    def tare(self):
        if HAS_GPIO:
            self.hx711.tare()


class ButtonWatchThread(Thread):

    def __init__(self, pin, widget):
        super().__init__()
        self.button_pin = pin
        self.widget = widget
        self.event = Event()

        if HAS_GPIO:
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def run(self):
        while not self.event.is_set():
            if HAS_GPIO:
                if(GPIO.input(self.button_pin) == 0):
                    self.widget.button_press()
                    self.event.wait(1)
                    # self.event.wait(0.2)
            self.event.wait(0.01)

    def terminate(self):
        self.event.set()
        if HAS_GPIO:
            GPIO.cleanup()
