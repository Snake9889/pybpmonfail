# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import Qt, QObject
import argparse

class TerminalParser(QObject):
    """   """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parser = argparse.ArgumentParser(description='Startup settings for software')

        self.parser.add_argument('-sn', action='store', default='on', dest='sound_status',
                                help='Sound status - on or off.')
        self.parser.add_argument('-bn', action='store', default='bpm', dest='bpm_name',
                                help='Type of bpm for monitoring - model (for tests) or real 4 BPMs')
        self.parser.add_argument('-mw', action='store', default='on', dest='mw_status',
                                 help='MainWindow mode - on or off')

        self.results = self.parser.parse_args()
        self.sound_status_parsed = self.results.sound_status
        self.bpm_name_parsed = self.results.bpm_name
        self.mw_status_parsed = self.results.mw_status
