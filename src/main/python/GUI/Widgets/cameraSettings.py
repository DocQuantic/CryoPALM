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

        self.comboGain = QtWidgets.QComboBox()
        self.labelGain = QtWidgets.QLabel("Gain")

        self.comboExposeMode = QtWidgets.QComboBox()
        self.labelExposeMode = QtWidgets.QLabel("Expose Mode")

        self.comboRate = QtWidgets.QComboBox()
        self.labelRate = QtWidgets.QLabel("Readout Rate")

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

        if data.cameraName == data.primeName:
            data.rates = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'ReadoutRate')
            self.gridLayout.addWidget(self.labelRate, 2, 0, 1, 1)
            self.gridLayout.addWidget(self.comboRate, 2, 1, 1, 1)
            self.initRate()

            data.gains = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'Gain')
            self.gridLayout.addWidget(self.labelGain, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.comboGain, 3, 1, 1, 1)
            self.initGain()

            data.exposeModes = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'ExposeOutMode')
            self.gridLayout.addWidget(self.labelExposeMode, 4, 0, 1, 1)
            self.gridLayout.addWidget(self.comboExposeMode, 4, 1, 1, 1)
            self.initExposeMode()
        elif data.cameraName == data.evolveName:
            data.gains = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'Gain')
            self.gridLayout.addWidget(self.labelGain, 2, 0, 1, 1)
            self.gridLayout.addWidget(self.comboGain, 2, 1, 1, 1)
            self.initGain()

            self.gridLayout.addWidget(self.labelEMGain, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.sliderEMGain, 3, 1, 1, 1)
            self.gridLayout.addWidget(self.spinBoxEMGain, 3, 2, 1, 1)
            self.initSliderSpinBox(self.sliderEMGain, self.spinBoxEMGain, data.limitsEMGain, MM.getPropertyValue(data.cameraDeviceName, 'MultiplierGain'), self.setEMGain)


        self.mainLayout.addWidget(self.groupBoxCameraSettings)
        
        self.initFormats()
        self.initSliderSpinBox(self.sliderExposure, self.spinBoxExposure, data.limitsExposure, MM.getPropertyValue(data.cameraDeviceName, 'Exposure'), self.setExposure)

    def initGain(self):
        """
        Initializes the combo box values for the gain settings and sets the initial gain to the current gain.
        """
        for el in data.gains.keys():
            self.comboGain.addItem(el)
        self.setGain()
        self.comboGain.currentIndexChanged['int'].connect(self.setGain)

    def initExposeMode(self):
        """
        Initializes the combo box values for the expose mode settings and sets the initial expose mode to the current one.
        """
        for el in data.exposeModes.keys():
            self.comboExposeMode.addItem(el)
        self.setExposeMode()
        self.comboExposeMode.currentIndexChanged['int'].connect(self.setExposeMode)

    def initRate(self):
        """
        Initializes the combo box values for the readout rate settings and sets the initial readout rate to the current one.
        """
        for el in data.rates.keys():
            self.comboRate.addItem(el)
        self.setRate()
        self.comboRate.currentIndexChanged['int'].connect(self.setRate)

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
        spinBox.editingFinished.connect(function)
        slider.valueChanged['int'].connect(spinBox.setValue)

    def setFormat(self):
        """
        Sets the image format.
        """
        imgFormat = self.comboImageFormat.currentText()
        MM.setPropertyValue(data.cameraDeviceName, 'Binning', imgFormat)
        data.binning = int(imgFormat[0])
        data.changedBinning = True
        
    def setExposure(self):
        """
        Sets the exposure time of the camera.
        """
        MM.setPropertyValue(data.cameraDeviceName, 'Exposure', float(self.sliderExposure.value()))
        data.waitTime = MM.cameraAcquisitionTime()

    def setEMGain(self):
        """
        Sets the EMGain of the camera (only for evolve camera).
        """
        MM.setPropertyValue(data.cameraDeviceName, 'MultiplierGain', float(self.sliderEMGain.value()))

    def setGain(self):
        """
        Sets the Gain of the camera.
        """
        gain = self.comboGain.currentText()
        MM.setPropertyValue(data.cameraDeviceName, 'Gain', gain)

    def setExposeMode(self):
        """
        Sets the Expose Mode of the camera (only for prime camera).
        """
        exposeMode = self.comboExposeMode.currentText()
        MM.setPropertyValue(data.cameraDeviceName, 'ExposeOutMode', exposeMode)

    def setRate(self):
        """
        Sets the Readout Rate of the camera (only for prime camera).
        """
        rate = self.comboRate.currentText()
        MM.setPropertyValue(data.cameraDeviceName, 'ReadoutRate', rate)
        if rate=='200MHz 12bit':
            data.bitDepth = 12
        elif rate == '100MHz 16bit':
            data.bitDepth = 16

        try:
            self.comboGain.currentIndexChanged['int'].disconnect()
        except TypeError:
            pass

        self.comboGain.clear()
        data.gains = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'Gain')
        for el in data.gains.keys():
            self.comboGain.addItem(el)

        self.setGain()
        self.comboGain.currentIndexChanged['int'].connect(self.setGain)