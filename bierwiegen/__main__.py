from PyQt5.QtWidgets import QApplication
from pkg_resources import resource_string
import sys

from .gui import BigBangGui
from .gpio import ButtonWatchThread


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(
        resource_string('bierwiegen', 'resources/bierwiegen.qss').decode()
    )

    w = BigBangGui()

    t = ButtonWatchThread(pin=11, widget=w)
    t.start()

    w.showFullScreen()

    ret = app.exec_()

    t.terminate()
    sys.exit(ret)


if __name__ == '__main__':
    main()
