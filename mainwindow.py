# This Python file uses the following encoding: utf-8

import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5.QtCore import pyqtSignal, QSettings, QSize, QPoint
from PyQt5 import uic
from helpwidget import HelpWidget



class MainWindow(QMainWindow):
    """   """
    period_changed = pyqtSignal(object)
    sound_changed = pyqtSignal(object)
    
    def __init__(self, settings_control, *args, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow.ui'), self)
        
        self.bpm01_dict = {'BPM_label': self.ui.statusWidget_1.BPM_label, 'time_label': self.ui.statusWidget_1.time_label,
                           'status': self.ui.statusWidget_1.status, 'name': 'X<sub>01</sub>'}
        self.bpm02_dict = {'BPM_label': self.ui.statusWidget_2.BPM_label, 'time_label': self.ui.statusWidget_2.time_label,
                           'status': self.ui.statusWidget_2.status, 'name': 'X<sub>02</sub>'}
        self.bpm03_dict = {'BPM_label': self.ui.statusWidget_3.BPM_label, 'time_label': self.ui.statusWidget_3.time_label,
                           'status': self.ui.statusWidget_3.status, 'name': 'X<sub>03</sub>'}
        self.bpm04_dict = {'BPM_label': self.ui.statusWidget_4.BPM_label, 'time_label': self.ui.statusWidget_4.time_label,
                           'status': self.ui.statusWidget_4.status, 'name': 'X<sub>04</sub>'}

        self.settingsControl = settings_control
        self.watcher_1 = args[0]
        self.watcher_2 = args[1]
        self.watcher_3 = args[2]
        self.watcher_4 = args[3]
        
        self.widgets_customization()
        
        self.statusWidget_1.set_bpm('bpm01')
        self.statusWidget_2.set_bpm('bpm02')
        self.statusWidget_3.set_bpm('bpm03')
        self.statusWidget_4.set_bpm('bpm04')
        
        self.statusWidget_1.period_changed.connect(self.on_perion_changed)
        self.statusWidget_1.sound_changed.connect(self.on_sound_changed)
        self.statusWidget_2.period_changed.connect(self.on_perion_changed)
        self.statusWidget_2.sound_changed.connect(self.on_sound_changed)
        self.statusWidget_3.period_changed.connect(self.on_perion_changed)
        self.statusWidget_3.sound_changed.connect(self.on_sound_changed)
        self.statusWidget_4.period_changed.connect(self.on_perion_changed)
        self.statusWidget_4.sound_changed.connect(self.on_sound_changed)

        self.actionSave.triggered.connect(self.on_save_button)
        self.actionRead.triggered.connect(self.on_read_button)

        self.actionExit.triggered.connect(self.on_exit_button)
        self.actionExit.triggered.connect(QApplication.instance().quit)

        self.help_widget = HelpWidget(os.path.join(ui_path, 'etc/icons/Help_1.png'))
        self.actionHelp.triggered.connect(self.help_widget.show)

    def on_exit_button(self):
        """   """
        print(self, ' Exiting... Bye...')

    def on_read_button(self):
        """   """
        self.settingsControl.read_settings()

    def on_save_button(self):
        """   """
        self.settingsControl.save_settings()

    def widgets_customization(self):
        """   """
        self.curr_widget_customization(self.bpm01_dict, self.watcher_1.get_start_type())
        self.curr_widget_customization(self.bpm02_dict, self.watcher_2.get_start_type())
        self.curr_widget_customization(self.bpm03_dict, self.watcher_3.get_start_type())
        self.curr_widget_customization(self.bpm04_dict, self.watcher_4.get_start_type())
    
    def curr_widget_customization(self, w_dict, start_type):
        """   """
        if start_type == 1:
            w_dict['status'].setStyleSheet("QLabel{background-color: green; border: 1px solid black; border-radius: 10px;}")
            w_dict['status'].setToolTip("Run regime")
        elif start_type == 0:
            w_dict['status'].setStyleSheet("QLabel{background-color: yellow; border: 1px solid black; border-radius: 10px;}")
            w_dict['status'].setToolTip("Injection regime")
        else:
            w_dict['status'].setStyleSheet("QLabel{background-color: red; border: 1px solid black; border-radius: 10px;}")
            w_dict['status'].setToolTip("Something wrong with istart")
        name = w_dict['name']
        w_dict['BPM_label'].setText(f'{name}')

    def on_alarm_status(self, watcher):
        """   """
        status = watcher.alarm
        if watcher.bpm_name in ('model_1', 'bpm01'):
            self.on_widget_status_changed(self.bpm01_dict, watcher.get_last_time(), status)
        elif watcher.bpm_name in ('model_2', 'bpm02'):
            self.on_widget_status_changed(self.bpm02_dict, watcher.get_last_time(), status)
        elif watcher.bpm_name in ('model_3', 'bpm03'):
            self.on_widget_status_changed(self.bpm03_dict, watcher.get_last_time(), status)
        elif watcher.bpm_name in ('model_4', 'bpm04'):
            self.on_widget_status_changed(self.bpm04_dict, watcher.get_last_time(), status)
        else: pass

    def on_widget_status_changed(self, w_dict, time, status):
        """   """
        if status == 1:
            w_dict['status'].setStyleSheet("QLabel{background-color: green; border: 1px solid black; border-radius: 10px;}")
            w_dict['status'].setToolTip("Run regime")
        else:
            w_dict['status'].setStyleSheet("QLabel{background-color: red; border: 1px solid black; border-radius: 10px;}")
            w_dict['status'].setToolTip("Data didn't come!")
        w_dict['time_label'].setText(f'{time}')
        
    def on_sound_changed(self, statusWidget):
        """   """
        if statusWidget.sound == 'on':
            sound = True
        else: sound = False
        bpm = statusWidget.bpm_name
        sound_info = (sound, bpm)
        self.sound_changed.emit(sound_info)
        
    def on_perion_changed(self, statusWidget):
        """   """
        period = statusWidget.period
        bpm = statusWidget.bpm_name
        period_info = (period, bpm)
        self.period_changed.emit(period_info)

    def save_settings(self):
        """   """
        settings = QSettings()
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        settings.sync()

    def read_settings(self):
        """   """
        settings = QSettings()
        self.resize(settings.value('size', QSize(500, 500)))
        self.move(settings.value('pos', QPoint(60, 60)))
        settings.endGroup()
