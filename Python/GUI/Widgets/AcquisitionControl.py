# -*- coding: utf-8 -*-
"""
This widget allows to run acquisitions and to save images

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import Modules.imageFunctions as imageFunctions
import data

class Ui_AcquisitionControl(QtWidgets.QWidget):
    
    startMovieSignal = QtCore.pyqtSignal()
    stopMovieSignal = QtCore.pyqtSignal()
    takeSnapshotSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        
        self.horizontalLayoutWidget1 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget1.setGeometry(QtCore.QRect(0, 0, 331, 90))
        self.horizontalLayoutWidget1.setObjectName("horizontalLayoutWidget1")
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget1)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        
        self.buttonLive = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonLive.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonLive.setObjectName("buttonLive")
        self.buttonLive.setText("Live")
        self.horizontalLayout1.addWidget(self.buttonLive)
        
        self.buttonSingleImage = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonSingleImage.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSingleImage.setObjectName("buttonSingleImage")
        self.buttonSingleImage.setText("Single Image")
        self.horizontalLayout1.addWidget(self.buttonSingleImage)
        
        self.buttonStop = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonStop.setObjectName("buttonStop")
        self.buttonStop.setText("Stop")
        self.horizontalLayout1.addWidget(self.buttonStop)
        
        self.horizontalLayoutWidget2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget2.setGeometry(QtCore.QRect(0, 110, 331, 90))
        self.horizontalLayoutWidget2.setObjectName("horizontalLayoutWidget2")
        self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget2)
        self.horizontalLayout2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        
        self.buttonSave = QtWidgets.QPushButton(self.horizontalLayoutWidget2)
        self.buttonSave.setEnabled(True)
        self.buttonSave.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText("Save")
        self.horizontalLayout2.addWidget(self.buttonSave)
        
        self.buttonSingleImage.clicked.connect(self.snapImage)
        self.buttonLive.clicked.connect(self.startMovie)
        self.buttonStop.clicked.connect(self.stopMovie)
        self.buttonSave.clicked.connect(self.saveImage)
        
    @QtCore.pyqtSlot()
    def snapImage(self):
        """Send a signal to the main GUI to take a snapshot
        """
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
        self.stopMovieSignal.emit()
        
    def saveImage(self):
        """Saves a 2d image with automatic naiming and increment saved images counter
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        path = data.savePath + '\\img' + str(data.savedImagesCounter) + '.tif'
        imageFunctions.saveImage2D(data.frame, path)
        data.savedImagesCounter += 1