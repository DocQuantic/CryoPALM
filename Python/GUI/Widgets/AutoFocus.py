# -*- coding: utf-8 -*-
"""
This widget allows to run the AutoFocus functionnality of the main program

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.imageFunctions as imageFunctions
import data

class Ui_AutoFocus(QtWidgets.QWidget):
    
    runAFSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        
        self.groupBoxAF = QtWidgets.QGroupBox(Form)
        self.groupBoxAF.setGeometry(QtCore.QRect(0, 0, 401, 221))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxAF.setFont(font)
        self.groupBoxAF.setObjectName("groupBoxAF")
        self.groupBoxAF.setTitle("AutoFocus")
        
        self.pushButtonFindFocus = QtWidgets.QPushButton(self.groupBoxAF)
        self.pushButtonFindFocus.setGeometry(QtCore.QRect(250, 40, 101, 51))
        self.pushButtonFindFocus.setObjectName("pushButtonFindFocus")
        self.pushButtonFindFocus.setText("Find Focus")
        
        self.gridLayoutWidgetAF = QtWidgets.QWidget(self.groupBoxAF)
        self.gridLayoutWidgetAF.setGeometry(QtCore.QRect(20, 40, 191, 141))
        self.gridLayoutWidgetAF.setObjectName("gridLayoutWidgetAF")
        self.gridLayoutAF = QtWidgets.QGridLayout(self.gridLayoutWidgetAF)
        self.gridLayoutAF.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutAF.setObjectName("gridLayoutAF")
        
        self.labelStepNumber = QtWidgets.QLabel(self.gridLayoutWidgetAF)
        self.labelStepNumber.setObjectName("labelStepNumber")
        self.labelStepNumber.setText("Step number")
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
        self.labelZRange.setText("Z range (µm)")
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
        self.labelStepSize.setText("Step Size (µm)")
        self.gridLayoutAF.addWidget(self.labelStepSize, 2, 0, 1, 1)
        
        
        self.spinBoxZRange.valueChanged['int'].connect(self.updateAFParam)
        self.spinBoxStepNumber.valueChanged['int'].connect(self.updateAFParam)
        self.pushButtonFindFocus.clicked.connect(self.runAF)
        
    def updateAFParam(self):
        """Sets the AF parameters in the data file
        """
        data.AFRange = self.spinBoxZRange.value()
        data.AFSteps = self.spinBoxStepNumber.value()
        data.AFStepSize = data.AFRange/data.AFSteps
        self.spinBoxStepSize.setValue(data.AFStepSize)
        
    @QtCore.pyqtSlot()
    def runAF(self):
        """Send a signal to the main GUI to run the auto focus
        """
        self.runAFSignal.emit()