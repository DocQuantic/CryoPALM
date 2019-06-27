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
    
    def __init__(self):
        super(Ui_LasersControl, self).__init__()

        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.gridLayoutLasersSetting = QtWidgets.QGridLayout()
        self.gridLayoutLasersSetting.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLasersSetting.setObjectName("gridLayoutLasersSetting")

        self.label405 = QtWidgets.QLabel()
        self.label405.setText("405 nm")

        self.label488 = QtWidgets.QLabel()
        self.label488.setText("488 nm")

        self.label561 = QtWidgets.QLabel()
        self.label561.setText("561 nm")

        self.slider405 = QtWidgets.QSlider()
        self.slider405.setMinimumSize(QtCore.QSize(40, 200))
        self.slider405.setAutoFillBackground(False)
        self.slider405.setStyleSheet("background-color: rgb(85, 0, 255);\n"
                                     "border-color: rgb(0, 0, 0);\n"
                                     "border-radius: 5px;")
        self.slider405.setMaximum(255)
        self.slider405.setOrientation(QtCore.Qt.Vertical)
        self.slider405.setInvertedAppearance(False)
        self.slider405.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider405.setTickInterval(10)

        self.slider488 = QtWidgets.QSlider()
        self.slider488.setMinimumSize(QtCore.QSize(40, 200))
        self.slider488.setAutoFillBackground(False)
        self.slider488.setStyleSheet("background-color: rgb(85, 255, 255);\n"
                                     "border-color: rgb(0, 0, 0);\n"
                                     "border-radius: 5px;")
        self.slider488.setMaximum(255)
        self.slider488.setOrientation(QtCore.Qt.Vertical)
        self.slider488.setInvertedAppearance(False)
        self.slider488.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider488.setTickInterval(10)
        
        self.slider561 = QtWidgets.QSlider()
        self.slider561.setMinimumSize(QtCore.QSize(40, 200))
        self.slider561.setAutoFillBackground(False)
        self.slider561.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                     "border-color: rgb(0, 0, 0);\n"
                                     "border-radius: 5px;")
        self.slider561.setMaximum(255)
        self.slider561.setOrientation(QtCore.Qt.Vertical)
        self.slider561.setInvertedAppearance(False)
        self.slider561.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider561.setTickInterval(10)
        
        self.spinBox405 = QtWidgets.QSpinBox()
        self.spinBox405.setReadOnly(True)
        self.spinBox405.setMaximum(100)
        self.spinBox405.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        
        self.spinBox488 = QtWidgets.QSpinBox()
        self.spinBox488.setReadOnly(True)
        self.spinBox488.setMaximum(100)
        self.spinBox488.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        
        self.spinBox561 = QtWidgets.QSpinBox()
        self.spinBox561.setReadOnly(True)
        self.spinBox561.setMaximum(100)
        self.spinBox561.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.gridLayoutLasersSetting.addWidget(self.label405, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.label488, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.label561, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.slider405, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.slider488, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.slider561, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.spinBox405, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.spinBox488, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayoutLasersSetting.addWidget(self.spinBox561, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)

        self.buttonsLayout = QtWidgets.QVBoxLayout()

        self.pushButtonBlank = QtWidgets.QPushButton()
        self.pushButtonBlank.setCheckable(True)
        self.pushButtonBlank.setChecked(True)
        self.pushButtonBlank.setText("Blank")
        self.pushButtonBlank.setMinimumSize(QtCore.QSize(100, 50))
        self.pushButtonBlank.setMaximumSize(QtCore.QSize(200, 50))

        self.pushButton405 = QtWidgets.QPushButton()
        self.pushButton405.setCheckable(True)
        self.pushButton405.setText("405 On/Off")
        self.pushButton405.setMinimumSize(QtCore.QSize(100, 50))
        self.pushButton405.setMaximumSize(QtCore.QSize(200, 50))

        self.pushButtonShutter = QtWidgets.QPushButton()
        self.pushButtonShutter.setCheckable(True)
        self.pushButtonShutter.setChecked(True)
        self.pushButtonShutter.setText("Shutter")
        self.pushButtonShutter.setMinimumSize(QtCore.QSize(100, 50))
        self.pushButtonShutter.setMaximumSize(QtCore.QSize(200, 50))

        self.buttonsLayout.addWidget(self.pushButtonBlank)
        self.buttonsLayout.addWidget(self.pushButton405)
        self.buttonsLayout.addWidget(self.pushButtonShutter)

        self.mainLayout.addLayout(self.gridLayoutLasersSetting)
        self.mainLayout.addLayout(self.buttonsLayout)
        
        self.slider405.valueChanged['int'].connect(self.set405)
        self.slider488.valueChanged['int'].connect(self.set488)
        self.slider561.valueChanged['int'].connect(self.set561)
        self.pushButtonBlank.clicked.connect(self.blankOutputs)
        self.pushButton405.clicked.connect(self.switch405)
        self.pushButtonShutter.clicked.connect(self.switchShutter)
        
    def set405(self):
        """Sets the power of the 405 laser
        """
        arduinoComm.writeChainArduino('0', str(self.slider405.value()))
        self.spinBox405.setValue(self.slider405.value()/255*100)
        
    def set488(self):
        """Sets the power of the 488 laser
        """
        arduinoComm.writeChainArduino('1', str(self.slider488.value()))
        self.spinBox488.setValue(round(self.slider488.value()/255.0*100.0))
        
    def set561(self):
        """Sets the power of the 561 laser
        """
        arduinoComm.writeChainArduino('2', str(self.slider561.value()))
        self.spinBox561.setValue(self.slider561.value()/255*100)
    
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LasersControl = QtWidgets.QWidget()
    ui = Ui_LasersControl()
    ui.setupUi(LasersControl)
    LasersControl.show()
    app.exec_()