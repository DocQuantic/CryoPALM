# -*- coding: utf-8 -*-
"""
This widget allows to run the AutoFocus functionality of the main program

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import data

class Ui_AutoFocus(QtWidgets.QWidget):
    
    runAFSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def __init__(self):
        super(Ui_AutoFocus, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        
        self.groupBoxAF = QtWidgets.QGroupBox()
        self.groupBoxAF.setObjectName("groupBoxAF")
        self.groupBoxAF.setTitle("AutoFocus")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxAF)

        self.gridLayoutAF = QtWidgets.QGridLayout()
        
        self.labelStepNumber = QtWidgets.QLabel("Step number")
        
        self.spinBoxStepNumber = QtWidgets.QSpinBox()
        self.spinBoxStepNumber.setMaximum(1000)
        self.spinBoxStepNumber.setValue(data.AFSteps)
        
        self.spinBoxZRange = QtWidgets.QSpinBox()
        self.spinBoxZRange.setMaximum(1000)
        self.spinBoxZRange.setValue(data.AFRange)
        
        self.labelZRange = QtWidgets.QLabel("Z range (µm)")
        
        self.spinBoxStepSize = QtWidgets.QDoubleSpinBox()
        self.spinBoxStepSize.setReadOnly(True)
        self.spinBoxStepSize.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxStepSize.setMaximum(1000.0)
        self.spinBoxStepSize.setValue(data.AFStepSize)
        
        self.labelStepSize = QtWidgets.QLabel("Step Size (µm)")

        self.gridLayoutAF.addWidget(self.labelZRange, 0, 0, 1, 1)
        self.gridLayoutAF.addWidget(self.spinBoxZRange, 0, 1, 1, 1)
        self.gridLayoutAF.addWidget(self.labelStepNumber, 1, 0, 1, 1)
        self.gridLayoutAF.addWidget(self.spinBoxStepNumber, 1, 1, 1, 1)
        self.gridLayoutAF.addWidget(self.labelStepSize, 2, 0, 1, 1)
        self.gridLayoutAF.addWidget(self.spinBoxStepSize, 2, 1, 1, 1)

        self.pushButtonFindFocus = QtWidgets.QPushButton("Find Focus")
        self.pushButtonFindFocus.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButtonFindFocus.setMaximumSize(QtCore.QSize(200, 50))

        self.horizontalLayout.addLayout(self.gridLayoutAF)
        self.horizontalLayout.addWidget(self.pushButtonFindFocus)

        self.mainLayout.addWidget(self.groupBoxAF)

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