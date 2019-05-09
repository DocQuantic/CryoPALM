# -*- coding: utf-8 -*-
"""
This widget allows to run PALM acquisition

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import Modules.imageFunctions as imageFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
import data

class Ui_PALMAcquisitionControl(QtWidgets.QWidget):
    
    runPALMSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox(Form)
        self.groupBoxPALMAcquisition.setGeometry(QtCore.QRect(0, 0, 441, 101))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxPALMAcquisition.setFont(font)
        self.groupBoxPALMAcquisition.setObjectName("groupBoxPALMAcquisition")
        self.groupBoxPALMAcquisition.setTitle("PALM Acquisition")
        
        self.pushButtonAcquirePALM = QtWidgets.QPushButton(self.groupBoxPALMAcquisition)
        self.pushButtonAcquirePALM.setGeometry(QtCore.QRect(310, 36, 111, 51))
        self.pushButtonAcquirePALM.setObjectName("pushButtonAcquirePALM")
        self.pushButtonAcquirePALM.setText("Run")
        
        self.horizontalLayoutWidgetPALM = QtWidgets.QWidget(self.groupBoxPALMAcquisition)
        self.horizontalLayoutWidgetPALM.setGeometry(QtCore.QRect(20, 40, 261, 41))
        self.horizontalLayoutWidgetPALM.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout(self.horizontalLayoutWidgetPALM)
        self.horizontalLayoutPALM.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutPALM.setObjectName("horizontalLayoutPALM")
        
        self.labelImageNumber = QtWidgets.QLabel(self.horizontalLayoutWidgetPALM)
        self.labelImageNumber.setObjectName("labelImageNumber")
        self.labelImageNumber.setText("Image number")
        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)
        
        self.spinBoxImageNumber = QtWidgets.QSpinBox(self.horizontalLayoutWidgetPALM)
        self.spinBoxImageNumber.setObjectName("spinBoxImageNumber")
        self.spinBoxImageNumber.setMaximum(100000)
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)
        
        self.pushButtonAcquirePALM.clicked.connect(self.runPALM)
        
    @QtCore.pyqtSlot()
    def runPALM(self):
        """Send a signal to the main GUI to run PALM acquisition
        """
        self.runPALMSignal.emit()
        
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