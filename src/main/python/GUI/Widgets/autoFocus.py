# -*- coding: utf-8 -*-
"""
This widget allows to run the AutoFocus functionality of the main program.
[TODO: implement other AF functions in order to be able to choose the best one for a specific application.]

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import data


class Ui_AutoFocus(QtWidgets.QWidget):
    
    runAFSignal = QtCore.pyqtSignal()
    
    # Initialization of the class
    def __init__(self):
        super(Ui_AutoFocus, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.comboMethod = QtWidgets.QComboBox()
        self.comboMethod.setMinimumSize(QtCore.QSize(200, 0))

        self.horizontalLayoutAF = QtWidgets.QHBoxLayout()

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

        self.horizontalLayoutAF.addLayout(self.gridLayoutAF)
        self.horizontalLayoutAF.addWidget(self.pushButtonFindFocus)

        self.mainLayout.addWidget(self.comboMethod)
        self.mainLayout.addLayout(self.horizontalLayoutAF)

        self.spinBoxZRange.valueChanged['int'].connect(self.updateAFParam)
        self.spinBoxStepNumber.valueChanged['int'].connect(self.updateAFParam)
        self.pushButtonFindFocus.clicked.connect(self.runAF)

        self.initAFMethods()

    def initAFMethods(self):
        """
        Initializes the AF methods list.
        """
        for el in data.methodsAF.values():
            self.comboMethod.addItem(el)
        self.comboMethod.setCurrentText(data.currentAFMethod)
        self.comboMethod.currentIndexChanged.connect(self.setAFMethod)

    def setAFMethod(self):
        """
        Sets the AF method.
        """
        data.currentAFMethod = data.methodsAF[self.comboMethod.currentIndex()]
        
    def updateAFParam(self):
        """
        Sets the AF parameters in the data file.
        """
        data.AFRange = self.spinBoxZRange.value()
        data.AFSteps = self.spinBoxStepNumber.value()
        data.AFStepSize = data.AFRange/data.AFSteps
        self.spinBoxStepSize.setValue(data.AFStepSize)
        
    @QtCore.pyqtSlot()
    def runAF(self):
        """
        Send a signal to the main GUI to run the auto focus.
        """
        self.runAFSignal.emit()
