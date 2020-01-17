# -*- coding: utf-8 -*-
"""
This widget allows to control the settings of the Camera that we need (exposure time and binning) through Micro-Manager
interaction.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import Modules.MM as MM
import data


class Ui_CameraSettings(QtWidgets.QWidget):
    
    # Initialization of the class
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

        self.spinBoxGain = QtWidgets.QSpinBox()

        self.sliderGain = QtWidgets.QSlider()
        self.sliderGain.setOrientation(QtCore.Qt.Horizontal)

        self.labelGain = QtWidgets.QLabel("Gain")

        self.spinBoxEMGain = QtWidgets.QSpinBox()

        self.sliderEMGain = QtWidgets.QSlider()
        self.sliderEMGain.setOrientation(QtCore.Qt.Horizontal)

        self.labelEMGain = QtWidgets.QLabel("EM Gain")
        
        self.labelImageFormat = QtWidgets.QLabel("Image Format")
        
        self.comboImageFormat = QtWidgets.QComboBox()

        self.gridLayout.addWidget(self.labelImageFormat, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.comboImageFormat, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.labelExposure, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.sliderExposure, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.spinBoxExposure, 1, 2, 1, 1)
        if data.isCameraEM:
            self.gridLayout.addWidget(self.labelGain, 2, 0, 1, 1)
            self.gridLayout.addWidget(self.sliderGain, 2, 1, 1, 1)
            self.gridLayout.addWidget(self.spinBoxGain, 2, 2, 1, 1)
            self.initSliderSpinBox(self.sliderGain, self.spinBoxGain, data.limitsGain, MM.getPropertyValue(data.cameraName, 'Gain'), self.setGain)
            self.gridLayout.addWidget(self.labelEMGain, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.sliderEMGain, 3, 1, 1, 1)
            self.gridLayout.addWidget(self.spinBoxEMGain, 3, 2, 1, 1)
            self.initSliderSpinBox(self.sliderEMGain, self.spinBoxEMGain, data.limitsEMGain, MM.getPropertyValue(data.cameraName, 'MultiplierGain'), self.setEMGain)

        self.mainLayout.addWidget(self.groupBoxCameraSettings)
        
        self.initFormats()
        self.initSliderSpinBox(self.sliderExposure, self.spinBoxExposure, data.limitsExposure, MM.getPropertyValue(data.cameraName, 'Exposure'), self.setExposure)
        
    def initFormats(self):
        """
        Initializes the combo box values for the image formats and sets the initial format to the current format (always 1x1).
        """
        for el in data.imageFormats.keys():
            self.comboImageFormat.addItem(el)
        self.setFormat()
        self.comboImageFormat.currentIndexChanged['int'].connect(self.setFormat)
            
    def initSliderSpinBox(self, slider, spinBox, limits, value, function):
        """
        Sets the lower and upper limits a slider/spinBox couple and initializes to a given value.
        :param slider: QtWidgets.QSlider()
        :param spinBox: QtWidgets.QSpinBox()
        :param limits: [str, str]
        :param value: str
        """
        slider.setMinimum(limits[0])
        slider.setMaximum(limits[1])
        slider.setValue(float(value))
        spinBox.setMinimum(limits[0])
        spinBox.setMaximum(limits[1])
        spinBox.setValue(float(value))
        spinBox.valueChanged['int'].connect(slider.setValue)
        slider.valueChanged['int'].connect(spinBox.setValue)
        slider.valueChanged['int'].connect(function)

    def setFormat(self):
        """
        Sets the image format.
        """
        imgFormat = self.comboImageFormat.currentText()
        MM.setPropertyValue(data.cameraName, 'Binning', imgFormat)
        data.binning = int(imgFormat[0])
        data.changedBinning = True
        
    def setExposure(self):
        """
        Sets the exposure time of the camera.
        """
        MM.setPropertyValue(data.cameraName, 'Exposure', float(self.sliderExposure.value()))
        data.waitTime = MM.cameraAcquisitionTime()

    def setEMGain(self):
        """
        Sets the EMGain of the camera.
        """
        MM.setPropertyValue(data.cameraName, 'MultiplierGain', float(self.sliderEMGain.value()))

    def setGain(self):
        """
        Sets the Gain of the camera.
        """
        MM.setPropertyValue(data.cameraName, 'Gain', float(self.sliderEMGain.value()))