# -*- coding: utf-8 -*-
"""
This widget allows to control the settings of the Camera that we need (exposure time and binning) through Micro-Manager interaction

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.MM as MM
import data

class Ui_CameraSettings(QtWidgets.QWidget):
    
    #Initialization of the class
    def __init__(self):
        super(Ui_CameraSettings, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        
        self.groupBoxCameraSettings = QtWidgets.QGroupBox()
        self.groupBoxCameraSettings.setTitle("Camera Settings")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxCameraSettings)
        
        self.spinBoxExposure = QtWidgets.QSpinBox()
        
        self.sliderExposure = QtWidgets.QSlider()
        self.sliderExposure.setOrientation(QtCore.Qt.Horizontal)
        
        self.labelExposure = QtWidgets.QLabel("Exposure [ms]")
        
        self.labelImageFormat = QtWidgets.QLabel("Image Format")
        
        self.comboImageFormat = QtWidgets.QComboBox()

        self.gridLayout.addWidget(self.labelImageFormat, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboImageFormat, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.labelExposure, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.sliderExposure, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.spinBoxExposure, 1, 2, 1, 1)

        self.mainLayout.addWidget(self.groupBoxCameraSettings)
        
        self.initFormats()
        self.initExposure(data.limitsExposure, MM.getPropertyValue('HamamatsuHam_DCAM', 'Exposure'))
        
    def initFormats(self):
        """Initializes the combo box values for the image formats and sets the initial format to the current format (always 1x1).
        """
        for el in data.imageFormats.keys():
            self.comboImageFormat.addItem(el)
        self.setFormat()
        self.comboImageFormat.currentIndexChanged['int'].connect(self.setFormat)
            
    def initExposure(self, limits, value):
        """Sets the lower and upper limits for the exposure and initializes to the current value
        :type limits: [str, str]
        :type value: str
        """
        self.sliderExposure.setMinimum(limits[0]+1)
        self.sliderExposure.setMaximum(limits[1])
        self.sliderExposure.setValue(float(value))
        self.spinBoxExposure.setMinimum(limits[0]+1)
        self.spinBoxExposure.setMaximum(limits[1])
        self.spinBoxExposure.setValue(float(value))
        self.spinBoxExposure.valueChanged['int'].connect(self.sliderExposure.setValue)
        self.sliderExposure.valueChanged['int'].connect(self.spinBoxExposure.setValue)
        self.sliderExposure.valueChanged['int'].connect(self.setExposure)
        
    def setFormat(self):
        """Sets the image format
        """
        imgFormat = self.comboImageFormat.currentText()
        MM.setPropertyValue('HamamatsuHam_DCAM', 'Binning', imgFormat)
        if imgFormat=="1x1":
            data.binning = 1
        elif imgFormat=="2x2":
            data.binning = 2
        else:
            data.binning = 4
        data.changedBinning = True
        
    def setExposure(self):
        """Sets the exposure time of the camera
        """
        MM.setPropertyValue('HamamatsuHam_DCAM', 'Exposure', float(self.sliderExposure.value()))
        data.waitTime = MM.cameraAcquisitionTime()
        
