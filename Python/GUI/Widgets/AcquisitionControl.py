# -*- coding: utf-8 -*-
"""
This widget allows to run acquisitions and to save images

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets, QtGui
import Modules.imageFunctions as imageFunctions
import data

class Ui_AcquisitionControl(QtWidgets.QWidget):
    
    startMovieSignal = QtCore.pyqtSignal()
    stopMovieSignal = QtCore.pyqtSignal()
    takeSnapshotSignal = QtCore.pyqtSignal()
    
    #Initialization of the class
    def setupUi(self, Form):
        
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)

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
        self.buttonLive.setFont(font)
        self.horizontalLayout.addWidget(self.buttonLive)

        self.buttonSingleImage = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonSingleImage.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSingleImage.setObjectName("buttonSingleImage")
        self.buttonSingleImage.setText("Single Image")
        self.buttonSingleImage.setFont(font)
        self.horizontalLayout.addWidget(self.buttonSingleImage)

        self.buttonStop = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonStop.setObjectName("buttonStop")
        self.buttonStop.setText("Stop")
        self.buttonStop.setFont(font)
        self.horizontalLayout.addWidget(self.buttonStop)

        self.verticalLayout_AcquisitionControl.addLayout(self.horizontalLayout)
        self.buttonSave = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.buttonSave.setMinimumSize(QtCore.QSize(120, 50))
        self.buttonSave.setMaximumSize(QtCore.QSize(150, 16777215))
        self.buttonSave.setObjectName("buttonSave")
        self.buttonSave.setText("Save As ...")
        self.buttonSave.setFont(font)
        self.verticalLayout_AcquisitionControl.addWidget(self.buttonSave, 0, QtCore.Qt.AlignHCenter)
        
        # self.horizontalLayoutWidget1 = QtWidgets.QWidget(Form)
        # self.horizontalLayoutWidget1.setGeometry(QtCore.QRect(0, 0, 331, 90))
        # self.horizontalLayoutWidget1.setObjectName("horizontalLayoutWidget1")
        # self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget1)
        # self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout1.setObjectName("horizontalLayout1")
        #
        # self.buttonLive = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        # self.buttonLive.setMinimumSize(QtCore.QSize(0, 50))
        # self.buttonLive.setObjectName("buttonLive")
        # self.buttonLive.setText("Live")
        # self.buttonLive.setFont(font)
        # self.horizontalLayout1.addWidget(self.buttonLive)
        #
        # self.buttonSingleImage = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        # self.buttonSingleImage.setMinimumSize(QtCore.QSize(0, 50))
        # self.buttonSingleImage.setObjectName("buttonSingleImage")
        # self.buttonSingleImage.setText("Single Image")
        # self.buttonSingleImage.setFont(font)
        # self.horizontalLayout1.addWidget(self.buttonSingleImage)
        #
        # self.buttonStop = QtWidgets.QPushButton(self.horizontalLayoutWidget1)
        # self.buttonStop.setEnabled(False)
        # self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        # self.buttonStop.setObjectName("buttonStop")
        # self.buttonStop.setText("Stop")
        # self.buttonStop.setFont(font)
        # self.horizontalLayout1.addWidget(self.buttonStop)
        #
        # self.horizontalLayoutWidget2 = QtWidgets.QWidget(Form)
        # self.horizontalLayoutWidget2.setGeometry(QtCore.QRect(0, 110, 331, 90))
        # self.horizontalLayoutWidget2.setObjectName("horizontalLayoutWidget2")
        # self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget2)
        # self.horizontalLayout2.setContentsMargins(0, 0, 0, 0)
        # self.horizontalLayout2.setObjectName("horizontalLayout2")
        #
        # self.buttonSave = QtWidgets.QPushButton(self.horizontalLayoutWidget2)
        # self.buttonSave.setEnabled(True)
        # self.buttonSave.setMinimumSize(QtCore.QSize(0, 50))
        # self.buttonSave.setObjectName("buttonSave")
        # self.buttonSave.setText("Save As ...")
        # self.buttonSave.setFont(font)
        # self.horizontalLayout2.addWidget(self.buttonSave)
        
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
        """Saves a 2d image with automatic naming and increment saved images counter
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save As ...", data.savePath, "Image File (*.tif)")[0]
        if path != "":
            delimiterPos = [pos for pos, char in enumerate(path) if char == '/']

            if data.savePath != path[0:max(delimiterPos)]:
                data.savePath = path[0:max(delimiterPos)]

            imageFunctions.saveImage2D(data.frame, path)