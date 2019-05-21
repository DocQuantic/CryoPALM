# -*- coding: utf-8 -*-
"""
This widget allows to run PALM acquisition

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import Modules.imageFunctions as imageFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.fileUtility as fileUtility
import data

class Ui_PALMAcquisitionControl(QtWidgets.QWidget):
    
    runSinglePALMSignal = QtCore.pyqtSignal()
    runSequencePALMSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox(Form)
        self.groupBoxPALMAcquisition.setGeometry(QtCore.QRect(0, 0, 441, 181))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxPALMAcquisition.setFont(font)
        self.groupBoxPALMAcquisition.setObjectName("groupBoxPALMAcquisition")
        self.groupBoxPALMAcquisition.setTitle("PALM Acquisition")
        
        self.pushButtonAcquirePALM = QtWidgets.QPushButton(self.groupBoxPALMAcquisition)
        self.pushButtonAcquirePALM.setGeometry(QtCore.QRect(310, 36, 111, 51))
        self.pushButtonAcquirePALM.setObjectName("pushButtonAcquirePALM")
        self.pushButtonAcquirePALM.setText("Single")
        
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
        
        self.labelFile = QtWidgets.QLabel(self.groupBoxPALMAcquisition)
        self.labelFile.setGeometry(QtCore.QRect(20, 90, 91, 16))
        self.labelFile.setObjectName("labelFile")
        self.labelFile.setText("SerialEM file")
        
        self.filePath = QtWidgets.QLineEdit(self.groupBoxPALMAcquisition)
        self.filePath.setGeometry(QtCore.QRect(20, 110, 261, 20))
        self.filePath.setObjectName("filePath")
        
        self.pushButtonAcquirePALMSequence = QtWidgets.QPushButton(self.groupBoxPALMAcquisition)
        self.pushButtonAcquirePALMSequence.setGeometry(QtCore.QRect(310, 100, 111, 51))
        self.pushButtonAcquirePALMSequence.setObjectName("pushButtonAcquirePALMSequence")
        self.pushButtonAcquirePALMSequence.setText("Sequence")
        
        self.pushButtonBrowse = QtWidgets.QPushButton(self.groupBoxPALMAcquisition)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(20, 140, 111, 21))
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.pushButtonBrowse.setText("Browse...")
        
        self.pushButtonAcquirePALM.clicked.connect(self.runPALM)
        self.pushButtonAcquirePALMSequence.clicked.connect(self.runPALMSequence)
        self.pushButtonBrowse.clicked.connect(self.selectFile)
        
    def selectFile(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open SerialEM Navigation file", "./", "Navigation (*.xml)")[0]
        if path != "":
            self.filePath.setText(path)
        
    @QtCore.pyqtSlot()
    def runPALMSequence(self):
        data.filePath = self.filePath.text()
        if data.filePath != "":
            data.stagePos = fileUtility.readFileSerialEM(data.filePath)
            if data.stagePos != 0:
                self.runSequencePALMSignal.emit()            
        
    @QtCore.pyqtSlot()
    def runPALM(self):
        """Send a signal to the main GUI to run PALM acquisition
        """
        self.runSinglePALMSignal.emit()
        
def saveStack():
    """Saves a 3d image stack with automatic naiming and increment saved stacks counter
    """            
    path = data.savePath + '\\stack' + str(data.savedStacksCounter) + '.tif'
    imageFunctions.saveImageStack(data.palmStack, path)
    data.savedStacksCounter += 1