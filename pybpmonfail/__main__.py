# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QCoreApplication, QSettings, QSize
from PyQt5.QtGui import QIcon
import signal
from pybpmonfail.Modules.MainWindow.mainwindow import *
from pybpmonfail.Modules.settingscontrol import SettingsControl
from pybpmonfail.Modules.command_parser import TerminalParser
from pybpmonfail.Modules.DataSources.datasources_all import BPMDataAll
from pybpmonfail.Modules.watcher import *

# pg.setConfigOption('background', 'w')
# pg.setConfigOption('foreground', 'k')

# Allow CTRL+C and/or SIGTERM to kill us (PyQt blocks it otherwise)
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

if __name__ == "__main__":
    """   """
    import sys

    QCoreApplication.setOrganizationName("Denisov")
    QCoreApplication.setApplicationName("pybpmonfail")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)
    app.setStyle('Cleanlooks')

    argument_parser = TerminalParser()
    bpm_name_parsed = argument_parser.bpm_name_parsed
    sound_status = argument_parser.sound_status_parsed
    mw_status = argument_parser.mw_status_parsed

    if bpm_name_parsed == "model":
        #from pybpmonfail.Modules.DataSources.datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name=bpm_name_parsed)
        watcher_1 = Watcher("model01")
        watcher_2 = Watcher("model02")
        watcher_3 = Watcher("model03")
        watcher_4 = Watcher("model04")


    elif bpm_name_parsed == "bpm":
        #from pybpmonfail.Modules.DataSources.datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name=bpm_name_parsed)
        watcher_1 = Watcher("bpm01")
        watcher_2 = Watcher("bpm02")
        watcher_3 = Watcher("bpm03")
        watcher_4 = Watcher("bpm04")

    else:
        #from pybpmonfail.Modules.DataSources.datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name="model")
        watcher_1 = Watcher("model01")
        watcher_2 = Watcher("model02")
        watcher_3 = Watcher("model03")
        watcher_4 = Watcher("model04")

    if data_source is None:
        print("Data source doesn't exists!!! You can't use this program!!!")
        exit()

    settingsControl = SettingsControl()

    watcher_dict = {'bpm01': watcher_1,
                    'bpm02': watcher_2,
                    'bpm03': watcher_3,
                    'bpm04': watcher_4}

    def on_data_recv(data_source):
        """   """
        if data_source.bpm_name in ('model01', 'bpm01'):
            watcher_1.on_data_ready(data_source)
        elif data_source.bpm_name in ('model02', 'bpm02'):
            watcher_2.on_data_ready(data_source)
        elif data_source.bpm_name in ('model03', 'bpm03'):
            watcher_3.on_data_ready(data_source)
        elif data_source.bpm_name in ('model04', 'bpm04'):
            watcher_4.on_data_ready(data_source)
        else: pass

    def period_connector(period_info):
        """   """
        period = period_info[0]
        bpm_name = period_info[1]
        if bpm_name in ('model01', 'bpm01'):
            watcher_1.set_time_length(period)
        elif bpm_name in ('model02', 'bpm02'):
            watcher_2.set_time_length(period)
        elif bpm_name in ('model03', 'bpm03'):
            watcher_3.set_time_length(period)
        elif bpm_name in ('model04', 'bpm04'):
            watcher_4.set_time_length(period)
        else: pass

    def sound_connector(sound_info):
        """   """
        sound = sound_info[0]
        bpm_name = sound_info[1]
        print('sound')
        if bpm_name in ('model01', 'bpm01'):
            watcher_1.set_sound_enabled(sound)
        elif bpm_name in ('model02', 'bpm02'):
            watcher_2.set_sound_enabled(sound)
        elif bpm_name in ('model03', 'bpm03'):
            watcher_3.set_sound_enabled(sound)
        elif bpm_name in ('model04', 'bpm04'):
            watcher_4.set_sound_enabled(sound)
        else: pass

    if mw_status == 'on':
        mw = MainWindow(settingsControl, watcher_1, watcher_2, watcher_3, watcher_4)
        mw.setWindowTitle('PyBPMonFail ({})'.format('all'))

        icon_path = os.path.dirname(os.path.abspath(__file__))
        mw_icon = QIcon()
        mw_icon.addFile(os.path.join(icon_path, 'etc/icons/app_icon.png'), QSize(32, 32))
        mw.setWindowIcon(mw_icon)

        settingsControl.add_object(mw)
        settingsControl.add_object(mw.statusWidget_1)
        settingsControl.add_object(mw.statusWidget_2)
        settingsControl.add_object(mw.statusWidget_3)
        settingsControl.add_object(mw.statusWidget_4)

        watcher_1.alarm_status.connect(mw.on_alarm_status)
        watcher_2.alarm_status.connect(mw.on_alarm_status)
        watcher_3.alarm_status.connect(mw.on_alarm_status)
        watcher_4.alarm_status.connect(mw.on_alarm_status)

        mw.period_changed.connect(period_connector)
        mw.sound_changed.connect(sound_connector)

        mw.show()
    else: pass

    data_source.data_ready.connect(on_data_recv)

    settingsControl.read_settings()

    sys.exit(app.exec_())
