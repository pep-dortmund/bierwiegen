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
import os
import yaml

from .gpio import Scale


config_file_path = os.path.join(os.environ['HOME'], '.config/bierwiegen/config.yaml')
config_dir = os.path.dirname(config_file_path)
pep_logo = resource_filename('bierwiegen', 'resources/logo_negativ.png')


class BigBangGui(QWidget):

    def __init__(self):
        super().__init__()

        self.target = False

        self.config = {}
        if not os.path.isfile(config_file_path):
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
        else:
            self.load_config()

        self.scale = Scale(
            self.config.get('dout_pin', 18),
            self.config.get('pd_sck_pin', 16),
        )
        self.setup_shortcuts()
        self.setup_gui()

    def setup_gui(self):
        self.setWindowTitle(self.config.get('title', 'PeP@BigBang'))
        vbox = QVBoxLayout(self)

        upper_hbox = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap(self.config.get('logo', pep_logo))
        logo.setPixmap(pixmap.scaled(
            800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
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
        self.fireworks.setScaledSize(QSize(1000, 450))

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
        QShortcut(QKeySequence('Ctrl+T'), self, self.scale.tare)
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
            self.measured = self.scale.get_weight(5)
            self.scale_label.setText('{: >-3.0f} g'.format(self.measured))

            diff = self.measured - self.target
            won = abs(diff) <= self.config.get('tolerance', 10)

            self.target = None

            self.winning_label.clear()
            if won:
                self.winning_label.setMovie(self.fireworks)
                self.fireworks.start()
            else:
                self.winning_label.setText('Verloren')
                self.winning_label.setStyleSheet('color: red;')
        else:
            self.winning_label.clear()
            self.target = random.uniform(
                self.config.get('lower_limit', 100),
                self.config.get('upper_limit', 500)
            )
            self.target_label.setText('{:.0f} g'.format(self.target))
            self.scale_label.setText('--- g')
            self.measured = None

    def load_config(self):
        with open(config_file_path) as f:
            self.config = yaml.safe_load(f)

    def save_config(self):
        with open(config_file_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
