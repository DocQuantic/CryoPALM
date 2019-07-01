# -*- coding: utf-8 -*-
"""
This widget allows to run PALM acquisitions

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.fileUtility as fileUtility
import datetime
import data

class Ui_PALMAcquisitionControl(QtWidgets.QWidget):
    
    runSinglePALMSignal = QtCore.pyqtSignal()
    runSequencePALMSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def __init__(self):
        super(Ui_PALMAcquisitionControl, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox()
        self.groupBoxPALMAcquisition.setTitle("PALM Acquisition")

        self.layoutPALM = QtWidgets.QVBoxLayout(self.groupBoxPALMAcquisition)
        self.layoutPALM.setSpacing(20)

        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout()

        self.labelImageNumber = QtWidgets.QLabel("Image number")

        self.spinBoxImageNumber = QtWidgets.QSpinBox()
        self.spinBoxImageNumber.setMaximum(10000)

        self.pushButtonAcquirePALMSingle = QtWidgets.QPushButton("Single")
        self.pushButtonAcquirePALMSingle.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMSingle.setMaximumSize(QtCore.QSize(200, 16777215))

        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)
        self.horizontalLayoutPALM.addWidget(self.pushButtonAcquirePALMSingle)

        self.verticalLayoutPALMCLEM = QtWidgets.QVBoxLayout()
        self.verticalLayoutPALMCLEM.setSpacing(6)

        self.labelFile = QtWidgets.QLabel()

        self.filePath = QtWidgets.QLineEdit("SerialEM file:")

        self.pushButtonBrowse = QtWidgets.QPushButton("Browse...")

        self.pushButtonAcquirePALMSequence = QtWidgets.QPushButton("Acquire Serial EM Sequence")
        self.pushButtonAcquirePALMSequence.setEnabled(True)
        self.pushButtonAcquirePALMSequence.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMSequence.setMaximumSize(QtCore.QSize(200, 16777215))

        self.verticalLayoutPALMCLEM.addWidget(self.labelFile)
        self.verticalLayoutPALMCLEM.addWidget(self.filePath)
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonBrowse)
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonAcquirePALMSequence, 0, QtCore.Qt.AlignHCenter)

        self.horizontalLayoutProgress = QtWidgets.QHBoxLayout()

        self.labelProgress = QtWidgets.QLabel("Status: Idle")

        self.horizontalLayoutProgress.addWidget(self.labelProgress)

        self.layoutPALM.addLayout(self.horizontalLayoutPALM)
        self.layoutPALM.addLayout(self.verticalLayoutPALMCLEM)
        self.layoutPALM.addLayout(self.horizontalLayoutProgress)

        self.mainLayout.addWidget(self.groupBoxPALMAcquisition)
        
        self.pushButtonAcquirePALMSingle.clicked.connect(self.runPALM)
        self.pushButtonAcquirePALMSequence.clicked.connect(self.runPALMSequence)
        self.pushButtonBrowse.clicked.connect(self.selectFile)
        
    def selectFile(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open SerialEM Navigation file", data.savePath, "Navigation (*.xml)")[0]
        if path != "":
            self.filePath.setText(path)
        
    @QtCore.pyqtSlot()
    def runPALMSequence(self):
        """Send a signal to the main GUI to run PALM acquisition sequence at each position that was spotted on LAS X and exported to Serial EM
        """
        data.filePath = self.filePath.text()
        if data.filePath != "":
            data.stagePos = fileUtility.readFileSerialEM(data.filePath)
            if data.stagePos != 0:
                data.acquisitionTime = datetime.datetime.now()
                self.runSequencePALMSignal.emit()            
        
    @QtCore.pyqtSlot()
    def runPALM(self):
        """Send a signal to the main GUI to run PALM acquisition
        """
        data.acquisitionTime = datetime.datetime.now()
        self.runSinglePALMSignal.emit()

    def setProgress(self, status):
        """Updates the status of the PALM Acquisition
        """
        self.labelProgress.setText(status)
        
# def saveStack():
#     """Saves a 3d image stack with automatic naiming and increment saved stacks counter
#     """
#     path = data.savePath + '/stack' + str(data.savedStacksCounter) + '.tif'
#     imageFunctions.saveImageStack(data.palmStack, path)
#     data.savedStacksCounter += 1