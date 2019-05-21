# -*- coding: utf-8 -*-
"""
This file contains the main UI code 
Form implementation generated from reading ui file 'guiMain.ui'

Created on Fri Mar 29 09:54:55 2019
Created with PyQt5 UI code generator 5.9.2

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.PALMAcquisitionControl as palmAcqControl
import GUI.Widgets.MicroscopeSettings as scopeSettings
import GUI.Widgets.imageViewerGUI as imageViewerGUI
import GUI.Widgets.AcquisitionControl as acqControl
import GUI.Widgets.CameraSettings as camSettings
import Modules.imageFunctions as imageFunctions
import GUI.Widgets.LasersControl as lasControl
import GUI.Widgets.movieThread as movieThread
from PyQt5 import QtCore, QtWidgets, QtTest
import GUI.Widgets.histPlot as histPlot
import GUI.Widgets.AutoFocus as AF
from pyqtgraph import ImageView
from scipy import ndimage
import Modules.MM as MM
import numpy as np
import data

class Ui_MainWindow(object):
        
    def setupUi(self, MainWindow):
        """Setups all the elements positions and connectionss with functions
        In the future, this part will be divided in different Widgets for code simplicity
        """
        MainWindow.setObjectName("Cryo PALM")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Microscope settings widget
        self.microscopeSettingsWidget = QtWidgets.QWidget(self.centralwidget)
        self.microscopeSettingsWidget.setGeometry(QtCore.QRect(70, 80, 410, 271))
        self.microscopeSettings = scopeSettings.Ui_MicroscopeSettings()
        self.microscopeSettings.setupUi(self.microscopeSettingsWidget)
        
        #Camera settings widget
        self.cameraSettingsWidget = QtWidgets.QWidget(self.centralwidget)
        self.cameraSettingsWidget.setGeometry(QtCore.QRect(70, 380, 410, 230))
        self.cameraSettings = camSettings.Ui_CameraSettings()
        self.cameraSettings.setupUi(self.cameraSettingsWidget)
        
        #Acquisition control widget
        self.acquisitionControlWidget = QtWidgets.QWidget(self.centralwidget)
        self.acquisitionControlWidget.setGeometry(QtCore.QRect(110, 640, 331, 200))
        self.acquisitionControl = acqControl.Ui_AcquisitionControl()
        self.acquisitionControl.setupUi(self.acquisitionControlWidget)
        
        #Auto-focus Widget
        self.autoFocusWidget = QtWidgets.QWidget(self.centralwidget)
        self.autoFocusWidget.setGeometry(QtCore.QRect(80, 880, 401, 221))
        self.autoFocus = AF.Ui_AutoFocus()
        self.autoFocus.setupUi(self.autoFocusWidget)
        
        #Image viewer widget
        self.imageViewerWidget = QtWidgets.QWidget(self.centralwidget)
        self.imageViewerWidget.setGeometry(QtCore.QRect(550, 20, 1300, 1400))
        self.imageViewer = imageViewerGUI.Ui_ImageViewer()
        self.imageViewer.setupUi(self.imageViewerWidget)
        
        self.movieAcq = movieThread.MovieThread(self.imageViewer)
        self.movieAcq.loop.connect(self.showMovie)
        
        #Histogram plot widget
        self.histPlotter = histPlot.Ui_HistPlot()
        
        self.verticalLayoutWidgetHist = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidgetHist.setGeometry(QtCore.QRect(500, 1300, 1250, 150))
        self.verticalLayoutWidgetHist.setObjectName("verticalLayoutWidgetHist")
        self.verticalLayoutHist = QtWidgets.QHBoxLayout(self.verticalLayoutWidgetHist)
        self.verticalLayoutHist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHist.setObjectName("verticalLayoutHist")
        
        self.verticalLayoutHist.addWidget(self.histPlotter)
        
        #Lasers control Widget
        self.lasersControlWidget = QtWidgets.QWidget(self.centralwidget)
        self.lasersControlWidget.setGeometry(QtCore.QRect(1800, 80, 561, 271))
        self.lasersControl = lasControl.Ui_LasersControl()
        self.lasersControl.setupUi(self.lasersControlWidget)
        
        #PALM Acquisition Widget
        self.sequencePalmThread = movieThread.SequencePALMThread(self.imageViewer)
        self.palmThread = movieThread.PALMThread(self.imageViewer)
        self.palmControlWidget = QtWidgets.QWidget(self.centralwidget)
        self.palmControlWidget.setGeometry(QtCore.QRect(1800, 390, 441, 181))
        self.palmControl = palmAcqControl.Ui_PALMAcquisitionControl()
        self.palmControl.setupUi(self.palmControlWidget)
        
        #Main window configuration
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1390, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowTitle("Cryo PALM")
        
        self.palmControl.runSequencePALMSignal.connect(self.runPALMSequence)
        self.palmControl.runSinglePALMSignal.connect(self.runPALM)
        self.palmThread.showFrame.connect(self.showMovie)
        self.palmThread.stopPALM.connect(self.stopPALMAcq)
        self.sequencePalmThread.showFrame.connect(self.showMovie)
        self.sequencePalmThread.stopPALM.connect(self.stopPALMAcq)
        self.acquisitionControl.takeSnapshotSignal.connect(self.snapImage)
        self.acquisitionControl.startMovieSignal.connect(self.startMovie)
        self.acquisitionControl.stopMovieSignal.connect(self.stopMovie)
        self.autoFocus.runAFSignal.connect(self.runAF)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def snapImage(self):
        """Takes a snapshot, convert to a pixmap, display it in the display window and compute and display the histogram.
        """
            
        frame = MM.snapImage()
        data.frame = frame
        imgPixmap = imageFunctions.array2Pixmap(frame)
        y, x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 10000))
        self.histPlotter.updateHist(x, y)
        self.imageViewer.displayWindow.setImage(imgPixmap)
        
    def showMovie(self, frame, x, y):
        """Displays the image sent by the movie thread and its histogram
        """
        if frame is not None and frame.width() != 0:
            self.histPlotter.updateHist(x, y)
            self.imageViewer.displayWindow.setImage(frame)
        else:
            return
        
    def startMovie(self):
        """Start live acquisition via a thread
        """
        if data.canSetROI:
            data.canSetROI = False
            
        self.acquisitionControl.buttonStop.setEnabled(True)
        self.acquisitionControl.buttonLive.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(False)
        self.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.autoFocus.pushButtonFindFocus.setEnabled(False)
        self.imageViewer.pushButtonSetROI.setEnabled(False)
        
        MM.startAcquisition()
        
        self.movieAcq.setTerminationEnabled(True)
        self.movieAcq.start()
        
    def stopMovie(self):
        """Stops the movie thread and the acquisition
        """
        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonStop.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)
        
        self.movieAcq.terminate()
        
        MM.stopAcquisition()
        
    def runPALMSequence(self):
        """Runs the PALM acquisition sequence via a thread
        """
        print("start PALM Sequence")
        imageNumber = self.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:
            MM.setROI(896, 896, 256, 256)
            data.changedBinning = True
            if data.canSetROI:
                data.canSetROI = False
            if data.canZoom:
                data.canZoom = False
                
            self.acquisitionControl.buttonStop.setEnabled(False)
            self.acquisitionControl.buttonLive.setEnabled(False)
            self.acquisitionControl.buttonSave.setEnabled(False)
            self.acquisitionControl.buttonSingleImage.setEnabled(False)
            self.autoFocus.pushButtonFindFocus.setEnabled(False)
            self.imageViewer.pushButtonSetROI.setEnabled(False)
            self.imageViewer.pushButtonZoom.setEnabled(False)
            
            self.sequencePalmThread.imageNumber = imageNumber
            MM.startAcquisition()
            self.sequencePalmThread.start()
                    
        
    def runPALM(self):
        """Runs the PALM acquisition via a thread
        """
        imageNumber = self.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:
            MM.setROI(896, 896, 256, 256)
            data.changedBinning = True
            if data.canSetROI:
                data.canSetROI = False
            if data.canZoom:
                data.canZoom = False
                
            self.acquisitionControl.buttonStop.setEnabled(False)
            self.acquisitionControl.buttonLive.setEnabled(False)
            self.acquisitionControl.buttonSave.setEnabled(False)
            self.acquisitionControl.buttonSingleImage.setEnabled(False)
            self.autoFocus.pushButtonFindFocus.setEnabled(False)
            self.imageViewer.pushButtonSetROI.setEnabled(False)
            self.imageViewer.pushButtonZoom.setEnabled(False)
            
            self.palmThread.imageNumber = imageNumber
            MM.startAcquisition()
            self.palmThread.start()
            
    def stopPALMAcq(self):
        """Stops the PALM thread, display the last image of the stack and its histogram, save the stack and set the ROI baack to full chip
        """
        print("Stop Acquisition")
        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonStop.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)
        self.imageViewer.pushButtonZoom.setEnabled(True)
        
        MM.stopAcquisition()
        imgPixmap = imageFunctions.array2Pixmap(data.palmStack[-1,:,:])
        y, x = np.histogram(data.palmStack[-1,:,:].ravel(), bins=np.linspace(0, 65535, 10000))
        self.histPlotter.updateHist(x, y)
        self.imageViewer.displayWindow.setImage(imgPixmap)
        
        MM.clearROI()
        data.changedBinning = True
        
    def runAF(self):
        """Runs the auto focus routine
        """
        if data.canSetROI:
            data.canSetROI = False
        if data.canZoom:
            data.canZoom = False
            
        self.acquisitionControl.buttonStop.setEnabled(False)
        self.acquisitionControl.buttonLive.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(False)
        self.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.autoFocus.pushButtonFindFocus.setEnabled(False)
        self.imageViewer.pushButtonSetROI.setEnabled(False)
        
        currentZPos = MM.getZPos()
        data.AFZPos = np.arange(currentZPos-data.AFRange/2.0, currentZPos+data.AFRange/2.0, data.AFStepSize)
        
        data.varStack = []
        data.AFStack = []
        idx = 0
        for step in data.AFZPos:
            MM.setZPos(step)
            QtTest.QTest.qWait(500)
            
            frame =  MM.snapImage()
            data.AFStack.append(frame)
            idx += 1
            edgedFrame = ndimage.sobel(frame)
            var = ndimage.variance(edgedFrame)
            data.varStack.append(var)
            imgPixmap = imageFunctions.array2Pixmap(frame)
            y, x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 1000))
            self.histPlotter.updateHist(x, y)
            self.imageViewer.displayWindow.setImage(imgPixmap)
            QtTest.QTest.qWait(100)
            
        idxMax = np.argmin(data.varStack)
        bestFocus = data.AFZPos[idxMax]
        MM.setZPos(bestFocus)
        QtTest.QTest.qWait(100)
        self.snapImage()
        
        self.acquisitionControl.buttonStop.setEnabled(True)
        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)
