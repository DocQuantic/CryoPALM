# -*- coding: utf-8 -*-
"""
This widget allows to run acquisitions and to save images.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import datetime
import data


class Ui_AcquisitionControl(QtWidgets.QWidget):
    
    startMovieSignal = QtCore.pyqtSignal()
    stopMovieSignal = QtCore.pyqtSignal()
    takeSnapshotSignal = QtCore.pyqtSignal()
    setROISignal = QtCore.pyqtSignal(object)
    changeQuadSizeSignal = QtCore.pyqtSignal(object)
    
    # Initialization of the class
    def __init__(self):
        super(Ui_AcquisitionControl, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

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

        self.labelXSize = QtWidgets.QLabel("X Size")
        self.labelYSize = QtWidgets.QLabel("Y Size")
        self.spinBoxX = QtWidgets.QSpinBox()
        self.spinBoxX.setMaximum(data.xDim)
        self.spinBoxX.setValue(256)
        self.spinBoxY = QtWidgets.QSpinBox()
        self.spinBoxY.setMaximum(data.yDim)
        self.spinBoxY.setValue(256)

        self.buttonSetROI = QtWidgets.QPushButton("Center Quad")
        self.buttonSetROI.setCheckable(True)
        self.buttonSetROI.setMinimumSize(QtCore.QSize(100, 30))
        self.buttonSetROI.setMaximumSize(QtCore.QSize(200, 50))

        self.mainLayout.addWidget(self.buttonLive, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.buttonSingleImage, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.buttonStop, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.mainLayout.addWidget(self.labelXSize, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.labelYSize, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.spinBoxX, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.spinBoxY, 2, 1, 1, 1)
        self.mainLayout.addWidget(self.buttonSetROI, 1, 2, 2, 1, QtCore.Qt.AlignHCenter)

        self.buttonSingleImage.clicked.connect(self.snapImage)
        self.buttonLive.clicked.connect(self.startMovie)
        self.buttonStop.clicked.connect(self.stopMovie)
        self.buttonSetROI.clicked.connect(self.setROI)
        self.spinBoxX.editingFinished.connect(self.setQuadSize)
        self.spinBoxY.editingFinished.connect(self.setQuadSize)

    @QtCore.pyqtSlot()
    def setROI(self):
        """
        Sends a signal to the main GUI to set the ROI to a center quad.
        """
        self.setROISignal.emit(self.buttonSetROI.isChecked())

    @QtCore.pyqtSlot()
    def setQuadSize(self):
        """
        Sets the size of the center quad in data file.
        """
        data.xSizeQuad = self.spinBoxX.value()
        data.ySizeQuad = self.spinBoxY.value()
        if data.isCenterQuad:
            self.changeQuadSizeSignal.emit(True)

    @QtCore.pyqtSlot()
    def snapImage(self):
        """
        Sends a signal to the main GUI to take a snapshot.
        """
        data.acquisitionTime = datetime.datetime.now()
        self.takeSnapshotSignal.emit()

    @QtCore.pyqtSlot()
    def startMovie(self):
        """
        Send a signal to the main GUI to start live acquisition.
        """
        self.startMovieSignal.emit()

    @QtCore.pyqtSlot()
    def stopMovie(self):
        """
        Send a signal to the main GUI to stop live acquisition.
        """
        data.acquisitionTime = datetime.datetime.now()
        self.stopMovieSignal.emit()
