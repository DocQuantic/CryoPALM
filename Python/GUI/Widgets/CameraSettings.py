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
    def setupUi(self, Form):
        
        self.groupBoxCameraSettings = QtWidgets.QGroupBox(Form)
        self.groupBoxCameraSettings.setGeometry(QtCore.QRect(0, 0, 410, 230))
        self.groupBoxCameraSettings.setObjectName("groupBoxCameraSettings")
        self.groupBoxCameraSettings.setTitle("Camera Settings")
        
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBoxCameraSettings)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(19, 29, 361, 181))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.spinBoxExposure = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxExposure.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxExposure.setObjectName("spinBoxExposure")
        self.gridLayout_3.addWidget(self.spinBoxExposure, 1, 2, 1, 1)
        
        self.sliderExposure = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.sliderExposure.setOrientation(QtCore.Qt.Horizontal)
        self.sliderExposure.setObjectName("sliderExposure")
        self.gridLayout_3.addWidget(self.sliderExposure, 1, 1, 1, 1)
        
        self.labelExposure = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.labelExposure.setObjectName("labelExposure")
        self.labelExposure.setText("Exposure [ms]")
        self.gridLayout_3.addWidget(self.labelExposure, 1, 0, 1, 1)
        
        self.labelImageFormat = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.labelImageFormat.setObjectName("labelImageFormat")
        self.labelImageFormat.setText("Image Format")
        self.gridLayout_3.addWidget(self.labelImageFormat, 0, 0, 1, 1)
        
        self.comboImageFormat = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboImageFormat.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboImageFormat.setObjectName("comboImageFormat")
        self.gridLayout_3.addWidget(self.comboImageFormat, 0, 1, 1, 1)
        
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
        self.sliderExposure.setMinimum(limits[0])
        self.sliderExposure.setMaximum(limits[1])
        self.sliderExposure.setValue(float(value))
        self.spinBoxExposure.setMinimum(limits[0])
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
        