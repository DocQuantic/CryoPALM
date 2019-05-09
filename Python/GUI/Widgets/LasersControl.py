# -*- coding: utf-8 -*-
"""
This widget allows to control the laser bench from Roper containing:
    -1 488 nm laser modulated by AOTF
    -1 561 nm laser modulated by AOTF
    -1 405 nm laser controlled directly
via an Arduino board

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.arduinoComm as arduinoComm

class Ui_LasersControl(QtWidgets.QWidget):
    
    def setupUi(self, Form):
        self.groupBoxLasersSettings = QtWidgets.QGroupBox(Form)
        self.groupBoxLasersSettings.setGeometry(QtCore.QRect(0, 0, 561, 271))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxLasersSettings.setFont(font)
        self.groupBoxLasersSettings.setObjectName("groupBoxLasersSettings")
        self.groupBoxLasersSettings.setTitle("Lasers Settings")
        
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
        self.label405.setText("405 nm")
        self.gridLayoutLasersSetting.addWidget(self.label405, 0, 0, 1, 1)
        
        self.label488 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label488.setObjectName("label488")
        self.label488.setText("488 nm")
        self.gridLayoutLasersSetting.addWidget(self.label488, 0, 1, 1, 1)
        
        self.label561 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label561.setObjectName("label561")
        self.label561.setText("561 nm")
        self.gridLayoutLasersSetting.addWidget(self.label561, 0, 2, 1, 1)
        
        self.pushButtonBlank = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButtonBlank.setGeometry(QtCore.QRect(290, 30, 111, 51))
        self.pushButtonBlank.setObjectName("pushButtonBlank")
        self.pushButtonBlank.setCheckable(True)
        self.pushButtonBlank.setChecked(True)
        self.pushButtonBlank.setText("Blank")
        
        self.pushButton405 = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButton405.setGeometry(QtCore.QRect(290, 101, 111, 51))
        self.pushButton405.setObjectName("pushButton405")
        self.pushButton405.setCheckable(True)
        self.pushButton405.setText("405 On/Off")
        
        self.pushButtonShutter = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButtonShutter.setGeometry(QtCore.QRect(290, 172, 111, 51))
        self.pushButtonShutter.setObjectName("pushButton405")
        self.pushButtonShutter.setCheckable(True)
        self.pushButtonShutter.setChecked(True)
        self.pushButtonShutter.setText("Shutter")
        
        self.slider405.sliderMoved['int'].connect(self.set405)
        self.slider488.sliderMoved['int'].connect(self.set488)
        self.slider561.sliderMoved['int'].connect(self.set561)
        self.pushButtonBlank.clicked.connect(self.blankOutputs)
        self.pushButton405.clicked.connect(self.switch405)
        self.pushButtonShutter.clicked.connect(self.switchShutter)
        
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