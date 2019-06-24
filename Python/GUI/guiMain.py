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
from PyQt5 import QtCore, QtWidgets, QtGui, QtTest
import GUI.Widgets.histUI as histUI
import GUI.Widgets.AutoFocus as AF
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
        MainWindow.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                                 "font: 12pt ''Berlin Sans FB'';\n"
                                 "color: rgb(255, 255, 255);\n")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                                         "QPushButton:checked{background-color:rgb(170, 15, 15);}")

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
        self.acquisitionControlWidget.setGeometry(QtCore.QRect(70, 640, 410, 160))
        self.acquisitionControl = acqControl.Ui_AcquisitionControl()
        self.acquisitionControl.setupUi(self.acquisitionControlWidget)

        #Auto-focus Widget
        self.autoFocusWidget = QtWidgets.QWidget(self.centralwidget)
        self.autoFocusWidget.setGeometry(QtCore.QRect(80, 880, 401, 221))
        self.autoFocus = AF.Ui_AutoFocus()
        self.autoFocus.setupUi(self.autoFocusWidget)

        #Image viewer widget
        self.imageViewerWidget = QtWidgets.QWidget(self.centralwidget)
        self.imageViewerWidget.setGeometry(QtCore.QRect(550, 20, 1400, 1400))
        self.imageViewer = imageViewerGUI.Ui_ImageViewer()
        self.imageViewer.setupUi(self.imageViewerWidget)

        self.movieAcq = movieThread.MovieThread(self.imageViewer)
        self.movieAcq.showFrame.connect(self.showFrame)

        #Histogram plot widget
        self.histWidget = QtWidgets.QWidget(self.centralwidget)
        self.histWidget.setGeometry(QtCore.QRect(520, 1250, 1250, 250))
        self.hist = histUI.Ui_Histogram()
        self.hist.setupUi(self.histWidget)

        #Lasers control Widget
        self.lasersControlWidget = QtWidgets.QWidget(self.centralwidget)
        self.lasersControlWidget.setGeometry(QtCore.QRect(1800, 80, 441, 350))
        self.lasersControl = lasControl.Ui_LasersControl()
        self.lasersControl.setupUi(self.lasersControlWidget)

        #PALM Acquisition Widget
        self.sequencePalmThread = movieThread.SequencePALMThread(self.imageViewer)
        self.palmThread = movieThread.PALMThread(self.imageViewer)
        self.palmControlWidget = QtWidgets.QWidget(self.centralwidget)
        self.palmControlWidget.setGeometry(QtCore.QRect(1800, 440, 441, 291))
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
        self.palmThread.showFrame.connect(self.showFrame)
        self.palmThread.stopPALM.connect(self.stopPALMAcq)
        self.palmThread.closeShutter.connect(self.stopAcq)
        self.palmThread.acquisitionState.connect(self.updateAcquisitionState)
        self.sequencePalmThread.showFrame.connect(self.showFrame)
        self.sequencePalmThread.stopPALM.connect(self.stopPALMAcq)
        self.sequencePalmThread.closeShutter.connect(self.stopAcq)
        self.acquisitionControl.takeSnapshotSignal.connect(self.snapImage)
        self.acquisitionControl.startMovieSignal.connect(self.startMovie)
        self.acquisitionControl.stopMovieSignal.connect(self.stopMovie)
        self.autoFocus.runAFSignal.connect(self.runAF)
        self.hist.showFrame.connect(self.showFrame)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def collectMetadata(self):
        lightPath = MM.getPropertyValue('Scope', 'Method')
        if lightPath == 'FLUO':
            acqMode = 'WideField'
            illumType = 'Epifluorescence'
            contrastMethod = 'Fluorescence'
        else:
            acqMode = 'BrightField'
            illumType = 'Transmitted'
            contrastMethod = 'BrightField'

        data.metadata = "<MetaData>\n," \
                        "<prop id=''Description'' type=''string'' value='' ''/>\n" \
                        "<prop id=''MetaDataVersion'' type=''float'' value=''1''/>\n" \
                        "<prop id=''ApplicationName'' type=''string'' value=''CryoPALM''/>\n" \
                        "<prop id=''ApplicationVersion'' type=''string'' value=''1.0''/>\n" \
                        "<PlaneInfo>\n" \
                        "<prop id=''plane-type'' type=''string'' value=''plane''/>\n" \
                        "<prop id=''pixel-size-x'' type=''int'' value=" + str(data.frame.shape[0]) + "/>\n" \
                        "<prop id=''pixel-size-y'' type=''int'' value=" + str(data.frame.shape[1]) + "/>\n" \
                        "<prop id=''bits-per-pixel'' type=''int'' value=''16''/>\n" \
                        "<prop id=''spatial-calibration-x'' type=''float'' value=" + str(data.pixelSize) + "/>\n" \
                        "<prop id=''spatial-calibration-y'' type=''float'' value=" + str(data.pixelSize) + "/>\n" \
                        "<prop id=''spatial-calibration-units'' type=''string'' value=''microns''/>\n" \
                        "<prop id=''gamma'' type=''float'' value=''1''/>\n" \
                        "<prop id=''acquisition-time-local'' type=''time'' value=" + str(data.acquisitionTime) + "/>\n" \
                        "<prop id=''stage-position-x'' type=''float'' value=" + str(MM.getXYPos()[0]) + "/>\n" \
                        "<prop id=''stage-position-y'' type=''float'' value=" + str(MM.getXYPos()[1]) + "/>\n" \
                        "<prop id=''z-position'' type=''float'' value=" + str(MM.getZPos()) + "/>\n" \
                        "<prop id=''wavelength'' type=''float'' value=''0''/>\n" \
                        "<prop id=''camera-binning-x'' type=''int'' value=" + str(data.binning) + "/>\n" \
                        "<prop id=''camera-binning-y'' type=''int'' value=" + str(data.binning) + "/>\n" \
                        "<prop id=''camera-chip-offset-x'' type=''float'' value=''0''/>\n" \
                        "<prop id=''camera-chip-offset-y'' type=''float'' value=''0''/>\n" \
                        "</PlaneInfo>\n" \
                        "<ExperimentInfo>\n" \
                        "<prop id=''objective'' type=''string'' value=''Plan Apo 50x N.A. 0.9 CLEM''/>\n" \
                        "<prop id=''magnification-multiplier'' type=''float'' value=''1.25''/>\n" \
                        "<prop id=''camera-exposure-time'' type=''float'' value=" + str(self.cameraSettings.sliderExposure.value()) + "/>\n" \
                        "<prop id=''light-path'' type=''string'' value=" + str(MM.getPropertyValue('Scope', 'Method')) + "/>\n" \
                        "<prop id=''filter-set'' type=''string'' value=" + str(MM.getPropertyValue('IL-Turret', 'Label')) + "/>\n" \
                        "<prop id=''laser-shutter-state'' type=''string'' value=" + str(self.lasersControl.pushButtonShutter.isChecked()) + "/>\n" \
                        "<prop id=''AOTF-blank-state'' type=''string'' value=" + str(self.lasersControl.pushButtonBlank.isChecked()) + "/>\n" \
                        "<prop id=''power-405'' type=''int'' value=" + str(self.lasersControl.slider405.value()) + "/>\n" \
                        "<prop id=''power-488'' type=''int'' value=" + str(self.lasersControl.slider488.value()) + "/>\n" \
                        "<prop id=''power-561'' type=''int'' value=" + str(self.lasersControl.slider561.value()) + "/>\n" \
                        "<prop id=''IL-shutter-state'' type=''string'' value=" + str(self.microscopeSettings.labelShutterILState.text()) + "/>\n" \
                        "<prop id=''TL-shutter-state'' type=''string'' value=" + str(self.microscopeSettings.labelShutterBFState.text()) + "/>\n" \
                        "<prop id=''TL-light-intensity'' type=''int'' value=" + str(self.microscopeSettings.sliderIntensityBF.value()) + "/>\n" \
                        "<prop id=''acquisition-mode'' type=''string'' value=" + acqMode + "/>\n" \
                        "<prop id=''illumination-type'' type=''string'' value=" + illumType + "/>\n" \
                        "<prop id=''contrast-method'' type=''string'' value=" + contrastMethod + "/>\n" \
                        "</ExperimentInfo>\n" \
                        "<SetInfo>\n" \
                        "<prop id=''number-of-planes'' type=''int'' value=''1''/>\n" \
                        "</SetInfo>\n" \
                        "</MetaData>"

    def updateAcquisitionState(self, flag):
        if flag == "Saving":
            self.palmControl.setProgress("Satus: Saving")
        if flag.find("/") != -1:
            self.palmControl.setProgress("Satus: Acquiring (" + flag + ")")


    def snapImage(self):
        """Takes a snapshot, convert to a pixmap, display it in the display window and compute and display the histogram.
        """
        self.startAcq()

        data.frame = MM.snapImage()
        self.collectMetadata()
        y, x = np.histogram(data.frame.ravel(), bins=np.linspace(data.histMin, data.histMax, data.histMax-data.histMin))
        self.showFrame(data.frame, x, y)

        self.stopAcq()

    def showFrame(self, frame, x, y):
        """Displays the image sent by the movie thread and its histogram
        """

        if type(frame) is not QtGui.QPixmap:
            data.frame = frame
            data.histX = x
            data.histY = y
            pix = imageFunctions.array2Pixmap(frame)
            self.imageViewer.displayWindow.setImage(pix)
        else:
            self.imageViewer.displayWindow.setImage(frame)

        if len(x) == len(y)+1:
            self.hist.updateHist(x, y)

    def startMovie(self):
        """Start live acquisition via a thread
        """
        if data.canSetROI:
            data.canSetROI = False

        self.acquisitionControl.buttonStop.setEnabled(True)
        self.acquisitionControl.buttonLive.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(False)
        self.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
        self.palmControl.pushButtonAcquirePALMSequence.setEnabled(False)
        self.autoFocus.pushButtonFindFocus.setEnabled(False)
        self.imageViewer.pushButtonSetROI.setEnabled(False)

        MM.startAcquisition()
        data.isAcquiring = True

        self.startAcq()

        self.movieAcq.setTerminationEnabled(True)
        self.movieAcq.start()

    def stopMovie(self):
        """Stops the movie thread and the acquisition
        """
        self.movieAcq.terminate()

        self.stopAcq()

        MM.stopAcquisition()
        data.isAcquiring = False
        self.collectMetadata()

        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonStop.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)
        self.palmControl.pushButtonAcquirePALMSequence.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)

    def runPALMSequence(self):
        """Runs the PALM acquisition sequence via a thread
        """
        imageNumber = self.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:
            self.collectMetadata()

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

            self.startAcq()

            MM.startAcquisition()
            data.isAcquiring = True

            self.sequencePalmThread.start()

    def runPALM(self):
        """Runs the PALM acquisition via a thread
        """
        imageNumber = self.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:
            self.collectMetadata()

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

            self.startAcq()

            self.palmControl.setProgress("Satus: Acquiring (0/" + str(imageNumber) + ")")

            MM.startAcquisition()
            data.isAcquiring = True

            self.palmThread.start()

    def stopPALMAcq(self):
        """Stops the PALM thread, display the last image of the stack and its histogram, save the stack and set the ROI baack to full chip
        """
        self.stopAcq()

        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonStop.setEnabled(False)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)
        self.imageViewer.pushButtonZoom.setEnabled(True)

        MM.stopAcquisition()
        data.isAcquiring = False

        self.palmControl.setProgress("Satus: Idle")

        frame = data.palmStack[-1,:,:]
        y, x = np.histogram(frame.ravel(), bins=np.linspace(data.histMin, data.histMax, data.histMax - data.histMin))
        self.showFrame(frame, x, y)

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
        self.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
        self.palmControl.pushButtonAcquirePALMSequence.setEnabled(False)
        self.autoFocus.pushButtonFindFocus.setEnabled(False)
        self.imageViewer.pushButtonSetROI.setEnabled(False)

        data.isAcquiring = True

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
            y, x = np.histogram(frame.ravel(), bins=np.linspace(data.histMin, data.histMax, data.histMax-data.histMin))
            self.showFrame(frame, x, y)
            QtTest.QTest.qWait(100)

        idxMax = np.argmin(data.varStack)
        bestFocus = data.AFZPos[idxMax]
        MM.setZPos(bestFocus)
        QtTest.QTest.qWait(100)
        self.snapImage()
        data.isAcquiring = False

        self.acquisitionControl.buttonStop.setEnabled(True)
        self.acquisitionControl.buttonLive.setEnabled(True)
        self.acquisitionControl.buttonSave.setEnabled(True)
        self.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.palmControl.pushButtonAcquirePALM.setEnabled(True)
        self.palmControl.pushButtonAcquirePALMSequence.setEnabled(True)
        self.autoFocus.pushButtonFindFocus.setEnabled(True)
        self.imageViewer.pushButtonSetROI.setEnabled(True)

    def startAcq(self):
        """Handles the automatic opening of the shutter when an acquisition starts
        """
        scopeSettings.Ui_MicroscopeSettings.startAcq(self.microscopeSettings)

    def stopAcq(self):
        """Handles the automatic closing of the shutter when an acquisition stops
        """
        scopeSettings.Ui_MicroscopeSettings.stopAcq(self.microscopeSettings)
