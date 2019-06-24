# -*- coding: utf-8 -*-
"""
This widget allows to run PALM acquisition

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import Modules.imageFunctions as imageFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.fileUtility as fileUtility
import datetime
import data

class Ui_PALMAcquisitionControl(QtWidgets.QWidget):
    
    runSinglePALMSignal = QtCore.pyqtSignal()
    runSequencePALMSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox(Form)
        self.groupBoxPALMAcquisition.setGeometry(QtCore.QRect(0, 0, 441, 291))
        self.groupBoxPALMAcquisition.setObjectName("groupBoxPALMAcquisition")
        self.groupBoxPALMAcquisition.setTitle("PALM Acquisition")

        self.verticalLayoutWidgetPALM = QtWidgets.QWidget(self.groupBoxPALMAcquisition)
        self.verticalLayoutWidgetPALM.setGeometry(QtCore.QRect(20, 30, 401, 241))
        self.verticalLayoutWidgetPALM.setObjectName("verticalLayoutWidgetPALM")

        self.layoutPALM = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetPALM)
        self.layoutPALM.setContentsMargins(0, 0, 0, 0)
        self.layoutPALM.setSpacing(20)
        self.layoutPALM.setObjectName("layoutPALM")

        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPALM.setObjectName("horizontalLayoutPALM")

        self.labelImageNumber = QtWidgets.QLabel(self.verticalLayoutWidgetPALM)
        self.labelImageNumber.setObjectName("labelImageNumber")
        self.labelImageNumber.setText("Image number")
        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)

        self.spinBoxImageNumber = QtWidgets.QSpinBox(self.verticalLayoutWidgetPALM)
        self.spinBoxImageNumber.setObjectName("spinBoxImageNumber")
        self.spinBoxImageNumber.setMaximum(10000)
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)

        self.pushButtonAcquirePALMSingle = QtWidgets.QPushButton(self.verticalLayoutWidgetPALM)
        self.pushButtonAcquirePALMSingle.setObjectName("pushButtonAcquirePALMSingle")
        self.pushButtonAcquirePALMSingle.setText("Single")
        self.horizontalLayoutPALM.addWidget(self.pushButtonAcquirePALMSingle)
        self.layoutPALM.addLayout(self.horizontalLayoutPALM)


        self.verticalLayoutPALMCLEM = QtWidgets.QVBoxLayout()
        self.verticalLayoutPALMCLEM.setSpacing(6)
        self.verticalLayoutPALMCLEM.setObjectName("verticalLayoutPALMCLEM")

        self.labelFile = QtWidgets.QLabel(self.verticalLayoutWidgetPALM)
        self.labelFile.setObjectName("labelFile")
        self.verticalLayoutPALMCLEM.addWidget(self.labelFile)

        self.filePath = QtWidgets.QLineEdit(self.verticalLayoutWidgetPALM)
        self.filePath.setObjectName("filePath")
        self.labelFile.setText("SerialEM file:")
        self.verticalLayoutPALMCLEM.addWidget(self.filePath)

        self.pushButtonBrowse = QtWidgets.QPushButton(self.verticalLayoutWidgetPALM)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.pushButtonBrowse.setText("Browse...")
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonBrowse)

        self.pushButtonAcquirePALMSequence = QtWidgets.QPushButton(self.verticalLayoutWidgetPALM)
        self.pushButtonAcquirePALMSequence.setEnabled(True)
        self.pushButtonAcquirePALMSequence.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMSequence.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButtonAcquirePALMSequence.setObjectName("pushButtonAcquirePALMSequence")
        self.pushButtonAcquirePALMSequence.setText("Acquire Serial EM Sequence")
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonAcquirePALMSequence, 0, QtCore.Qt.AlignHCenter)
        self.layoutPALM.addLayout(self.verticalLayoutPALMCLEM)


        self.horizontalLayoutProgress = QtWidgets.QHBoxLayout()
        self.horizontalLayoutProgress.setObjectName("horizontalLayoutProgress")

        self.labelProgress = QtWidgets.QLabel(self.verticalLayoutWidgetPALM)
        self.labelProgress.setObjectName("labelProgress")
        self.labelProgress.setText("Status: Idle")
        self.horizontalLayoutProgress.addWidget(self.labelProgress)
        self.layoutPALM.addLayout(self.horizontalLayoutProgress)
        
        self.pushButtonAcquirePALMSingle.clicked.connect(self.runPALM)
        self.pushButtonAcquirePALMSequence.clicked.connect(self.runPALMSequence)
        self.pushButtonBrowse.clicked.connect(self.selectFile)
        
    def selectFile(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open SerialEM Navigation file", data.savePath, "Navigation (*.xml)")[0]
        if path != "":
            self.filePath.setText(path)
        
    @QtCore.pyqtSlot()
    def runPALMSequence(self):
        """Send a signal to the main GUI to run PALM acquisition
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
        
def saveStack():
    """Saves a 3d image stack with automatic naiming and increment saved stacks counter
    """
    path = data.savePath + '/stack' + str(data.savedStacksCounter) + '.tif'
    imageFunctions.saveImageStack(data.palmStack, path)
    data.savedStacksCounter += 1