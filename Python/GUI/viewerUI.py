# -*- coding: utf-8 -*-
"""
This file contains the UI code for image viewer window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 26 16:31:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.histCommands as histCommands
import GUI.Widgets.imageViewerUI as imageViewerUI
import GUI.Widgets.histPlot as histPlot
import Modules.threads as threads
from PyQt5 import QtWidgets, QtCore, QtGui
from fast_histogram import histogram1d
import numpy as np
import tifffile
import data


class Ui_Viewer(QtWidgets.QMainWindow):

    storedFrame = []
    displayedFrame = []
    histX = []
    histY = []
    canZoom = False
    autoRange = False
    minHist = 0
    maxHist = (2**16)-1

    metadataCollectionSignal = QtCore.pyqtSignal(object)
    savingImageSignal = QtCore.pyqtSignal()
    imageSavedSignal = QtCore.pyqtSignal()
    saveCancelSignal = QtCore.pyqtSignal()

    def __init__(self, thread):
        """Setups all the elements positions and connections with functions
        """
        super(Ui_Viewer, self).__init__()

        self.thread = thread

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)

        #Image Display Widget
        self.imageDisplay = imageViewerUI.Ui_ImageViewer()

        #Histogram Commands Widget
        self.histogramCommands = histCommands.Ui_Histogram()

        #Histogram display Widget
        self.histogramDisplay = histPlot.Ui_HistPlot()
        self.histogramDisplay.setMinimumSize(QtCore.QSize(0, 120))

        self.mainLayout.addWidget(self.histogramCommands, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.imageDisplay, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.histogramDisplay, 1, 1, 1, 1)

        self.saveThread = threads.savingThread()

        self.setCentralWidget(self.centralWidget)
        # self.setWindowTitle("Image Viewer")

        self.saveThread.imageSavedSignal.connect(self.imageSaved)
        self.imageDisplay.saveImageSignal.connect(self.saveImage)
        self.histogramCommands.autoRangeSignal.connect(self.setAutoRange)
        self.histogramCommands.setMinSignal.connect(self.setMinHist)
        self.histogramCommands.setMaxSignal.connect(self.setMaxHist)
        if self.thread is not None:
            self.thread.showFrame.connect(self.showMovieFrame)
            if self.thread.flag == 'PALM':
                self.thread.storeFrame.connect(self.storeFrame)

    def stopMovie(self):
        if self.thread is not None:
            self.thread.showFrame.disconnect()
            if self.thread.flag == 'PALM':
                self.thread.storeFrame.disconnect()
        self.imageDisplay.pushButtonSave.setEnabled(True)

    def showFrame(self, frame, flag):
        """Displays the image sent by the movie thread and its histogram
        """
        if type(frame) is not QtGui.QPixmap:
            self.displayedFrame = frame
            if flag == 'snap':
                self.storedFrame = frame

            if self.autoRange:
                self.minHist = frame.min()
                self.maxHist = frame.max()


            self.histX = np.linspace(self.minHist, self.maxHist, self.maxHist-self.minHist)
            self.histY = histogram1d(frame.ravel(), bins=self.maxHist-self.minHist, range=(self.minHist, self.maxHist))

            pix = array2Pixmap(frame, self.minHist, self.maxHist)
            self.imageDisplay.displayWindow.setImage(pix)
        else:
            self.imageDisplay.displayWindow.setImage(frame)

        self.updateHist(self.histX, self.histY)

    def showMovieFrame(self, frame, pix, x, y, flag):
        """Displays the image sent by the movie thread and its histogram
        """
        self.histX = x
        self.histY = y
        self.displayedFrame = frame
        if flag == 'movie':
            self.storedFrame = frame

        if self.autoRange:
            self.minHist = frame.min()
            self.maxHist = frame.max()

        self.imageDisplay.displayWindow.setImage(pix)

        self.updateHist(self.histX, self.histY)

    def storeFrame(self, frame):
        self.storedFrame.append(frame)

    def setAutoRange(self, signal):
        flag = 'update'
        self.autoRange = signal

        if self.autoRange is True and data.isAcquiring is False and self.displayedFrame != []:
            self.showFrame(self.displayedFrame, flag)

    def setMinHist(self, valueMin):
        flag = 'update'
        self.minHist = valueMin

        if data.isAcquiring is False and self.displayedFrame != []:
            self.showFrame(self.displayedFrame, flag)

    def setMaxHist(self, valueMax):
        flag = 'update'
        self.maxHist = valueMax

        if data.isAcquiring is False and self.displayedFrame != []:
            self.showFrame(self.displayedFrame, flag)

    def updateHist(self, x, y):
        if self.autoRange:
            self.histogramCommands.sliderMinimum.setValue(self.minHist)
            self.histogramCommands.spinBoxMin.setValue(self.minHist)
            self.histogramCommands.sliderMaximum.setValue(self.maxHist)
            self.histogramCommands.spinBoxMax.setValue(self.maxHist)
        self.histogramDisplay.p1.clear()
        self.histogramDisplay.p1.plot(x, y, stepMode=False, fillLevel=0, brush=(0, 0, 0, 255))

    @QtCore.pyqtSlot()
    def saveImage(self):
        """Saves a 2d image with automatic naming and increment saved images counter
        """
        self.savingImageSignal.emit()
        self.metadataCollectionSignal.emit(self.displayedFrame)

        self.imageDisplay.pushButtonSave.setEnabled(False)
        self.imageDisplay.pushButtonZoom.setEnabled(False)

        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save As ...", data.savePath + '/' + self.windowTitle(), "Image File (*.tif)")[0]
        if path != "":
            delimiterPos = [pos for pos, char in enumerate(path) if char == '/']

            if data.savePath != path[0:max(delimiterPos)]:
                data.savePath = path[0:max(delimiterPos)]

            self.saveThread.pixels = self.storedFrame
            self.saveThread.path = path
            self.saveThread.start()

            self.setWindowTitle(path[max(delimiterPos)+1:-4])
        else:
            self.imageDisplay.pushButtonSave.setEnabled(True)
            self.imageDisplay.pushButtonZoom.setEnabled(True)
            self.saveCancelSignal.emit()

    @QtCore.pyqtSlot()
    def saveBatch(self, fileName, idx):
        """Saves a 2d image with automatic naming and increment saved images counter
        """
        self.savingImageSignal.emit()
        pixels = np.asarray(self.storedFrame)
        self.metadataCollectionSignal.emit(pixels)

        self.imageDisplay.pushButtonSave.setEnabled(False)
        self.imageDisplay.pushButtonZoom.setEnabled(False)

        delimiterPos = [pos for pos, char in enumerate(data.savePath) if char == '/']

        if idx < 10:
            fileName = fileName + '00' + str(idx)
        elif idx < 100:
            fileName = fileName + '0' + str(idx)
        elif idx < 1000:
            fileName = fileName + str(idx)

        path = data.savePath + '/' + fileName + ".tif"

        self.saveThread.pixels = pixels
        self.saveThread.path = path
        self.saveThread.start()

        self.setWindowTitle(path[max(delimiterPos) + 1:-4])

    @QtCore.pyqtSlot()
    def imageSaved(self):
        self.imageSavedSignal.emit()

        self.imageDisplay.pushButtonSave.setEnabled(True)
        self.imageDisplay.pushButtonZoom.setEnabled(True)


def array2Pixmap(frame, minHist, maxHist):
    """ Returns an 8 bits image pixmap from a raw 16 bits 2D array for display
    Before conversion, image values are scaled to the full dynamic range of the 8 bits image for better display
    :type frame: 2d array
    :rtype: QPixmap
    """
    idxHigh = np.where(frame > maxHist)
    idxLow = np.where(frame < minHist)
    frame[idxHigh] = maxHist-1
    frame[idxLow] = minHist
    img8 = abs((frame - minHist) / (maxHist-minHist))
    img8 = (img8*255).astype(np.uint8)
    img = QtGui.QImage(img8, img8.shape[0], img8.shape[1], QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap(img)
    return pix

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Viewer()
    ui.show()
    app.exec_()