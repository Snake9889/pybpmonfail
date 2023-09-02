# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import os.path


class StatusWidget(QWidget):
    """   """
    period_changed = pyqtSignal(object)
    sound_changed = pyqtSignal(object)


    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'StatusWidget.ui'), self)

        self.bpm_name = None
        self.period = 30
        self.sound = None

        self.periodSBox.setValue(30)

        self.periodSBox.valueChanged.connect(self.on_periodsbox_changed)
        self.sound_checkBox.stateChanged.connect(self.on_sound_checked)


    def on_periodsbox_changed(self, value):
        """   """
        self.period = value
        self.period_changed.emit(self)

    def on_sound_checked(self, state):
        """   """
        if state == Qt.Checked:
            self.sound = "on"
        else:
            self.sound = "off"
        self.sound_changed.emit(self)

    def set_bpm(self, bpm):
        """   """
        self.bpm_name = bpm

    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm_name)
        settings.setValue("period", self.period)
        settings.setValue("sound", self.sound)
        settings.endGroup()
        print("Saved!!!!!")
        settings.sync()

    def read_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm_name)
        self.period = settings.value("period", 30, type=float)
        self.sound = settings.value("sound", "on")
        settings.endGroup()


        if self.sound == "on":
            self.sound_checkBox.setCheckState(Qt.Checked)
        elif self.sound == "off":
            self.sound_checkBox.setCheckState(Qt.Unchecked)
        self.sound_changed.emit(self)

        self.periodSBox.setValue(self.period)
        self.period_changed.emit(self)
