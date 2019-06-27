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
    def __init__(self):
        super(Ui_AcquisitionControl, self).__init__()

        self.mainLayout = QtWidgets.QGridLayout(self)

        self.buttonLive = QtWidgets.QPushButton("Live")
        self.buttonLive.setMinimumSize(QtCore.QSize(100, 50))
        self.buttonLive.setMaximumSize(QtCore.QSize(200, 50))

        self.buttonSingleImage = QtWidgets.QPushButton("Single Image")
        self.buttonSingleImage.setMinimumSize(QtCore.QSize(100, 50))
        self.buttonSingleImage.setMaximumSize(QtCore.QSize(200, 50))

        self.buttonStop = QtWidgets.QPushButton("Stop")
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(100, 50))
        self.buttonStop.setMaximumSize(QtCore.QSize(500, 50))

        self.buttonSetROI = QtWidgets.QPushButton("Center Quad")
        self.buttonSetROI.setMinimumSize(QtCore.QSize(100, 30))
        self.buttonSetROI.setMaximumSize(QtCore.QSize(200, 50))

        self.mainLayout.addWidget(self.buttonLive, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.buttonSingleImage, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.buttonStop, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.buttonSetROI, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        
        self.buttonSingleImage.clicked.connect(self.snapImage)
        self.buttonLive.clicked.connect(self.startMovie)
        self.buttonStop.clicked.connect(self.stopMovie)
        
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