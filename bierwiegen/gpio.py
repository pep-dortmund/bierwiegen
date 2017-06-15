import warnings
try:
    from RPi import GPIO
    GPIO.setmode(GPIO.BOARD)
    HAS_GPIO = True
except RuntimeError:
    HAS_GPIO = False
    warnings.warn("Not on a raspberry pi")

from threading import Thread, Event


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
                if(GPIO.input(self.button_pin) == 1):
                    self.widget.button_press()
                    self.event.wait(0.2)
            self.event.wait(0.01)

    def terminate(self):
        self.event.set()
        if HAS_GPIO:
            GPIO.cleanup()
