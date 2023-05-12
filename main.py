# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QCoreApplication, QSettings, QSize
from PyQt5.QtGui import QIcon
import signal
from mainwindow import *
from settingscontrol import SettingsControl
from command_parser import TerminalParser

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

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

    data_source = None

    if bpm_name_parsed == "model":
        from datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name=bpm_name_parsed)


    elif bpm_name_parsed == "bpm":
        from datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name=bpm_name_parsed)

    else:
        from datasources_all import BPMDataAll
        data_source = BPMDataAll(bpm_name="model")

    if data_source is None:
        print("Data source doesn't exists!!! You can't use this program!!!")
        exit()

    settingsControl = SettingsControl()

    # mw = MainWindow(data_source, settingsControl, bpm_name_parsed)
    # mw.setWindowTitle('pybpmonfail ({})'.format('all'))

    # icon_path = os.path.dirname(os.path.abspath(__file__))
    # mw_icon = QIcon()
    # mw_icon.addFile(os.path.join(icon_path, 'etc/icons/app_icon.png'), QSize(32, 32))
    # mw.setWindowIcon(mw_icon)

    data_source.data_ready.connect(mw.on_current_choice)
    data_source.data_ready.connect(data_proc.on_data_recv)

    settingsControl.add_object(mw)
    settingsControl.read_settings()

    data_proc.data_processed.connect(mw.on_widgets_choice)

    mw.show()
    sys.exit(app.exec_())
