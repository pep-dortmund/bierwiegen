from time import sleep
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

if HAS_GPIO:
    scale = HX711(18, 16) 
    scale.set_reading_format("LSB", "MSB")
    scale.set_reference_unit(693.21)
    scale.reset()
    scale.tare()

def readout_scale():
    if HAS_GPIO:
        scale.reset()
        return scale.get_weight(5)
    else:
        return random.uniform(100, 500)


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
                    #self.event.wait(0.2)
            self.event.wait(0.01)

    def terminate(self):
        self.event.set()
        if HAS_GPIO:
            GPIO.cleanup()
