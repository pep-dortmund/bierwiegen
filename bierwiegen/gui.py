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
        self.target = False

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
        if self.target:
            self.measured = random.uniform(100, 500)
            self.scale_label.setText('{:.0f} g'.format(self.measured))

            won = abs(self.measured - self.target) / self.target < 0.1

            self.target = None

            w = WonWindow(won=won)
            w.show()
            sleep(10)
            w.destroy()
            self.target_label.setText('--- g')
        else:
            self.target = random.uniform(100, 500)
            self.target_label.setText('{:.0f} g'.format(self.target))
            self.scale_label.setText('--- g')
            self.measured = None
