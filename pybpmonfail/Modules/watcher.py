
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
import os
from datetime import datetime
from playsound import playsound

class Watcher(QObject):
    """   """
    alarm_status = pyqtSignal(object)

    """ Default time for timer in ms """
    DEFAULT_TIME = 5*1000

    def __init__(self, bpm_name='', time_lenght=DEFAULT_TIME, sound_status=True, parent=None):
        super().__init__(parent)

        self.time_lenght = time_lenght
        self.bpm_name = bpm_name
        self.sound_status = sound_status

        self.last_time = None
        self.enumerator = 0
        self.alarm = 0
        self.istart = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_update)
        self.timer.start(self.time_lenght)

        self.sound_path = os.path.dirname(os.path.abspath(__file__))
        self.music_win = {"bpm01": 'MainWindow\etc\sound\BPM01_stopped.mp3',
                          "bpm02": 'MainWindow\etc\sound\BPM02_stopped.mp3',
                          "bpm03": 'MainWindow\etc\sound\BPM03_stopped.mp3',
                          "bpm04": 'MainWindow\etc\sound\BPM04_stopped.mp3',
                          "model01": 'MainWindow\etc\sound\Model_stopped.mp3',
                          "model02": 'MainWindow\etc\sound\Model_stopped.mp3',
                          "model03": 'MainWindow\etc\sound\Model_stopped.mp3',
                          "model04": 'MainWindow\etc\sound\Model_stopped.mp3'}
        self.music_lin = {"bpm01": 'MainWindow/etc/sound/BPM01_stopped.mp3',
                          "bpm02": 'MainWindow/etc/sound/BPM02_stopped.mp3',
                          "bpm03": 'MainWindow/etc/sound/BPM03_stopped.mp3',
                          "bpm04": 'MainWindow/etc/sound/BPM04_stopped.mp3',
                          "model01": 'MainWindow/etc/sound/Model_stopped.mp3',
                          "model02": 'MainWindow/etc/sound/Model_stopped.mp3',
                          "model03": 'MainWindow/etc/sound/Model_stopped.mp3',
                          "model04": 'MainWindow/etc/sound/Model_stopped.mp3'}

    def on_timer_update(self):
        """   """
        if self.istart != 1:
            self.alarm = 0
            if self.istart == 0:
                self.sound_status = False
            self.alarm_status.emit(self)
        else:
            if self.enumerator != 0:
                self.enumerator = 0
                self.alarm = 0
                self.timer.start(self.time_lenght)
                self.alarm_status.emit(self)
            else:
                self.on_sound_played()
                self.alarm = 1
                self.timer.start(self.time_lenght)
                self.alarm_status.emit(self)

    def on_data_ready(self, BPM):
        """   """
        self.bpm_name = BPM.bpm_name
        self.enumerator += 1
        self.istart = BPM.istart
        now = datetime.now()
        self.last_time = now.strftime("%H:%M:%S")

    def on_sound_played(self):
        """   """
        if self.sound_status == True:
            sound_path = None
            sound_path = os.path.join(self.sound_path, self.music_lin[self.bpm_name])
            print(sound_path)
            playsound(sound_path)
        else:
            pass

    def set_sound_enabled(self, sound_enabled: bool):
        """   """
        print(sound_enabled)
        self.sound_status = sound_enabled

    def get_sound_enabled(self):
        """   """
        return(self.sound_status)

    def get_last_time(self):
        """   """
        return(self.last_time)

    def get_start_type(self):
        """   """
        return(self.istart)

    def get_bpm_name(self):
        """   """
        return(self.bpm_name)

    def set_time_length(self, time_lenght):
        """   """
        self.time_lenght = time_lenght *1000
        print(time_lenght)
