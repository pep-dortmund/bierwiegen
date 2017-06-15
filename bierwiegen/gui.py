from PyQt5.QtCore import QCoreApplication, Qt, QSize
import random
from PyQt5.QtWidgets import (
    QWidget,
    QShortcut,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)
from PyQt5.QtGui import (
    QKeySequence,
    QPixmap,
    QMovie,
)
from pkg_resources import resource_filename

from .gpio import readout_scale


class BigBangGui(QWidget):

    def __init__(self):
        super().__init__()

        self.target = False
        self.setup_shortcuts()
        self.setup_gui()

    def setup_gui(self):
        self.setWindowTitle('PeP@BigBang')
        vbox = QVBoxLayout(self)

        upper_hbox = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap(
            resource_filename('bierwiegen', 'resources/logo_negativ.png'),
        )
        logo.setPixmap(pixmap.scaled(
            800, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        logo.setAlignment(Qt.AlignTop)

        title = QLabel('Bierwiegen', objectName='title')
        title.setAlignment(Qt.AlignTop)

        upper_hbox.addWidget(logo)
        upper_hbox.addWidget(title)
        vbox.addLayout(upper_hbox)

        self.fireworks = QMovie(resource_filename(
            'bierwiegen', 'resources/fireworks.gif'
        ))
        self.fireworks.setScaledSize(QSize(1200, 536))

        self.winning_label = QLabel(objectName='winning_label')
        self.winning_label.setAlignment(Qt.AlignCenter)
        self.winning_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vbox.addWidget(self.winning_label)

        lower_hbox = QHBoxLayout()
        vbox.addLayout(lower_hbox)

        left_vbox = QVBoxLayout()
        right_vbox = QVBoxLayout()

        target_title = QLabel('Ziel', objectName='target_title')
        scale_title = QLabel('Waage', objectName='scale_title')

        left_vbox.addWidget(target_title)
        right_vbox.addWidget(scale_title)

        self.target_label = QLabel('--- g', objectName='target_label')
        left_vbox.addWidget(self.target_label)

        self.scale_label = QLabel('--- g', objectName='scale_label')
        right_vbox.addWidget(self.scale_label)

        lower_hbox.addLayout(left_vbox)
        lower_hbox.addLayout(right_vbox)

        for label in (self.target_label, self.scale_label, scale_title, target_title):
            label.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

    def setup_shortcuts(self):
        QShortcut(QKeySequence('Esc'), self, QCoreApplication.instance().quit)
        QShortcut(QKeySequence('Ctrl+F'), self, self.toggle_fullscreen)
        QShortcut(QKeySequence('Return'), self, self.button_press)

    def closeEvent(self, event):
        QCoreApplication.instance().quit()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def button_press(self):
        if self.target:
            self.measured = readout_scale()
            self.scale_label.setText('{:.0f} g'.format(self.measured))

            won = abs(self.measured - self.target) / self.target < 0.05

            self.target = None

            if won:
                self.winning_label.setMovie(self.fireworks)
                self.fireworks.jumpToFrame(0)
                self.fireworks.start()
            else:
                self.winning_label.setText('Verloren')
                self.winning_label.setStyleSheet('color: red;')
        else:
            self.winning_label.clear()
            self.target = random.uniform(100, 500)
            self.target_label.setText('{:.0f} g'.format(self.target))
            self.scale_label.setText('--- g')
            self.measured = None
