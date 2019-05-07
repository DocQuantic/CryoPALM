# -*- coding: utf-8 -*-
"""
This file contains the main UI code 
Form implementation generated from reading ui file 'guiMain.ui'

Created on Fri Mar 29 09:54:55 2019
Created with PyQt5 UI code generator 5.9.2

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from pyqtgraph import ImageView
from scipy import ndimage
import imageViewerGUI
import imageFunctions
import arduinoComm
import movieThread
import numpy as np
import histPlot
import data
import MM

class Ui_MainWindow(object):
        
    def setupUi(self, MainWindow):
        """Setups all the elements positions and connectionss with functions
        In the future, this part will be divided in different Widgets for code simplicity
        """
        MainWindow.setObjectName("Cryo PALM")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        #Image viewer widget
        self.imageViewer = imageViewerGUI.Ui_ImageViewer()
        self.movieAcq = movieThread.MovieThread(self.imageViewer)
        
        self.horizontalLayoutWidgetImage = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidgetImage.setGeometry(QtCore.QRect(550, 20, 1200, 1200))
        self.horizontalLayoutWidgetImage.setObjectName("horizontalLayoutWidgetImage")
        self.horizontalLayoutImage = QtWidgets.QHBoxLayout(self.horizontalLayoutWidgetImage)
        self.horizontalLayoutImage.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutImage.setObjectName("horizontalLayoutImage")
        
        self.horizontalLayoutImage.addWidget(self.imageViewer)
        
        self.pushButtonZoom = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonZoom.setGeometry(QtCore.QRect(940, 1250, 71, 31))
        self.pushButtonZoom.setObjectName("pushButtonZoom")
        self.pushButtonZoom.setCheckable(True)
        self.pushButtonZoom.setChecked(False)
        self.pushButtonSetROI = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSetROI.setGeometry(QtCore.QRect(1020, 1250, 71, 31))
        self.pushButtonSetROI.setObjectName("pushButtonSetROI")
        self.pushButtonSetROI.setCheckable(True)
        self.pushButtonSetROI.setChecked(False)
        
        #Acquisition control widget
        self.horizontalLayoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget1.setGeometry(QtCore.QRect(110, 640, 331, 90))
        self.horizontalLayoutWidget1.setObjectName("horizontalLayoutWidget1")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget1)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        
        self.buttonLive = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonLive.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonLive.setObjectName("buttonLive")
        self.horizontalLayout1.addWidget(self.buttonLive)
        
        self.buttonSingleImage = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonSingleImage.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSingleImage.setObjectName("buttonSingleImage")
        self.horizontalLayout1.addWidget(self.buttonSingleImage)
        
        self.buttonStop = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonStop.setObjectName("buttonStop")
        self.horizontalLayout1.addWidget(self.buttonStop)
        
        self.horizontalLayoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget2.setGeometry(QtCore.QRect(110, 750, 331, 90))
        self.horizontalLayoutWidget2.setObjectName("horizontalLayoutWidget2")
        self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget2)
        self.horizontalLayout2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        
        self.buttonSave = QtWidgets.QPushButton(self.horizontalLayoutWidget2)
        self.buttonSave.setEnabled(True)
        self.buttonSave.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSave.setObjectName("buttonSave")
        self.horizontalLayout2.addWidget(self.buttonSave)
        
        #Histogram plot widget
        self.histPlotter = histPlot.Ui_HistPlot()
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 80, 410, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.verticalLayoutWidgetHist = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidgetHist.setGeometry(QtCore.QRect(500, 1300, 1250, 150))
        self.verticalLayoutWidgetHist.setObjectName("verticalLayoutWidgetHist")
        self.verticalLayoutHist = QtWidgets.QHBoxLayout(self.verticalLayoutWidgetHist)
        self.verticalLayoutHist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHist.setObjectName("verticalLayoutHist")
        
        self.verticalLayoutHist.addWidget(self.histPlotter)
        
        #Microscope settings tabs
        self.labelMicroscopeSettings = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(14)
        self.labelMicroscopeSettings.setFont(font)
        self.labelMicroscopeSettings.setObjectName("labelMicroscopeSettings")
        self.verticalLayout.addWidget(self.labelMicroscopeSettings)
        
        self.tabWidgetMethod = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.tabWidgetMethod.setFont(font)
        self.tabWidgetMethod.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidgetMethod.setObjectName("tabWidgetMethod")
        self.tabWidgetMethod.setCurrentIndex(0)
        self.TLBF = QtWidgets.QWidget()
        self.TLBF.setObjectName("TLBF")
        self.gridLayoutWidget = QtWidgets.QWidget(self.TLBF)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(12, 10, 371, 201))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.sliderApertureBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderApertureBF.setStyleSheet("color: rgb(170, 170, 255);")
        self.sliderApertureBF.setSingleStep(0)
        self.sliderApertureBF.setProperty("value", 0)
        self.sliderApertureBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderApertureBF.setObjectName("sliderApertureBF")
        self.gridLayout.addWidget(self.sliderApertureBF, 1, 1, 1, 1)
        self.spinBoxFieldBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxFieldBF.setMinimumSize(QtCore.QSize(70, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxFieldBF.setFont(font)
        self.spinBoxFieldBF.setObjectName("spinBoxFieldBF")
        self.gridLayout.addWidget(self.spinBoxFieldBF, 2, 2, 1, 1)
        self.labelShutterBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelShutterBF.setFont(font)
        self.labelShutterBF.setObjectName("labelShutterBF")
        self.gridLayout.addWidget(self.labelShutterBF, 3, 0, 1, 1)
        self.buttonShutterBF = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonShutterBF.setFont(font)
        self.buttonShutterBF.setObjectName("buttonShutterBF")
        self.buttonShutterBF.setCheckable(True)
        self.gridLayout.addWidget(self.buttonShutterBF, 3, 1, 1, 1)
        self.labelApertureBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelApertureBF.setFont(font)
        self.labelApertureBF.setObjectName("labelApertureBF")
        self.gridLayout.addWidget(self.labelApertureBF, 1, 0, 1, 1)
        self.sliderIntensityBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderIntensityBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderIntensityBF.setObjectName("sliderIntensityBF")
        self.gridLayout.addWidget(self.sliderIntensityBF, 0, 1, 1, 1)
        self.labelIntensityBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelIntensityBF.setFont(font)
        self.labelIntensityBF.setObjectName("labelIntensityBF")
        self.gridLayout.addWidget(self.labelIntensityBF, 0, 0, 1, 1)
        self.spinBoxApertureBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxApertureBF.setMinimumSize(QtCore.QSize(70, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxApertureBF.setFont(font)
        self.spinBoxApertureBF.setObjectName("spinBoxApertureBF")
        self.gridLayout.addWidget(self.spinBoxApertureBF, 1, 2, 1, 1)
        self.labelLight = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelLight.setFont(font)
        self.labelLight.setObjectName("labelLight")
        self.gridLayout.addWidget(self.labelLight, 4, 0, 1, 1)
        self.labelFieldBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFieldBF.setFont(font)
        self.labelFieldBF.setObjectName("labelFieldBF")
        self.gridLayout.addWidget(self.labelFieldBF, 2, 0, 1, 1)
        self.sliderFieldBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderFieldBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderFieldBF.setObjectName("sliderFieldBF")
        self.gridLayout.addWidget(self.sliderFieldBF, 2, 1, 1, 1)
        self.spinBoxIntensityBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxIntensityBF.setEnabled(True)
        self.spinBoxIntensityBF.setMinimumSize(QtCore.QSize(70, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxIntensityBF.setFont(font)
        self.spinBoxIntensityBF.setObjectName("spinBoxIntensityBF")
        self.gridLayout.addWidget(self.spinBoxIntensityBF, 0, 2, 1, 1)
        self.buttonLightState = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonLightState.setFont(font)
        self.buttonLightState.setObjectName("buttonLightState")
        self.buttonLightState.setCheckable(True)
        self.gridLayout.addWidget(self.buttonLightState, 4, 1, 1, 1)
        self.labelLightState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLightState.setObjectName("labelLightState")
        self.gridLayout.addWidget(self.labelLightState, 4, 2, 1, 1)
        self.labelShutterBFState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelShutterBFState.setObjectName("labelShutterBFState")
        self.gridLayout.addWidget(self.labelShutterBFState, 3, 2, 1, 1)
        self.tabWidgetMethod.addTab(self.TLBF, "")
        self.FLUO = QtWidgets.QWidget()
        self.FLUO.setObjectName("FLUO")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.FLUO)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 50, 371, 111))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelShutterIL = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelShutterIL.setFont(font)
        self.labelShutterIL.setObjectName("labelShutterIL")
        self.gridLayout_2.addWidget(self.labelShutterIL, 0, 0, 1, 1)
        self.buttonShutterIL = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.buttonShutterIL.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonShutterIL.setFont(font)
        self.buttonShutterIL.setObjectName("buttonShutterIL")
        self.buttonShutterIL.setCheckable(True)
        self.gridLayout_2.addWidget(self.buttonShutterIL, 0, 1, 1, 1)
        self.LabelFilter = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LabelFilter.setFont(font)
        self.LabelFilter.setObjectName("LabelFilter")
        self.gridLayout_2.addWidget(self.LabelFilter, 1, 0, 1, 1)
        self.comboFilter = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboFilter.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboFilter.setFont(font)
        self.comboFilter.setObjectName("comboFilter")
        self.gridLayout_2.addWidget(self.comboFilter, 1, 1, 1, 1)
        self.labelShutterILState = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelShutterILState.setObjectName("labelShutterILState")
        self.gridLayout_2.addWidget(self.labelShutterILState, 0, 2, 1, 1)
        self.tabWidgetMethod.addTab(self.FLUO, "")
        self.verticalLayout.addWidget(self.tabWidgetMethod)
        
        #Camera settings widget
        self.groupBoxCameraSettings = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxCameraSettings.setGeometry(QtCore.QRect(70, 380, 410, 230))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxCameraSettings.setFont(font)
        self.groupBoxCameraSettings.setStyleSheet("")
        self.groupBoxCameraSettings.setObjectName("groupBoxCameraSettings")
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
        self.gridLayout_3.addWidget(self.labelExposure, 1, 0, 1, 1)
        self.labelImageFormat = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.labelImageFormat.setObjectName("labelImageFormat")
        self.gridLayout_3.addWidget(self.labelImageFormat, 0, 0, 1, 1)
        self.comboImageFormat = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboImageFormat.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboImageFormat.setObjectName("comboImageFormat")
        self.gridLayout_3.addWidget(self.comboImageFormat, 0, 1, 1, 1)
        
        #Lasers control Widget
        self.groupBoxLasersSettings = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxLasersSettings.setGeometry(QtCore.QRect(1800, 80, 561, 271))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxLasersSettings.setFont(font)
        self.groupBoxLasersSettings.setObjectName("groupBoxLasersSettings")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxLasersSettings)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(19, 29, 231, 221))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayoutLasersSetting = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayoutLasersSetting.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLasersSetting.setObjectName("gridLayoutLasersSetting")
        self.slider561 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider561.setMinimumSize(QtCore.QSize(40, 0))
        self.slider561.setAutoFillBackground(False)
        self.slider561.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.slider561.setMaximum(255)
        self.slider561.setOrientation(QtCore.Qt.Vertical)
        self.slider561.setInvertedAppearance(False)
        self.slider561.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider561.setTickInterval(10)
        self.slider561.setObjectName("slider561")
        self.gridLayoutLasersSetting.addWidget(self.slider561, 1, 2, 1, 1)
        self.slider488 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider488.setMinimumSize(QtCore.QSize(40, 0))
        self.slider488.setAutoFillBackground(False)
        self.slider488.setStyleSheet("background-color: rgb(85, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.slider488.setMaximum(255)
        self.slider488.setOrientation(QtCore.Qt.Vertical)
        self.slider488.setInvertedAppearance(False)
        self.slider488.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider488.setTickInterval(10)
        self.slider488.setObjectName("slider488")
        self.gridLayoutLasersSetting.addWidget(self.slider488, 1, 1, 1, 1)
        self.slider405 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider405.setMinimumSize(QtCore.QSize(40, 0))
        self.slider405.setAutoFillBackground(False)
        self.slider405.setStyleSheet("background-color: rgb(85, 0, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.slider405.setMaximum(255)
        self.slider405.setOrientation(QtCore.Qt.Vertical)
        self.slider405.setInvertedAppearance(False)
        self.slider405.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider405.setTickInterval(10)
        self.slider405.setObjectName("slider405")
        self.gridLayoutLasersSetting.addWidget(self.slider405, 1, 0, 1, 1)
        self.label405 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label405.setObjectName("label405")
        self.gridLayoutLasersSetting.addWidget(self.label405, 0, 0, 1, 1)
        self.label488 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label488.setObjectName("label488")
        self.gridLayoutLasersSetting.addWidget(self.label488, 0, 1, 1, 1)
        self.label561 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label561.setObjectName("label561")
        self.gridLayoutLasersSetting.addWidget(self.label561, 0, 2, 1, 1)
        self.pushButtonBlank = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButtonBlank.setGeometry(QtCore.QRect(290, 30, 111, 51))
        self.pushButtonBlank.setObjectName("pushButtonBlank")
        self.pushButtonBlank.setCheckable(True)
        self.pushButtonBlank.setChecked(True)
        self.pushButton405 = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButton405.setGeometry(QtCore.QRect(290, 101, 111, 51))
        self.pushButton405.setObjectName("pushButton405")
        self.pushButton405.setCheckable(True)
        self.pushButtonShutter = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButtonShutter.setGeometry(QtCore.QRect(290, 172, 111, 51))
        self.pushButtonShutter.setObjectName("pushButton405")
        self.pushButtonShutter.setCheckable(True)
        self.pushButtonShutter.setChecked(True)
        
        #Auto-focus Widget
        self.groupBoxAF = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxAF.setGeometry(QtCore.QRect(80, 880, 401, 221))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxAF.setFont(font)
        self.groupBoxAF.setObjectName("groupBoxAF")
        self.pushButtonFindFocus = QtWidgets.QPushButton(self.groupBoxAF)
        self.pushButtonFindFocus.setGeometry(QtCore.QRect(250, 40, 101, 51))
        self.pushButtonFindFocus.setObjectName("pushButtonFindFocus")
        self.gridLayoutWidgetAF = QtWidgets.QWidget(self.groupBoxAF)
        self.gridLayoutWidgetAF.setGeometry(QtCore.QRect(20, 40, 191, 141))
        self.gridLayoutWidgetAF.setObjectName("gridLayoutWidgetAF")
        self.gridLayoutAF = QtWidgets.QGridLayout(self.gridLayoutWidgetAF)
        self.gridLayoutAF.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutAF.setObjectName("gridLayoutAF")
        self.labelStepNumber = QtWidgets.QLabel(self.gridLayoutWidgetAF)
        self.labelStepNumber.setObjectName("labelStepNumber")
        self.gridLayoutAF.addWidget(self.labelStepNumber, 1, 0, 1, 1)
        self.spinBoxStepNumber = QtWidgets.QSpinBox(self.gridLayoutWidgetAF)
        self.spinBoxStepNumber.setObjectName("spinBoxStepNumber")
        self.spinBoxStepNumber.setMaximum(1000)
        self.spinBoxStepNumber.setValue(data.AFSteps)
        self.gridLayoutAF.addWidget(self.spinBoxStepNumber, 1, 1, 1, 1)
        self.spinBoxZRange = QtWidgets.QSpinBox(self.gridLayoutWidgetAF)
        self.spinBoxZRange.setObjectName("spinBoxZRange")
        self.spinBoxZRange.setMaximum(1000)
        self.spinBoxZRange.setValue(data.AFRange)
        self.gridLayoutAF.addWidget(self.spinBoxZRange, 0, 1, 1, 1)
        self.labelZRange = QtWidgets.QLabel(self.gridLayoutWidgetAF)
        self.labelZRange.setObjectName("labelZRange")
        self.gridLayoutAF.addWidget(self.labelZRange, 0, 0, 1, 1)
        self.spinBoxStepSize = QtWidgets.QDoubleSpinBox(self.gridLayoutWidgetAF)
        self.spinBoxStepSize.setObjectName("spinBoxStepSize")
        self.spinBoxStepSize.setReadOnly(True)
        self.spinBoxStepSize.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxStepSize.setMaximum(1000.0)
        self.spinBoxStepSize.setValue(data.AFStepSize)
        self.gridLayoutAF.addWidget(self.spinBoxStepSize, 2, 1, 1, 1)
        self.labelStepSize = QtWidgets.QLabel(self.gridLayoutWidgetAF)
        self.labelStepSize.setObjectName("labelStepSize")
        self.gridLayoutAF.addWidget(self.labelStepSize, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        #PALM Acquisition Widget
        self.palmAcq = movieThread.PALMThread(self.imageViewer)
        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxPALMAcquisition.setGeometry(QtCore.QRect(1800, 390, 441, 101))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxPALMAcquisition.setFont(font)
        self.groupBoxPALMAcquisition.setObjectName("groupBoxPALMAcquisition")
        self.pushButtonAcquirePALM = QtWidgets.QPushButton(self.groupBoxPALMAcquisition)
        self.pushButtonAcquirePALM.setGeometry(QtCore.QRect(310, 36, 111, 51))
        self.pushButtonAcquirePALM.setObjectName("pushButtonAcquirePALM")
        self.horizontalLayoutWidgetPALM = QtWidgets.QWidget(self.groupBoxPALMAcquisition)
        self.horizontalLayoutWidgetPALM.setGeometry(QtCore.QRect(20, 40, 261, 41))
        self.horizontalLayoutWidgetPALM.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout(self.horizontalLayoutWidgetPALM)
        self.horizontalLayoutPALM.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutPALM.setObjectName("horizontalLayoutPALM")
        self.labelImageNumber = QtWidgets.QLabel(self.horizontalLayoutWidgetPALM)
        self.labelImageNumber.setObjectName("labelImageNumber")
        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)
        self.spinBoxImageNumber = QtWidgets.QSpinBox(self.horizontalLayoutWidgetPALM)
        self.spinBoxImageNumber.setObjectName("spinBoxImageNumber")
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)
        self.spinBoxImageNumber.setMaximum(100000)
        
        #Main window configuration
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1390, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        self.sliderFieldBF.sliderMoved['int'].connect(self.spinBoxFieldBF.setValue)
        self.spinBoxApertureBF.valueChanged['int'].connect(self.sliderApertureBF.setValue)
        self.spinBoxIntensityBF.valueChanged['int'].connect(self.sliderIntensityBF.setValue)
        self.spinBoxFieldBF.valueChanged['int'].connect(self.sliderFieldBF.setValue)
        self.sliderIntensityBF.valueChanged['int'].connect(self.spinBoxIntensityBF.setValue)
        self.sliderApertureBF.sliderMoved['int'].connect(self.spinBoxApertureBF.setValue)
        self.spinBoxExposure.valueChanged['int'].connect(self.sliderExposure.setValue)
        self.sliderExposure.valueChanged['int'].connect(self.spinBoxExposure.setValue)
        self.comboImageFormat.currentIndexChanged['int'].connect(self.setFormat)
        self.sliderIntensityBF.sliderReleased.connect(self.setIntensityBF)
        self.sliderApertureBF.sliderReleased.connect(self.setApertureBF)
        self.sliderFieldBF.sliderReleased.connect(self.setFieldBF)
        self.sliderExposure.sliderReleased.connect(self.setExposure)
        self.tabWidgetMethod.currentChanged['int'].connect(self.setMethod)
        self.buttonShutterBF.clicked.connect(self.setShutterTL)
        self.buttonShutterIL.clicked.connect(self.setShutterIL)
        self.buttonLightState.clicked.connect(self.setBFLightState)
        self.buttonSingleImage.clicked.connect(self.snapImage)
        self.buttonLive.clicked.connect(self.startMovie)
        self.buttonStop.clicked.connect(self.stopMovie)
        self.slider405.sliderMoved['int'].connect(self.set405)
        self.slider488.sliderMoved['int'].connect(self.set488)
        self.slider561.sliderMoved['int'].connect(self.set561)
        self.pushButtonBlank.clicked.connect(self.blankOutputs)
        self.pushButton405.clicked.connect(self.switch405)
        self.pushButtonShutter.clicked.connect(self.switchShutter)
        self.buttonSave.clicked.connect(self.saveImage)
        self.spinBoxZRange.valueChanged['int'].connect(self.updateAFParam)
        self.spinBoxStepNumber.valueChanged['int'].connect(self.updateAFParam)
        self.pushButtonFindFocus.clicked.connect(self.runAF)
        self.pushButtonZoom.clicked.connect(self.handleZoom)
        self.pushButtonSetROI.clicked.connect(self.setROI)
        self.pushButtonAcquirePALM.clicked.connect(self.runPALM)
        
        self.movieAcq.loop.connect(self.showMovie)
        self.palmAcq.showFrame.connect(self.showMovie)
        self.palmAcq.stopPALM.connect(self.stopPALMAcq)
#        self.imageViewer.leftMouseButtonDoubleClicked.connect(self.mousePressEvent)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def handleZoom(self):
        """Sets the zoom on the image window active or inactive.
        """
        if self.pushButtonZoom.isChecked():
            data.canZoom=True
            if self.pushButtonSetROI.isChecked():
                self.pushButtonSetROI.setCheked(False)
                data.canSetROI=False
        else:
            data.canZoom=False
            
    def setROI(self):
        """Sets the ROI of the camera.
        If active, the ROI is set to a 256x256 pixels square area centered on the camera chip.
        When deactivated, it is set back to full chip.
        """
        if self.pushButtonSetROI.isChecked():
            data.canSetROI=True
            if self.pushButtonZoom.isChecked():
                self.pushButtonZoom.setChecked(False)
                data.canZoom=False
            MM.setROI(896, 896, 256, 256)
        else:
            data.canSetROI=False
            MM.clearROI()
        
    ###### DM6000 functions ######
    def initFilters(self):
        """Initializes the combo box values for the filters and sets the initial filter to the empty filter.
        """
        for el in data.filters.keys():
            self.comboFilter.addItem(el)
        self.comboFilter.setCurrentIndex(3)
        self.comboFilter.currentIndexChanged['int'].connect(self.setFilter)
        
    def initFormats(self):
        """Initializes the combo box values for the image formats and sets the initial format to the current format (always 1x1).
        """
        for el in data.imageFormats.keys():
            self.comboImageFormat.addItem(el)
        self.setFormat()
        
    def initMethod(self):
        """Initializes the method to BF
        """
        MM.setPropertyValue('Scope', 'Method', 'TL BF')
        
    def initIntensity(self, limits, value):
        """Sets the lower and upper limits for the BF intensity and initializes to the current value
        :type limits: [str, str]
        :type value: str
        """
        self.sliderIntensityBF.setMinimum(limits[0])
        self.sliderIntensityBF.setMaximum(limits[1])
        self.sliderIntensityBF.setValue(int(value))
        self.spinBoxIntensityBF.setMinimum(limits[0])
        self.spinBoxIntensityBF.setMaximum(limits[1])
        self.spinBoxIntensityBF.setValue(int(value))
        
    def initAperture(self, limits, value):
        """Sets the lower and upper limits for the BF aperture diaphragm and initializes to the current value
        :type limits: [str, str]
        :type value: str
        """
        self.sliderApertureBF.setMinimum(limits[0])
        self.sliderApertureBF.setMaximum(limits[1])
        self.sliderApertureBF.setValue(int(value))
        self.spinBoxApertureBF.setMinimum(limits[0])
        self.spinBoxApertureBF.setMaximum(limits[1])
        self.spinBoxApertureBF.setValue(int(value))
        
    def initFieldBF(self, limits, value):
        """Sets the lower and upper limits for the BF field diaphragm and initializes to the current value
        :type limits: [str, str]
        :type value: str
        """
        self.sliderFieldBF.setMinimum(limits[0])
        self.sliderFieldBF.setMaximum(limits[1])
        self.sliderFieldBF.setValue(int(value))
        self.spinBoxFieldBF.setMinimum(limits[0])
        self.spinBoxFieldBF.setMaximum(limits[1])
        self.spinBoxFieldBF.setValue(int(value))
        
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
        
    def initBFLightState(self):
        """Initializes the BF light state to off
        """
        MM.setPropertyValue('Transmitted Light', 'State', '0')
        self.labelLightState.setText('Off')
        
    def initShutterTL(self):
        """Initializes the TL shutter state to closed
        """
        MM.setPropertyValue('TL-Shutter', 'State', '0')
        self.labelShutterBFState.setText('Closed')
        
    def initShutterIL(self):
        """Initializes the IL shutter state to closed
        """
        MM.setPropertyValue('IL-Shutter', 'State', '0')
        self.labelShutterILState.setText('Closed')
        
    def setMethod(self):
        """Sets the method
        """
        tabIndex = self.tabWidgetMethod.currentIndex()
        MM.setPropertyValue('Scope', 'Method', self.tabWidgetMethod.tabText(tabIndex))
        if self.tabWidgetMethod.tabText(tabIndex)=='FLUO':
            self.comboFilter.setCurrentIndex(0)
        elif self.tabWidgetMethod.tabText(tabIndex)=='TL BF':
            self.comboFilter.setCurrentIndex(3)
        
    def setFilter(self):
        """Sets the filter
        """
        MM.setPropertyValue('IL-Turret', 'Label', self.comboFilter.currentText())
        
    def setShutterTL(self):
        """Sets the opening of the TL shutter
        """
        if self.buttonShutterBF.isChecked():
            MM.setPropertyValue('TL-Shutter', 'State', '1')
            self.labelShutterBFState.setText('Opened')
        else:
            MM.setPropertyValue('TL-Shutter', 'State', '0')
            self.labelShutterBFState.setText('Closed')
            
    def setShutterIL(self):
        """Sets the opening of the IL shutter
        """
        if self.buttonShutterIL.isChecked():
            MM.setPropertyValue('IL-Shutter', 'State', '1')
            self.labelShutterILState.setText('Opened')
        else:
            MM.setPropertyValue('IL-Shutter', 'State', '0')
            self.labelShutterILState.setText('Closed')
            
    def setBFLightState(self):
        """Sets the BF light on or off
        """
        if self.buttonLightState.isChecked():
            MM.setPropertyValue('Transmitted Light', 'State', '1')
            self.labelShutterILState.setText('Opened')
        else:
            MM.setPropertyValue('Transmitted Light', 'State', '0')
            self.labelShutterILState.setText('Closed')
        
    def setIntensityBF(self):
        """Sets the Intensity of the BF light
        """
        MM.setPropertyValue('Transmitted Light', 'Level', self.sliderIntensityBF.value())
        
    def setApertureBF(self):
        """Sets the opening of the BF aperture diaphragm
        """
        MM.setPropertyValue('TL-ApertureDiaphragm', 'Position', self.sliderApertureBF.value())
        
    def setFieldBF(self):
        """Sets the opening of the BF field diaphragm
        """
        MM.setPropertyValue('TL-FieldDiaphragm', 'Position', self.sliderFieldBF.value())
        
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
            
    def set405(self):
        """Sets the power of the 405 laser
        """
        arduinoComm.writeChainArduino('0', str(self.slider405.value()))
        
    def set488(self):
        """Sets the power of the 488 laser
        """
        arduinoComm.writeChainArduino('1', str(self.slider488.value()))
        
    def set561(self):
        """Sets the power of the 561 laser
        """
        arduinoComm.writeChainArduino('2', str(self.slider561.value()))
    
    def blankOutputs(self):
        """Blanks the output of the AOTF
        """
        if self.pushButtonBlank.isChecked():
            lasersState = '0'
        else:
            lasersState = '255'
        
        arduinoComm.writeChainArduino('3', lasersState)
        
    def switch405(self):
        """Switch the 405 laser on or off
        """
        if self.pushButton405.isChecked():
            lasersState = '255'
        else:
            lasersState = '0'
        
        arduinoComm.writeChainArduino('4', lasersState)
        
    def switchShutter(self):
        """Sets the opening of the laser shutter
        """
        if self.pushButtonShutter.isChecked():
            shutterState = '0'
        else:
            shutterState = '255'
            
        arduinoComm.writeChainArduino('5', shutterState)
    
    def snapImage(self):
        """Takes a snapshot, convert to a pixmap, display it in the display window and compute and display the histogram.
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        frame = MM.snapImage()
        data.frame = frame
        imgPixmap = imageFunctions.array2Pixmap(frame)
        y, x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 10000))
        self.histPlotter.updateHist(x, y)
        self.imageViewer.setImage(imgPixmap)
        
    def showMovie(self, frame, x, y):
        """Displays the image sent by the movie thread and its histogram
        """
        if frame is not None and frame.width() != 0:
            self.histPlotter.updateHist(x, y)
            self.imageViewer.setImage(frame)
        else:
            return
        
    def startMovie(self):
        """Start live acquisition via a thread
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        self.buttonStop.setEnabled(True)
        self.buttonLive.setEnabled(False)
        self.buttonSave.setEnabled(False)
        self.buttonSingleImage.setEnabled(False)
        self.pushButtonFindFocus.setEnabled(False)
        self.pushButtonSetROI.setEnabled(False)
        
        MM.startAcquisition()
        
        self.movieAcq.setTerminationEnabled(True)
        self.movieAcq.start()
        
    def stopMovie(self):
        """Stops the movie thread and the acquisition
        """
        self.buttonLive.setEnabled(True)
        self.buttonStop.setEnabled(False)
        self.buttonSave.setEnabled(True)
        self.buttonSingleImage.setEnabled(True)
        self.pushButtonFindFocus.setEnabled(True)
        self.pushButtonSetROI.setEnabled(True)
        
        self.movieAcq.terminate()
        
        MM.stopAcquisition()
        
    def runPALM(self):
        """Runs the PALM acquisition sequence via a thread
        """
        imageNumber = self.spinBoxImageNumber.value()
        if imageNumber != 0:
            MM.setROI(896, 896, 256, 256)
            if data.canSetROI:
                data.canSetROI = False
            if data.canZoom:
                data.canZoom = False
                
            self.buttonStop.setEnabled(False)
            self.buttonLive.setEnabled(False)
            self.buttonSave.setEnabled(False)
            self.buttonSingleImage.setEnabled(False)
            self.pushButtonFindFocus.setEnabled(False)
            self.pushButtonSetROI.setEnabled(False)
            
            self.palmAcq.imageNumber = imageNumber
            MM.startAcquisition()
            self.palmAcq.start()
            
    def stopPALMAcq(self):
        """Stops the PALM thread, display the last image of the stack and its histogram, save the stack and set the ROI baack to full chip
        """
        self.buttonLive.setEnabled(True)
        self.buttonStop.setEnabled(False)
        self.buttonSave.setEnabled(True)
        self.buttonSingleImage.setEnabled(True)
        self.pushButtonFindFocus.setEnabled(True)
        self.pushButtonSetROI.setEnabled(True)
        
        MM.stopAcquisition()
        imgPixmap = imageFunctions.array2Pixmap(data.palmStack[-1,:,:])
        y, x = np.histogram(data.palmStack[-1,:,:].ravel(), bins=np.linspace(0, 65535, 10000))
        self.histPlotter.updateHist(x, y)
        self.imageViewer.setImage(imgPixmap)
        
        self.saveStack()
        MM.clearROI()
        
    def saveImage(self):
        """Saves a 2d image with automatic naiming and increment saved images counter
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        path = data.savePath + '\\img' + str(data.savedImagesCounter) + '.tif'
        imageFunctions.saveImage2D(data.frame, path)
        data.savedImagesCounter += 1
        
    def saveStack(self):
        """Saves a 3d image stack with automatic naiming and increment saved stacks counter
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        path = data.savePath + '\\stack' + str(data.savedStacksCounter) + '.tif'
        imageFunctions.saveImageStack(data.palmStack, path)
        data.savedStacksCounter += 1
        
    def updateAFParam(self):
        """Sets the AF parameters in the data file
        """
        data.AFRange = self.spinBoxZRange.value()
        data.AFSteps = self.spinBoxStepNumber.value()
        data.AFStepSize = data.AFRange/data.AFSteps
        self.spinBoxStepSize.setValue(data.AFStepSize)
        
    def runAF(self):
        """Runs the auto focus
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        self.buttonStop.setEnabled(False)
        self.buttonLive.setEnabled(False)
        self.buttonSave.setEnabled(False)
        self.buttonSingleImage.setEnabled(False)
        self.pushButtonFindFocus.setEnabled(False)
        self.pushButtonSetROI.setEnabled(False)
        
        currentZPos = MM.getZPos()
        data.AFZPos = np.arange(currentZPos-data.AFRange/2.0, currentZPos+data.AFRange/2.0, data.AFStepSize)
        
        data.varStack = []
        data.AFStack = []
        idx = 0
        for step in data.AFZPos:
            MM.setZPos(step)
            QtTest.QTest.qWait(500)
            
            frame =  MM.snapImage()
            data.AFStack.append(frame)
            idx += 1
            edgedFrame = ndimage.sobel(frame)
            var = ndimage.variance(edgedFrame)
            data.varStack.append(var)
            imgPixmap = imageFunctions.array2Pixmap(frame)
            y, x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 1000))
            self.histPlotter.updateHist(x, y)
            self.imageViewer.setImage(imgPixmap)
            QtTest.QTest.qWait(100)
            
        idxMax = np.argmin(data.varStack)
        bestFocus = data.AFZPos[idxMax]
        MM.setZPos(bestFocus)
        QtTest.QTest.qWait(100)
        self.snapImage()
        
        self.buttonStop.setEnabled(True)
        self.buttonLive.setEnabled(True)
        self.buttonSave.setEnabled(True)
        self.buttonSingleImage.setEnabled(True)
        self.pushButtonFindFocus.setEnabled(True)
        self.pushButtonSetROI.setEnabled(True)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cryo PALM"))
        self.buttonLive.setText(_translate("MainWindow", "Live"))
        self.buttonSingleImage.setText(_translate("MainWindow", "Single Image"))
        self.buttonStop.setText(_translate("MainWindow", "Stop"))
        self.labelMicroscopeSettings.setText(_translate("MainWindow", "Microscope Settings"))
        self.labelShutterBF.setText(_translate("MainWindow", "Shutter"))
        self.buttonShutterBF.setText(_translate("MainWindow", "TL-Shutter"))
        self.labelApertureBF.setText(_translate("MainWindow", "Aperture"))
        self.labelIntensityBF.setText(_translate("MainWindow", "Intensity"))
        self.labelLight.setText(_translate("MainWindow", "Light"))
        self.labelFieldBF.setText(_translate("MainWindow", "Field"))
        self.buttonLightState.setText(_translate("MainWindow", "State"))
        self.labelLightState.setText(_translate("MainWindow", "Off"))
        self.labelShutterBFState.setText(_translate("MainWindow", "Closed"))
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.TLBF), _translate("MainWindow", "TL BF"))
        self.labelShutterIL.setText(_translate("MainWindow", "Shutter"))
        self.buttonShutterIL.setText(_translate("MainWindow", "IL-Shutter"))
        self.LabelFilter.setText(_translate("MainWindow", "Filter"))
        self.labelShutterILState.setText(_translate("MainWindow", "Closed"))
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.FLUO), _translate("MainWindow", "FLUO"))
        self.groupBoxLasersSettings.setTitle(_translate("MainWindow", "Lasers Settings"))
        self.groupBoxCameraSettings.setTitle(_translate("MainWindow", "Camera Settings"))
        self.label405.setText(_translate("MainWindow", "405 nm"))
        self.label488.setText(_translate("MainWindow", "488 nm"))
        self.label561.setText(_translate("MainWindow", "561 nm"))
        self.labelExposure.setText(_translate("MainWindow", "Exposure [ms]"))
        self.labelImageFormat.setText(_translate("MainWindow", "Image Format"))
        self.pushButtonBlank.setText(_translate("MainWindow", "Blank"))
        self.pushButton405.setText(_translate("MainWindow", "405 On/Off"))
        self.pushButtonShutter.setText(_translate("MainWindow", "Shutter"))
        self.buttonSave.setText(_translate("MainWindow", "Save"))
        self.groupBoxAF.setTitle(_translate("MainWindow", "AutoFocus"))
        self.pushButtonFindFocus.setText(_translate("MainWindow", "Find Focus"))
        self.labelStepNumber.setText(_translate("MainWindow", "Step number"))
        self.labelZRange.setText(_translate("MainWindow", "Z range (µm)"))
        self.labelStepSize.setText(_translate("MainWindow", "Step Size (µm)"))
        self.pushButtonZoom.setText(_translate("MainWindow", "Zoom"))
        self.pushButtonSetROI.setText(_translate("MainWindow", "Set ROI"))
        self.groupBoxPALMAcquisition.setTitle(_translate("MainWindow", "PALM Acquisition"))
        self.pushButtonAcquirePALM.setText(_translate("MainWindow", "Run"))
        self.labelImageNumber.setText(_translate("MainWindow", "Image number"))
