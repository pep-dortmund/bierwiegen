from RPi import GPIO
from threading import Thread, Event


BUTTON_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class ButtonWatchThread(Thread):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            if(GPIO.input(BUTTON_PIN) == 1):
                self.widget.button_press()
                self.event.wait(0.2)
            self.event.wait(0.01)

    def terminate(self):
        self.event.set()
        GPIO.cleanup()
