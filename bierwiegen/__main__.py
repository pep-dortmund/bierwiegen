from PyQt5.QtWidgets import QApplication
from pkg_resources import resource_string
import sys
import os
from time import gmtime, strftime

from .gui import BigBangGui
from .gpio import ButtonWatchThread


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(
        resource_string('bierwiegen', 'resources/bierwiegen.qss').decode()
    )

    start_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    if not os.path.isdir(os.path.expanduser("~/bierwiegen_logs")):
        os.mkdir(os.path.expanduser("~/bierwiegen_logs"))
    outputfile = open(os.path.expanduser("~/bierwiegen_logs/log_%s.txt" % start_time), "w")
    outputfile.write("time" + "\t" + "target" + "\t" + "measured" + "\t" + "abs" + "\n")

    w = BigBangGui(5, outputfile)

    t = ButtonWatchThread(pin=11, widget=w)
    t.start()

    w.showFullScreen()

    ret = app.exec_()

    t.terminate()
    outputfile.close()
    sys.exit(ret)


if __name__ == '__main__':
    main()
