from PyQt5.QtWidgets import QApplication
from pkg_resources import resource_string
import sys

from .gui import BigBangGui
from .gpio import cleanup


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(
        resource_string('bierwiegen', 'resources/bierwiegen.qss').decode()
    )

    try:
        w = BigBangGui()
        w.showFullScreen()
        sys.exit(app.exec_())
    finally:
        w.scale.wait()
        w.button_thread.wait()
        cleanup()


if __name__ == '__main__':
    main()
