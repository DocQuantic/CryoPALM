# -*- coding: utf-8 -*-
"""
This widget allows to run acquisitions and to save images

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets, QtGui
import Modules.imageFunctions as imageFunctions
import datetime
import data

class Ui_AcquisitionControl(QtWidgets.QWidget):
    
    startMovieSignal = QtCore.pyqtSignal()
    stopMovieSignal = QtCore.pyqtSignal()
    takeSnapshotSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):

        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 410, 160))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_AcquisitionControl = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_AcquisitionControl.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_AcquisitionControl.setObjectName("verticalLayout_AcquisitionControl")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.buttonLive = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonLive.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonLive.setObjectName("buttonLive")
        self.buttonLive.setText("Live")
        self.horizontalLayout.addWidget(self.buttonLive)

        self.buttonSingleImage = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonSingleImage.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSingleImage.setObjectName("buttonSingleImage")
        self.buttonSingleImage.setText("Single Image")
        self.horizontalLayout.addWidget(self.buttonSingleImage)

        self.buttonStop = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonStop.setObjectName("buttonStop")
        self.buttonStop.setText("Stop")
        self.horizontalLayout.addWidget(self.buttonStop)

        self.verticalLayout_AcquisitionControl.addLayout(self.horizontalLayout)
        self.buttonSave = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonSave.setMinimumSize(QtCore.QSize(120, 50))
        self.buttonSave.setMaximumSize(QtCore.QSize(150, 16777215))
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText("Save As ...")
        self.verticalLayout_AcquisitionControl.addWidget(self.buttonSave, 0, QtCore.Qt.AlignHCenter)
        
        self.buttonSingleImage.clicked.connect(self.snapImage)
        self.buttonLive.clicked.connect(self.startMovie)
        self.buttonStop.clicked.connect(self.stopMovie)
        self.buttonSave.clicked.connect(self.saveImage)
        
    @QtCore.pyqtSlot()
    def snapImage(self):
        """Send a signal to the main GUI to take a snapshot
        """
        data.acquisitionTime = datetime.datetime.now()
        self.takeSnapshotSignal.emit()

    @QtCore.pyqtSlot()
    def startMovie(self):
        """Send a signal to the main GUI to start live acquisition
        """
        self.startMovieSignal.emit()

    @QtCore.pyqtSlot()
    def stopMovie(self):
        """Send a signal to the main GUI to stop live acquisition
        """
        data.acquisitionTime = datetime.datetime.now()
        self.stopMovieSignal.emit()

    def saveImage(self):
        """Saves a 2d image with automatic naming and increment saved images counter
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save As ...", data.savePath, "Image File (*.tif)")[0]
        if path != "":
            delimiterPos = [pos for pos, char in enumerate(path) if char == '/']

            if data.savePath != path[0:max(delimiterPos)]:
                data.savePath = path[0:max(delimiterPos)]

            imageFunctions.saveImage2D(data.frame, path)