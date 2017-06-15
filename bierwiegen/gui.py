from PyQt5.QtCore import QCoreApplication, Qt
import random
import pkg_resources
from time import sleep
from PyQt5.QtWidgets import (
    QWidget,
    QShortcut,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QApplication,
)
from PyQt5.QtGui import (
    QKeySequence,
    QPixmap,
    QFontDatabase,
)


class WonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        self.move(QApplication.desktop().center)

        vbox = QVBoxLayout()

        label = QLabel('Gewonnen')
        font = label.font()
        font.setPointSize(120)
        font.setBold(True)
        label.setFont(font)
        vbox.addWidget(label)

        self.setLayout(vbox)
        self.show()


class BigBangGui(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PeP@BigBang')
        self.exit_shortcut = QShortcut(
            QKeySequence('Esc'),
            self,
            QCoreApplication.instance().quit
        )

        self.setStyleSheet('background-color: white;')
        self.target_set = False

        vbox = QVBoxLayout(self)

        upper_hbox = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap(pkg_resources.resource_filename(
            'bierwiegen', 'resources/logo_negativ.png'
        ))
        logo.setPixmap(pixmap.scaled(800, 300, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignTop)

        title = QLabel('Bierwiegen')
        # title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        title.setAlignment(Qt.AlignTop)
        title_font = title.font()
        title_font.setPointSize(120)
        title_font.setBold(True)
        title.setFont(title_font)

        upper_hbox.addWidget(logo)
        upper_hbox.addWidget(title)
        vbox.addLayout(upper_hbox)

        lower_hbox = QHBoxLayout()
        vbox.addLayout(lower_hbox)

        left_vbox = QVBoxLayout()
        right_vbox = QVBoxLayout()

        target_title = QLabel('Ziel')
        scale_title = QLabel('Waage')

        left_vbox.addWidget(target_title)
        right_vbox.addWidget(scale_title)

        self.target_label = QLabel('--- g')
        left_vbox.addWidget(self.target_label)

        self.scale_label = QLabel('--- g')
        right_vbox.addWidget(self.scale_label)

        lower_hbox.addLayout(left_vbox)
        lower_hbox.addLayout(right_vbox)

        font = scale_title.font()
        font.setPointSize(120)
        font.setBold(True)

        number_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        number_font.setPointSize(120)
        number_font.setBold(True)

        for label in (self.target_label, self.scale_label):
            label.setFont(number_font)
            label.setAlignment(Qt.AlignCenter)

        for label in (scale_title, target_title):
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

    def button_press(self):
        if self.target_set:
            self.scale_label.setText(
                '{:.0f} g'.format(random.uniform(100, 500))
            )
            self.target_set = False
            w = WonWindow()
            w.show()
            sleep(5)
            w.hide()
        else:
            self.target_label.setText(
                '{:.0f} g'.format(random.uniform(100, 500))
            )
            self.scale_label.setText('--- g')
            self.target_set = True
