# -*- coding: utf-8 -*-
"""
This widget allows to run PALM acquisitions.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import GUI.Widgets.batchPopUp as batchPopUp
import Modules.fileUtility as fileUtility
import datetime
import data


class Ui_PALMAcquisitionControl(QtWidgets.QWidget):
    
    runSinglePALMSignal = QtCore.pyqtSignal()
    runBatchSignal = QtCore.pyqtSignal()
    stopSinglePALMSignal = QtCore.pyqtSignal()
    runSequencePALMSignal = QtCore.pyqtSignal()
    
    # Initialization of the class
    def __init__(self):
        super(Ui_PALMAcquisitionControl, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.line1 = QtWidgets.QFrame()
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)

        # self.line2 = QtWidgets.QFrame()
        # self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox()
        self.groupBoxPALMAcquisition.setTitle("PALM Acquisition")

        self.layoutPALM = QtWidgets.QVBoxLayout(self.groupBoxPALMAcquisition)

        self.verticalLayoutPALMSimple = QtWidgets.QVBoxLayout()

        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout()

        self.labelImageNumber = QtWidgets.QLabel("Image number")

        self.spinBoxImageNumber = QtWidgets.QSpinBox()
        self.spinBoxImageNumber.setMaximum(10000)
        self.spinBoxImageNumber.setValue(200)

        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)

        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()

        self.pushButtonAcquirePALMSingle = QtWidgets.QPushButton("Start")
        self.pushButtonAcquirePALMSingle.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMSingle.setMaximumSize(QtCore.QSize(200, 16777215))

        self.pushButtonAcquirePALMBatch = QtWidgets.QPushButton("Batch")
        self.pushButtonAcquirePALMBatch.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMBatch.setMaximumSize(QtCore.QSize(200, 16777215))

        self.pushButtonStopPALMSingle = QtWidgets.QPushButton("Cancel")
        self.pushButtonStopPALMSingle.setEnabled(False)
        self.pushButtonStopPALMSingle.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonStopPALMSingle.setMaximumSize(QtCore.QSize(200, 16777215))

        self.horizontalLayoutButtons.addWidget(self.pushButtonAcquirePALMSingle)
        self.horizontalLayoutButtons.addWidget(self.pushButtonAcquirePALMBatch)
        self.horizontalLayoutButtons.addWidget(self.pushButtonStopPALMSingle)

        self.verticalLayoutPALMSimple.addLayout(self.horizontalLayoutPALM)
        self.verticalLayoutPALMSimple.addLayout(self.horizontalLayoutButtons)

        # self.verticalLayoutPALMCLEM = QtWidgets.QVBoxLayout()
        #
        # self.labelFile = QtWidgets.QLabel("SerialEM file:")
        #
        # self.filePath = QtWidgets.QLineEdit(data.savePath)
        #
        # self.pushButtonBrowse = QtWidgets.QPushButton("Browse...")
        #
        # self.pushButtonAcquirePALMSequence = QtWidgets.QPushButton("Acquire Serial EM Sequence")
        # self.pushButtonAcquirePALMSequence.setMinimumSize(QtCore.QSize(0, 50))
        # self.pushButtonAcquirePALMSequence.setMaximumSize(QtCore.QSize(200, 16777215))
        #
        # self.verticalLayoutPALMCLEM.addWidget(self.labelFile)
        # self.verticalLayoutPALMCLEM.addWidget(self.filePath)
        # self.verticalLayoutPALMCLEM.addWidget(self.pushButtonBrowse)
        # self.verticalLayoutPALMCLEM.addWidget(self.pushButtonAcquirePALMSequence, 0, QtCore.Qt.AlignHCenter)

        self.horizontalLayoutProgress = QtWidgets.QHBoxLayout()

        self.labelProgress = QtWidgets.QLabel("Status: Idle")

        self.horizontalLayoutProgress.addWidget(self.labelProgress)

        self.layoutPALM.addLayout(self.verticalLayoutPALMSimple)
        self.layoutPALM.addWidget(self.line1)
        # self.layoutPALM.addLayout(self.verticalLayoutPALMCLEM)
        # self.layoutPALM.addWidget(self.line2)
        self.layoutPALM.addLayout(self.horizontalLayoutProgress)

        self.mainLayout.addWidget(self.groupBoxPALMAcquisition)

        self.popUp = batchPopUp.Ui_BatchPopUp()
        
        self.pushButtonAcquirePALMSingle.clicked.connect(self.runPALM)
        self.pushButtonAcquirePALMBatch.clicked.connect(self.openPopUp)
        self.pushButtonStopPALMSingle.clicked.connect(self.stopPALM)
        # self.pushButtonAcquirePALMSequence.clicked.connect(self.runPALMSequence)
        # self.pushButtonBrowse.clicked.connect(self.selectFile)
        
    def selectFile(self):
        """
        Opens a navigation window to elect am xml file to open containing interest positions (not implemented yet).
        """
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open SerialEM Navigation file", data.savePath, "Navigation (*.xml)")[0]
        if path != "":
            self.filePath.setText(path)

    @QtCore.pyqtSlot()
    def runPALM(self):
        """
        Sends a signal to the main GUI to run PALM acquisition.
        """
        data.acquisitionTime = datetime.datetime.now()
        self.runSinglePALMSignal.emit()

    def openPopUp(self):
        """
        Opens batch configuration pop up window.
        """
        self.popUp.show()

    @QtCore.pyqtSlot()
    def runBatch(self, maxNumber):
        """
        Sends a signal to run the batch acquisition.
        :param maxNumber: int
        """
        self.runBatchSignal.emit(maxNumber)

    @QtCore.pyqtSlot()
    def stopPALM(self):
        """
        Sends a signal to stop the PALM acquisiion.
        """
        self.stopSinglePALMSignal.emit()
        
    @QtCore.pyqtSlot()
    def runPALMSequence(self):
        """
        Send a signal to the main GUI to run PALM acquisition sequence at each position that was spotted on LAS X and exported to Serial EM (not implemented yet).
        """
        data.filePath = self.filePath.text()
        if data.filePath != "":
            data.stagePos = fileUtility.readFileSerialEM(data.filePath)
            if data.stagePos != 0:
                data.acquisitionTime = datetime.datetime.now()
                self.runSequencePALMSignal.emit()

    def setProgress(self, status):
        """
        Updates the status of the PALM Acquisition.
        """
        self.labelProgress.setText(status)
