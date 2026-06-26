#
#
import numpy as np
#import pycx4.qcda as cda
from pybpmonfail.Modules.DataSources.BPM_template import BPMTemplate
import pybpmonfail.Modules.DataSources.datasources_bpm as ds_bpm
import pybpmonfail.Modules.DataSources.datasources as ds_model

class BPMDataAll(BPMTemplate):
    """   """

    """Default time for timer in ms"""
    DEFAULT_TIME = 5*1000
    """Control for hash"""
    control = (1, 1, 1, 1)
    """BPM name"""
    bpm = "bpm_all"
    """istart type"""
    istart_work = (0, 0, 0, 0)

    def __init__(self, bpm_name='', parent=None):
        super().__init__(bpm_name, parent)

        self.data_bpm = None
        self.istart = None
        self.bpm_name_local = None

        if bpm_name == 'bpm':
            self.BPM1 = ds_bpm.BPMData("bpm01")
            self.BPM2 = ds_bpm.BPMData("bpm02")
            self.BPM3 = ds_bpm.BPMData("bpm03")
            self.BPM4 = ds_bpm.BPMData("bpm04")
            self.CCD1 = ds_bpm.BPMData("ccd01")
            self.CCD2 = ds_bpm.BPMData("ccd02")
            self.CCD3 = ds_bpm.BPMData("ccd03")
            self.CCD4 = ds_bpm.BPMData("ccd04")
        elif bpm_name == 'model':
            print('model')
            self.BPM1 = ds_model.BPMData("model01")
            self.BPM2 = ds_model.BPMData("model02")
            self.BPM3 = ds_model.BPMData("model03")
            self.BPM4 = ds_model.BPMData("model04")
            self.CCD1 = ds_model.BPMData("model05")
            self.CCD2 = ds_model.BPMData("model06")
            self.CCD3 = ds_model.BPMData("model07")
            self.CCD4 = ds_model.BPMData("model08")
        else:
            self.BPM1 = ds_model.BPMData("model01")
            self.BPM2 = ds_model.BPMData("model02")
            self.BPM3 = ds_model.BPMData("model03")
            self.BPM4 = ds_model.BPMData("model04")
            self.CCD1 = ds_model.BPMData("model05")
            self.CCD2 = ds_model.BPMData("model06")
            self.CCD3 = ds_model.BPMData("model07")
            self.CCD4 = ds_model.BPMData("model08")

        self.BPM1.data_ready.connect(self.on_data_ready)
        self.BPM2.data_ready.connect(self.on_data_ready)
        self.BPM3.data_ready.connect(self.on_data_ready)
        self.BPM4.data_ready.connect(self.on_data_ready)
        self.CCD1.data_ready.connect(self.on_data_ready)
        self.CCD2.data_ready.connect(self.on_data_ready)
        self.CCD3.data_ready.connect(self.on_data_ready)
        self.CCD4.data_ready.connect(self.on_data_ready)

    def on_data_ready(self, BPM):
        """   """
        self.bpm_name = BPM.bpm_name
        self.istart = BPM.istart
        self.reshaping_data(BPM)

    def reshaping_data(self, BPM):
        """   """
        # self.bpm_name_local = BPM.bpm_name
        data_len = len(BPM.dataT)
        data_bpm = self.reshaping_arrays(BPM.dataT, BPM.dataX, BPM.dataZ, BPM.dataI)
        self.data_bpm = data_bpm
        self.data_ready.emit(self)

    def reshaping_arrays(self, M1, M2, M3, M4):
        """   """
        newMass = np.zeros((len(M1),4))
        newMass[:, 0] = M1
        newMass[:, 1] = M2
        newMass[:, 2] = M3
        newMass[:, 3] = M4

        return(newMass)
