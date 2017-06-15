from PyQt5.QtWidgets import QApplication
import sys

from .gui import BigBangGui
from .gpio import ButtonWatchThread


def main():
    app = QApplication(sys.argv)

    w = BigBangGui()

    t = ButtonWatchThread(w)
    t.start()

    w.showFullScreen()

    ret = app.exec_()

    t.terminate()
    sys.exit(ret)


if __name__ == '__main__':
    main()
