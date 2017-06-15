from PyQt5.QtCore import QCoreApplication, Qt
import random
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
)
from pkg_resources import resource_filename


class WonWindow(QWidget):
    def __init__(self, won=True):
        super().__init__()

        vbox = QVBoxLayout()

        if won:
            label = QLabel('Gewonnen')
        else:
            label = QLabel('Verloren')

        self.adjustSize()
        center = QApplication.desktop().availableGeometry().center()
        self.move(center.x() - self.width() // 2, center.y() - self.height() // 2)
        self.setWindowFlags(Qt.FramelessWindowHint)

        vbox.addWidget(label)

        self.setLayout(vbox)
        self.show()


class BigBangGui(QWidget):

    def __init__(self):
        super().__init__()

        self.target = False
        self.w = None

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
            self.measured = random.uniform(100, 500)
            self.scale_label.setText('{:.0f} g'.format(self.measured))

            won = abs(self.measured - self.target) / self.target < 0.1

            self.target = None

            self.w = WonWindow(won=won)
            self.w.show()
        else:
            if self.w:
                self.w.destroy()
            self.target = random.uniform(100, 500)
            self.target_label.setText('{:.0f} g'.format(self.target))
            self.scale_label.setText('--- g')
            self.measured = None
