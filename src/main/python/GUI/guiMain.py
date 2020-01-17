# -*- coding: utf-8 -*-
"""
This file contains the main UI code.

Created on Fri Mar 29 09:54:55 2019

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
import Modules.MM as MM
import numpy as np
import data
import Modules.AFModes as AF
import tifffile


class Ui_MainWindow(QtWidgets.QMainWindow):

    isBatchRunning = False

    def __init__(self):
        """
        Setups all the elements positions and connections with functions.
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

        # Main window configuration
        self.setWindowTitle("Cryo PALM")
        self.setCentralWidget(self.centralWidget)

        # Menu bar configuration
        self.menuBar = QtGui.QMenuBar(self)
        self.fileMenu = self.menuBar.addMenu('&File')
        self.windowsMenu = self.menuBar.addMenu('&Tools')

        self.actionOpen = QtWidgets.QAction("Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openTif)

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
        self.fileMenu.addAction(self.actionOpen)
        self.windowsMenu.addAction(self.actionLasersControl)
        self.windowsMenu.addAction(self.actionCounterControl)
        self.windowsMenu.addAction(self.actionAutoFocus)
        self.windowsMenu.addAction(self.actionCloseAll)

        self.menuBar.addAction(self.fileMenu.menuAction())
        self.menuBar.addAction(self.windowsMenu.menuAction())

        # Additional windows configuration
        self.lasersControlUI = lasersControlUI.Ui_LasersControl()
        self.autoFocusUI = autoFocusUI.Ui_AutoFocus()
        self.counterControlUI = counterControlUI.Ui_CounterControl()

        # Threads configuration
        self.movieThread = threads.MovieThread(None)
        self.palmThread = threads.PALMThread(None)
        self.batchThread = threads.BatchThread(0)
        self.countThread = threads.CountThread()
        self.palmThread.countThread = self.countThread
        self.currentThread = self.movieThread

        self.viewerList = []
        self.currentViewer = None
        self.countGraphList = []
        self.currentCountGraph = None

        self.switcherAF = AF.SwitcherAF()

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
        self.autoFocusUI.autoFocus.runAFSignal.connect(self.runAF)
        self.counterControlUI.clearMarksSignal.connect(self.clearMarksViewers)
        self.counterControlUI.showMarksSignal.connect(self.showMarksViewer)

    def closeEvent(self, event):
        """
        Closes all the viewers and controllers when the close button is pressed.
        :param event: event
        """
        self.closeAllViewers()
        self.lasersControlUI.close()
        self.counterControlUI.close()
        self.autoFocusUI.close()
        event.accept()

    def closeApp(self):
        """
        Closes the applicaton.
        """
        self.closeAllViewers()
        QtCore.QCoreApplication.instance().quit()

    def openTif(self):
        """
        Opens an image in a new viewer.
        """

        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open ...", data.savePath, "Image File (*.tif)")[0]
        if path != "":
            image = tifffile.imread(path)
            self.openViewer('snap')

            delimiterPos = [pos for pos, char in enumerate(path) if char == '/']
            self.currentViewer.setWindowTitle(path[max(delimiterPos)+1:-4])
            if len(image.shape) == 2:
                self.currentViewer.showFrame(image, 'snap')
                self.currentViewer.storeFrame(image)
            else:
                slicesCount = image.shape[0]
                idx = 0
                self.currentViewer.showFrame(image[idx, :, :], 'stack')
                while idx < slicesCount:
                    self.currentViewer.storeFrame(image[idx, :, :])
                    idx += 1
                self.currentViewer.imageDisplay.enableSlider(slicesCount)


    def openLasersControl(self):
        """
        Opens the lasers control window.
        """
        self.lasersControlUI.show()
        self.lasersControlUI.move(0, 820)

    def openCounterControl(self):
        """
        Opens the particules counter window.
        """
        self.counterControlUI.show()
        self.counterControlUI.move(0, 1340)

    def openAF(self):
        """
        Opens the Auto Focus control window.
        """
        self.autoFocusUI.show()
        self.autoFocusUI.move(0, 1160)

    def openViewer(self, flag):
        """
        Opens a viewer and set its flag.
        :param flag: string
        """
        if flag == 'snap':
            viewer = viewerUI.Ui_Viewer(None)
            viewer.setWindowTitle("Snapshot")
        elif flag == 'movie':
            viewer = viewerUI.Ui_Viewer(self.movieThread)
            viewer.setWindowTitle("Live")
        elif flag == 'PALM':
            viewer = viewerUI.Ui_Viewer(self.palmThread)
            viewer.setWindowTitle("Stream")
        elif flag == 'AF':
            viewer = viewerUI.Ui_Viewer(self.palmThread)
            viewer.setWindowTitle("Z-Stack")

        # viewer.storedFrame = []
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
        """
        Closes the last two viewer windows opened after a batch is saved (last batch and live windows).
        """
        self.viewerList[-1].close()
        del self.viewerList[-1]
        self.viewerList[-1].close()
        del self.viewerList[-1]

    def closeAllViewers(self):
        """
        Closes all the opened viewer windows.
        """
        self.currentViewer = None
        for viewer in self.viewerList:
            viewer.close()
        self.viewerList = []

    def setCenterQuad(self, signal):
        """
        Sets the ROI to a quad of 256 by 256 pixels centered on the camera chip. If the ROI was already on center quad,
        it resets the ROI to full chip.
        :param signal: boolean
        """
        if data.isAcquiring:
            self.stopMovie()

            if signal:
                MM.setROI(int(data.xDim / (4 * data.binning)), int(data.yDim / (4 * data.binning)),
                          int(256 / data.binning),
                          int(256 / data.binning))
            else:
                MM.clearROI()

            self.startMovie()
        else:
            if signal:
                MM.setROI(int(data.xDim / (4 * data.binning)), int(data.yDim / (4 * data.binning)),
                          int(256 / data.binning),
                          int(256 / data.binning))
            else:
                MM.clearROI()

    def clearMarksViewers(self):
        for viewer in self.viewerList:
            viewer.imageDisplay.displayWindow.clearMarks()

    def showMarksViewer(self):
        self.currentViewer.countAndShow(self.currentViewer.displayedFrame)

    def savingImage(self):
        """
        Handles the display and the activated buttons while an image is being saved.
        """
        self.updateAcquisitionState("Saving")

        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)

    def saveBatch(self, fileName, idx):
        """
        Sets the fileName and the index of the batch to be saved.
        :param fileName: string
        :param idx: int
        """
        self.currentViewer.saveBatch(fileName, idx)

    def imageSaved(self):
        """
        Handles the display and the activated buttons once an image is saved.
        """
        self.updateAcquisitionState("Idle")

        if self.isBatchRunning:
            self.batchThread.isSaving = False

        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)

    def collectMetadata(self, frame):
        """
        Collects all the system information in order to save in image metadata.
        :param frame: 2d array
        """
        lightPath = MM.getPropertyValue('Scope', 'Method')
        if lightPath == 'FLUO':
            acqMode = 'WideField'
            illumType = 'Epifluorescence'
            contrastMethod = 'Fluorescence'
        else:
            acqMode = 'BrightField'
            illumType = 'Transmitted'
            contrastMethod = 'BrightField'

        if data.isCameraEM:
            EMGain = str(MM.getProperty(data.cameraName, 'MultiplierGain'))
        else:
            EMGain = 'N/A'

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
                        "<prop id=''camera-EMGain'' type=''int'' value=" + EMGain + "/>\n" \
                        "<prop id=''light-path'' type=''string'' value=" + str(MM.getPropertyValue('Scope', 'Method')) + "/>\n" \
                        "<prop id=''filter-set'' type=''string'' value=" + str(MM.getPropertyValue('IL-Turret', 'Label')) + "/>\n" \
                        "<prop id=''laser-shutter-state'' type=''string'' value=" + str(self.lasersControlUI.lasersControl.pushButtonShutter.isChecked()) + "/>\n" \
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
        """
        Handles the automatic opening of the shutter when an acquisition starts.
        """
        data.waitTime = MM.cameraAcquisitionTime()
        self.openViewer(flag)
        self.experimentControlUI.microscopeSettings.startAcq()

    def stopAcq(self):
        """
        Handles the automatic closing of the shutter when an acquisition stops.
        """
        self.experimentControlUI.microscopeSettings.stopAcq()
        self.currentViewer.stopMovie()

    def updateMovieFrame(self, pixmap, x, y):
        """
        Updates the current viewer's displayed frame and histogram.
        :param pixmap: QPixmap
        :param x: array
        :param y: array
        """
        self.currentViewer.showMovieFrame(pixmap, x, y)

    def updateGraph(self, count, cX, cY, idx, showMarks):
        """
        Updates the count graph by adding it the last measured value.
        :param count: int
        :param idx: int
        """
        if self.currentCountGraph is not None:
            self.currentCountGraph.updateGraph(count, idx)
            if showMarks:
                self.currentViewer.imageDisplay.displayWindow.clearMarks()
                self.currentViewer.imageDisplay.displayWindow.showParticulesPositions(cX, cY)


    def snapImage(self):
        """
        Takes a snapshot, convert to a pixmap, display it in the display window and compute and display the histogram.
        """
        flag = 'snap'
        self.startAcq(flag)
        QtTest.QTest.qWait(10)

        frame = MM.snapImage()
        self.currentViewer.showFrame(frame, flag)

        self.stopAcq()

    def startMovie(self):
        """
        Start live acquisition via a thread.
        """
        flag = 'movie'
        self.currentThread = self.movieThread

        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)
        self.autoFocusUI.autoFocus.pushButtonFindFocus.setEnabled(False)

        MM.startAcquisition()
        data.isAcquiring = True

        self.startAcq(flag)
        self.movieThread.imageViewer = self.currentViewer
        self.movieThread.setTerminationEnabled(True)
        if self.isBatchRunning:
            self.currentViewer.autoRange = True
        self.movieThread.start()

    def stopMovie(self):
        """
        Stops the movie thread and the acquisition.
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
        self.autoFocusUI.autoFocus.pushButtonFindFocus.setEnabled(True)

    def runPALM(self):
        """
        Runs the PALM acquisition via a thread.
        """
        flag = 'PALM'
        self.currentThread = self.palmThread

        imageNumber = self.experimentControlUI.palmControl.spinBoxImageNumber.value()
        if imageNumber != 0:

            MM.setROI(data.xDim/(4*data.binning), data.yDim/(4*data.binning), 256/data.binning, 256/data.binning)

            data.changedBinning = True
            self.experimentControlUI.acquisitionControl.buttonSetROI.setChecked(True)

            self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(False)
            self.experimentControlUI.acquisitionControl.buttonSetROI.setEnabled(False)
            self.experimentControlUI.palmControl.pushButtonStopPALMSingle.setEnabled(True)
            self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
            self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)
            self.autoFocusUI.autoFocus.pushButtonFindFocus.setEnabled(False)

            self.palmThread.imageNumber = imageNumber

            self.startAcq(flag)
            self.palmThread.imageViewer = self.currentViewer

            MM.startAcquisition()
            data.isAcquiring = True

            self.palmThread.setTerminationEnabled(True)
            # if self.isBatchRunning:
            #     self.currentViewer.autoRange = False
            self.palmThread.start()

    def runBatch(self, maxNumber, fileName):
        """
        Runs the PALM acquisition as a batch acquisition.
        :param maxNumber: int
        :param fileName: string
        """
        if maxNumber != 0:
            self.batchThread.batchNumber = maxNumber
            self.batchThread.fileName = fileName

            self.batchThread.setTerminationEnabled(True)
            self.batchThread.start()
            self.isBatchRunning = True

    def stopBatch(self):
        """
        Stops the current batch
        """
        self.batchThread.terminate()
        self.isBatchRunning = False

    def stopPALMAcq(self):
        """
        Stops the PALM thread, display the last image of the stack and its histogram, save the stack and set the ROI back to full chip.
        """
        self.stopAcq()

        self.currentCountGraph = None

        self.palmThread.acquire = False
        self.palmThread.terminate()

        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonSetROI.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonStopPALMSingle.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(True)
        self.autoFocusUI.autoFocus.pushButtonFindFocus.setEnabled(True)

        MM.stopAcquisition()
        data.isAcquiring = False

        if self.isBatchRunning:
            self.batchThread.isPALMRunning = False

        self.experimentControlUI.palmControl.setProgress("Satus: Idle")

        self.currentViewer.imageDisplay.enableSlider(len(self.currentViewer.storedFrame))

    def updateAcquisitionState(self, flag):
        """
        Updates the acquisition state information label.
        :param flag: string
        """
        if flag == "Saving":
            self.experimentControlUI.palmControl.setProgress("Satus: Saving")
        elif flag.find("/") != -1:
            self.experimentControlUI.palmControl.setProgress("Satus: Acquiring (" + flag + ")")
        elif flag == "Idle":
            self.experimentControlUI.palmControl.setProgress("Satus: Idle")

    def runAF(self):
        """
        Runs the auto focus routine.
        """
        flag = 'AF'

        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(False)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(False)
        # self.experimentControlUI.palmControl.pushButtonAcquirePALMSequence.setEnabled(False)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)

        self.startAcq(flag)

        data.isAcquiring = True

        currentZPos = MM.getZPos()
        data.AFZPos = np.arange(currentZPos-data.AFRange/2.0, currentZPos+data.AFRange/2.0, data.AFStepSize)

        data.valStack = []
        data.AFStack = []
        idx = 0
        for step in data.AFZPos:
            MM.setZPos(step)
            QtTest.QTest.qWait(100)

            frame = MM.snapImage()

            data.AFStack.append(frame)
            idx += 1

            self.currentViewer.showFrame(frame, flag)
            self.currentViewer.storeFrame(frame)

            self.switcherAF.getFocusValue(frame, data.currentAFMethod)

        self.stopAcq()
        idxMin = np.argmin(data.valStack)

        self.currentViewer.imageDisplay.pushButtonSave.setEnabled(True)
        self.currentViewer.imageDisplay.enableSlider(len(self.currentViewer.storedFrame))

        bestFocus = data.AFZPos[idxMin]
        MM.setZPos(bestFocus)
        QtTest.QTest.qWait(200)

        self.snapImage()
        data.isAcquiring = False

        self.experimentControlUI.acquisitionControl.buttonStop.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonLive.setEnabled(True)
        self.experimentControlUI.acquisitionControl.buttonSingleImage.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMSingle.setEnabled(True)
        # self.experimentControlUI.palmControl.pushButtonAcquirePALMSequence.setEnabled(True)
        self.experimentControlUI.palmControl.pushButtonAcquirePALMBatch.setEnabled(False)
