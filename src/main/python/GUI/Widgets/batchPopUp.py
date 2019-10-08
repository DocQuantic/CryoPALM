# -*- coding: utf-8 -*-
"""
This widget displays a combo box to choose the max number of batch to run for a PALM batch acquisition.

Created on Thu Jul  4 11:51:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import data


class Ui_BatchPopUp(QtWidgets.QWidget):

    runBatchSignal = QtCore.pyqtSignal(object, object)
    fileName = ""
    
    #Initialization of the class
    def __init__(self):
        super(Ui_BatchPopUp, self).__init__()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.labelFile = QtWidgets.QLabel("File name:")

        self.filePath = QtWidgets.QLineEdit(data.savePath)

        self.pushButtonBrowse = QtWidgets.QPushButton("Browse...")

        self.verticalLayout.addWidget(self.labelFile)
        self.verticalLayout.addWidget(self.filePath)
        self.verticalLayout.addWidget(self.pushButtonBrowse)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        
        self.labelBatchNumber = QtWidgets.QLabel("Batch number")
        
        self.spinBoxBatchNumber = QtWidgets.QSpinBox()
        self.spinBoxBatchNumber.setMaximum(999)
        self.spinBoxBatchNumber.setValue(data.AFSteps)

        self.horizontalLayout.addWidget(self.labelBatchNumber)
        self.horizontalLayout.addWidget(self.spinBoxBatchNumber)

        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()

        self.pushButtonStart = QtWidgets.QPushButton("Start")
        self.pushButtonStart.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButtonStart.setMaximumSize(QtCore.QSize(200, 50))

        self.pushButtonCancel = QtWidgets.QPushButton("Cancel")
        self.pushButtonCancel.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButtonCancel.setMaximumSize(QtCore.QSize(200, 50))

        self.horizontalLayoutButtons.addWidget(self.pushButtonStart)
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)

        self.mainLayout.addLayout(self.verticalLayout)
        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addLayout(self.horizontalLayoutButtons)

        self.setWindowTitle("Maximum batch to acquire")

        self.pushButtonStart.clicked.connect(self.startBatch)
        self.pushButtonCancel.clicked.connect(self.cancel)
        self.pushButtonBrowse.clicked.connect(self.selectFile)

    def selectFile(self):
        """
        Opens a navigation window to select where to save the batch files.
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save As ...", data.savePath, "Image File (*.tif)")[0]
        if path != "":
            self.filePath.setText(path)

        if path != "":
            delimiterPos = [pos for pos, char in enumerate(path) if char == '/']

            if data.savePath != path[0:max(delimiterPos)]:
                data.savePath = path[0:max(delimiterPos)]

            self.fileName = path[max(delimiterPos)+1:-4]

    @QtCore.pyqtSlot()
    def startBatch(self):
        """
        Sends a signal to start the batch acquisition.
        :return:
        """
        if self.spinBoxBatchNumber.value() != 0 and self.filePath.text() is not "":
            self.runBatchSignal.emit(self.spinBoxBatchNumber.value(), self.fileName)
        self.close()

    def cancel(self):
        """
        Closes the batch configuration pop up window.
        """
        self.close()
