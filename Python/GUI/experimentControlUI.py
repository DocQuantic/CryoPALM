# -*- coding: utf-8 -*-
"""
This file contains the UI code for the experiment control window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 25 14:11:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.PALMAcquisitionControl as palmAcqControl
import GUI.Widgets.MicroscopeSettings as scopeSettings
import GUI.Widgets.AcquisitionControl as acqControl
import GUI.Widgets.CameraSettings as camSettings
from PyQt5 import QtCore, QtWidgets, QtGui, QtTest
import data

class Ui_ExperimentControl(QtWidgets.QWidget):

    def __init__(self):
        """Setups all the elements positions and connections with functions
        """
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

        #PALM Acquisition Widget
        self.palmControl = palmAcqControl.Ui_PALMAcquisitionControl()

        self.mainLayout.addWidget(self.microscopeSettings)
        self.mainLayout.addWidget(self.cameraSettings)
        self.mainLayout.addWidget(self.acquisitionControl)
        self.mainLayout.addWidget(self.palmControl)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_ExperimentControl()
    ExperimentControl.show()
    app.exec_()