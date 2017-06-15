from PyQt5.QtWidgets import QApplication
import sys
from RPi import GPIO
from time import sleep
from threading import Thread

from . import BigBangGui

BUTTON_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_press_handler(widget):
    while True:
        if(GPIO.input(BUTTON_PIN) == 1):
            widget.button_press()
            sleep(0.2)


def main():
    app = QApplication(sys.argv)

    w = BigBangGui()

    Thread(target=button_press_handler, daemon=True, args=(w, )).start()

    w.showFullScreen()

    ret = app.exec_()
    GPIO.cleanup()
    sys.exit(ret)


if __name__ == '__main__':
    main()
