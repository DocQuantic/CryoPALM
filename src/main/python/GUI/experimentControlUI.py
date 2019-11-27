# -*- coding: utf-8 -*-
"""
This file contains the UI code for the experiment control window.

Created on Tue Jun 26 16:18:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.acquisitionControlPALM as palmAcqControl
import GUI.Widgets.microscopeSettings as scopeSettings
import GUI.Widgets.acquisitionControl as acqControl
import GUI.Widgets.cameraSettings as camSettings
from PyQt5 import QtWidgets


class Ui_ExperimentControl(QtWidgets.QWidget):

    def __init__(self):
        super(Ui_ExperimentControl, self).__init__()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # Microscope settings widget
        self.microscopeSettings = scopeSettings.Ui_MicroscopeSettings()

        # Camera settings widget
        self.cameraSettings = camSettings.Ui_CameraSettings()

        # Acquisition control widget
        self.acquisitionControl = acqControl.Ui_AcquisitionControl()

        # PALM Acquisition Widget
        self.palmControl = palmAcqControl.Ui_PALMAcquisitionControl()

        self.mainLayout.addWidget(self.microscopeSettings)
        self.mainLayout.addWidget(self.cameraSettings)
        self.mainLayout.addWidget(self.acquisitionControl)
        self.mainLayout.addWidget(self.palmControl)
