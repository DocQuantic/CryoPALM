# -*- coding: utf-8 -*-
"""
This file contains the main UI code 
Form implementation generated from reading ui file 'guiMain.ui'

Created on Fri Mar 29 09:54:55 2019
Created with PyQt5 UI code generator 5.9.2

@author: William Magrini @ Bordeaux Imaging Center
"""

import Modules.threads as threads
import GUI.experimentControlUI as experimentControlUI
import GUI.lasersControlUI as lasersControlUI
import GUI.counterControlUI as counterControlUI
import GUI.autoFocusUI as autoFocusUI
import GUI.viewerUI as viewerUI
import GUI.countGraphUI as countGraphUI
from PyQt5 import QtCore, QtWidgets, QtGui, QtTest
from scipy import ndimage
import Modules.MM as MM
import numpy as np
import data


class Ui_MainWindow(QtWidgets.QMainWindow):

    isBatchRunning = False

    def __init__(self):
        """Setups all the elements positions and connections with functions
        """
        super(Ui_MainWindow, self).__init__()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.centralWidget = QtWidgets.QWidget()

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.experimentControlUI = experimentControlUI.Ui_ExperimentControl()
        self.mainLayout.addWidget(self.experimentControlUI)

        self.experimentControlWidth = self.experimentControlUI.frameGeometry().width()
        self.experimentControlHeight = self.experimentControlUI.frameGeometry().height()

        #Main window configuration
        self.setWindowTitle("Cryo PALM")
        self.setCentralWidget(self.centralWidget)

        #Menu bar configuration
        self.menuBar = QtGui.QMenuBar(self)
        self.fileMenu = self.menuBar.addMenu('&File')
        self.toolsMenu = self.menuBar.addMenu('&Tools')

        self.actionExit = QtWidgets.QAction("Exit")
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.triggered.connect(self.closeApp)

        self.actionCloseAll = QtWidgets.QAction("Close All")
        self.actionCloseAll.triggered.connect(self.closeAllViewers)

        self.actionLasersControl = QtWidgets.QAction("Lasers Control")
        self.actionLasersControl.triggered.connect(self.openLasersControl)

        self.actionCounterControl = QtWidgets.QAction("Particules Counter")
        self.actionCounterControl.triggered.connect(self.openCounterControl)

        self.actionAutoFocus = QtWidgets.QAction("Auto Focus")
        self.actionAutoFocus.triggered.connect(self.openAF)

        self.fileMenu.addAction(self.actionExit)
        self.fileMenu.addAction(self.actionCloseAll)
        self.toolsMenu.addAction(self.actionLasersControl)
        self.toolsMenu.addAction(self.actionCounterControl)
        self.toolsMenu.addAction(self.actionAutoFocus)

        self.menuBar.addAction(self.fileMenu.menuAction())
        self.menuBar.addAction(self.toolsMenu.menuAction())

        #Additional windows configuration
        self.lasersControlUI = lasersControlUI.Ui_LasersControl()
        self.autoFocusUI = autoFocusUI.Ui_AutoFocus()
        self.counterControlUI = counterControlUI.Ui_CounterControl()

        #Threads configuration
        self.movieThread = threads.MovieThread(None)
        self.palmThread = threads.PALMThread(None)
        self.batchThread = threads.BatchThread(0)
        self.countThread = threads.CountThread()
        self.palmThread.countThread = self.countThread
        self.currentThread = self.movieThread

        self.viewerList = []
        self.currentViewer = []
        self.countGraphList = []
        self.currentCountGraph = None

        self.experimentControlUI.palmControl.runSinglePALMSignal.connect(self.runPALM)
        self.experimentControlUI.palmControl.popUp.runBatchSignal.connect(self.runBatch)
        self.batchThread.runPALMSignal.connect(self.runPALM)
        self.batchThread.runMovieSignal.connect(self.startMovie)
        self.batchThread.savePALMSignal.connect(self.saveBatch)
        self.batchThread.stopMovieSignal.connect(self.stopMovie)
        self.batchThread.closeViewersSignal.connect(self.closeViewersBatch)
        self.batchThread.stopBatchSignal.connect(self.stopBatch)
        self.experimentControlUI.palmControl.stopSinglePALMSignal.connect(self.stopPALMAcq)
        self.experimentControlUI.palmControl.stopSinglePALMSignal.connect(self.stopBatch)
        self.palmThread.stopPALM.connect(self.stopPALMAcq)
        self.palmThread.acquisitionState.connect(self.updateAcquisitionState)
        self.countThread.countSignal.connect(self.updateGraph)
        self.experimentControlUI.acquisitionControl.takeSnapshotSignal.connect(self.snapImage)
        self.experimentControlUI.acquisitionControl.startMovieSignal.connect(self.startMovie)
        self.experimentControlUI.acquisitionControl.stopMovieSignal.connect(self.stopMovie)
        self.experimentControlUI.acquisitionControl.setROISignal.connect(self.setCenterQuad)
        # self.autoFocus.runAFSignal.connect(self.runAF)

    def closeEvent(self, event):
        self.closeAllViewers()
        self.lasersControlUI.close()
        self.counterControlUI.close()
        self.autoFocusUI.close()
        event.accept()

    def closeApp(self):
        self.closeAllViewers()
        QtCore.QCoreApplication.instance().quit()

    def openLasersControl(self):
        self.lasersControlUI.show()
        self.lasersControlUI.move(0, 820)

    def openCounterControl(self):
        self.counterControlUI.show()
        self.counterControlUI.move(0, 1340)

    def openAF(self):
        self.autoFocusUI.show()
        self.autoFocusUI.move(0, 1160)

    def openViewer(self, flag):
        if flag == 'snap':
            viewer = viewerUI.Ui_Viewer(None)
            viewer.setWindowTitle("Snapshot")
        elif flag == 'movie':
            viewer = viewerUI.Ui_Viewer(self.movieThread)
            viewer.setWindowTitle("Live")
        elif flag == 'PALM':
            viewer = viewerUI.Ui_Viewer(self.palmThread)
            viewer.setWindowTitle("Stream")

        viewer.storedFrame = []
        viewer.show()

        if data.countingState:
            countGraphWidget = countGraphUI.Ui_CounterGraph()
            countGraphWidget.show()
            countGraphWidget.move(1800, 0)
            self.currentCountGraph = countGraphWidget

        self.currentViewer = viewer

        self.currentViewer.savingImageSignal.connect(self.savingImage)
        self.currentViewer.imageSavedSignal.connect(self.imageSaved)
        self.currentViewer.metadataCollectionSignal.connect(self.collectMetadata)
        self.currentViewer.saveCancelSignal.connect(self.imageSaved)
        self.currentViewer.move(420, 0)
        self.viewerList.append(viewer)

    def closeViewersBatch(self):
        self.viewerList[-1].close()
        del self.viewerList[-1]
        self.viewerList[-1].close()
        del self.viewerList[-1]

    def closeAllViewers(self):
        self.currentViewer = []
        for viewer in self.viewerList:
            viewer.close()
        self.viewerList = []

    def setCenterQuad(self, signal):
        if data.isAcquiring:
            self.stopMovie()

            if signal:
                MM.setROI(895, 895, 256, 256)
            else:
                MM.clearROI()

            self.startMovie()
        else:
            if signal:
                MM.setROI(895, 895, 256, 256)
            else:
                MM.clearROI()

    def savingImage(self):
        self.updateAcquisitionState("Saving")

        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)

    def saveBatch(self, fileName, idx):
        self.currentViewer.saveBatch(fileName, idx)

    def imageSaved(self):
        self.updateAcquisitionState("Idle")

        if self.isBatchRunning:
            self.batchThread.isSaving = False

        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)

    def collectMetadata(self, frame):
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
                        "<prop id=''pixel-size-x'' type=''int'' value=" + str(frame.shape[0]) + "/>\n" \
                        "<prop id=''pixel-size-y'' type=''int'' value=" + str(frame.shape[1]) + "/>\n" \
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
                        "<prop id=''camera-exposure-time'' type=''float'' value=" + str(self.experimentControlUI.cameraSettings.sliderExposure.value()) + "/>\n" \
                        "<prop id=''light-path'' type=''string'' value=" + str(MM.getPropertyValue('Scope', 'Method')) + "/>\n" \
                        "<prop id=''filter-set'' type=''string'' value=" + str(MM.getPropertyValue('IL-Turret', 'Label')) + "/>\n" \
                        "<prop id=''laser-shutter-state'' type=''string'' value=" + str(self.lasersControlUI.lasersControl.pushButtonShutter.isChecked()) + "/>\n" \
                        "<prop id=''AOTF-blank-state'' type=''string'' value=" + str(self.lasersControlUI.lasersControl.pushButtonBlank.isChecked()) + "/>\n" \
                        "<prop id=''power-405'' type=''int'' value=" + str(self.lasersControlUI.lasersControl.slider405.value()) + "/>\n" \
                        "<prop id=''power-488'' type=''int'' value=" + str(self.lasersControlUI.lasersControl.slider488.value()) + "/>\n" \
                        "<prop id=''power-561'' type=''int'' value=" + str(self.lasersControlUI.lasersControl.slider561.value()) + "/>\n" \
                        "<prop id=''IL-shutter-state'' type=''string'' value=" + str(self.experimentControlUI.microscopeSettings.labelShutterILState.text()) + "/>\n" \
                        "<prop id=''TL-shutter-state'' type=''string'' value=" + str(self.experimentControlUI.microscopeSettings.labelShutterBFState.text()) + "/>\n" \
                        "<prop id=''TL-light-intensity'' type=''int'' value=" + str(self.experimentControlUI.microscopeSettings.sliderIntensityBF.value()) + "/>\n" \
                        "<prop id=''acquisition-mode'' type=''string'' value=" + acqMode + "/>\n" \
                        "<prop id=''illumination-type'' type=''string'' value=" + illumType + "/>\n" \
                        "<prop id=''contrast-method'' type=''string'' value=" + contrastMethod + "/>\n" \
                        "</ExperimentInfo>\n" \
                        "<SetInfo>\n" \
                        "<prop id=''number-of-planes'' type=''int'' value=''1''/>\n" \
                        "</SetInfo>\n" \
                        "</MetaData>"

    def startAcq(self, flag):
        """Handles the automatic opening of the shutter when an acquisition starts
        """
        data.waitTime = MM.cameraAcquisitionTime()
        self.openViewer(flag)
        self.experimentControlUI.microscopeSettings.startAcq()
        self.lasersControlUI.lasersControl.pushButtonBlank.setChecked(False)
        self.lasersControlUI.lasersControl.blankOutputs()
        self.lasersControlUI.lasersControl.pushButton405.setChecked(True)
        self.lasersControlUI.lasersControl.switch405()

    def stopAcq(self):
        """Handles the automatic closing of the shutter when an acquisition stops
        """
        self.experimentControlUI.microscopeSettings.stopAcq()
        self.currentViewer.stopMovie()
        self.lasersControlUI.lasersControl.pushButtonBlank.setChecked(True)
        self.lasersControlUI.lasersControl.blankOutputs()
        self.lasersControlUI.lasersControl.pushButton405.setChecked(False)
        self.lasersControlUI.lasersControl.switch405()

    def updateMovieFrame(self, pixmap, x, y):
        self.currentViewer.showMovieFrame(pixmap, x, y)

    def updateGraph(self, count, idx):
        if self.currentCountGraph is not None:
            self.currentCountGraph.updateGraph(count, idx)

    def snapImage(self):
        """Takes a snapshot, convert to a pixmap, display it in the display window and compute and display the histogram.
        """
        flag = 'snap'
        self.startAcq(flag)

        frame = MM.snapImage()
        self.currentViewer.showFrame(frame, flag)

        self.stopAcq()

    def startMovie(self):
        """Start live acquisition via a thread
        """
        flag = 'movie'
        self.currentThread = self.movieThread

        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)

        MM.startAcquisition()
        data.isAcquiring = True

        self.startAcq(flag)
        self.movieThread.imageViewer = self.currentViewer
        self.movieThread.setTerminationEnabled(True)
        if self.isBatchRunning:
            self.currentViewer.autoRange = True
        self.movieThread.start()

    def stopMovie(self):
        """Stops the movie thread and the acquisition
        """
        self.movieThread.acquire = False
        self.movieThread.terminate()

        self.stopAcq()

        MM.stopAcquisition()
        data.isAcquiring = False

        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(True)

    def runPALM(self):
        """Runs the PALM acquisition via a thread
        """
        flag = 'PALM'
        self.currentThread = self.palmThread

        imageNumber = self.experimentControlUI.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:

            MM.setROI(896, 896, 256, 256)
            data.changedBinning = True
            self.experimentControlUI.acquisitionControl.buttonSetROI.setChecked(True)

            self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonSetROI.setEnabled(False)
            self.experimentControlUI.palmControl.pushButtonStopPALMSingle.setEnabled(True)
            self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
            self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)

            self.palmThread.imageNumber = imageNumber

            self.startAcq(flag)
            self.palmThread.imageViewer = self.currentViewer

            MM.startAcquisition()
            data.isAcquiring = True

            self.palmThread.setTerminationEnabled(True)
            if self.isBatchRunning:
                self.currentViewer.autoRange = True
            self.palmThread.countingState = data.countingState
            self.palmThread.start()

    def runBatch(self, maxNumber, fileName):
        if maxNumber != 0:
            self.batchThread.batchNumber = maxNumber
            self.batchThread.fileName = fileName

            self.batchThread.setTerminationEnabled(True)
            self.batchThread.start()
            self.isBatchRunning = True

    def stopBatch(self):
        self.batchThread.terminate()
        self.isBatchRunning = False

    def stopPALMAcq(self):
        """Stops the PALM thread, display the last image of the stack and its histogram, save the stack and set the ROI baack to full chip
        """
        self.stopAcq()

        self.currentCountGraph = None

        self.palmThread.acquire = False
        self.palmThread.terminate()

        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonSetROI.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonSetROI.setChecked(False)
        self.experimentControlUI.palmControl.pushButtonStopPALMSingle.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(True)

        MM.stopAcquisition()
        data.isAcquiring = False

        if self.isBatchRunning:
            self.batchThread.isPALMRunning = False

        self.experimentControlUI.palmControl.setProgress("Satus: Idle")

        data.changedBinning = True

    def updateAcquisitionState(self, flag):
        if flag == "Saving":
            self.experimentControlUI.palmControl.setProgress("Satus: Saving")
        elif flag.find("/") != -1:
            self.experimentControlUI.palmControl.setProgress("Satus: Acquiring (" + flag + ")")
        elif flag == "Idle":
            self.experimentControlUI.palmControl.setProgress("Satus: Idle")

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