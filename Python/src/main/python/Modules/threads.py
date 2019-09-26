# -*- coding: utf-8 -*-
"""
This file contains two classes implementing threads in the main program. 
Those threads allow for execution a an infinite (or not) while loop during the execution of the main program.
This way, we can continue to interact with other functionnalities of the program while acquisition is running.

Created on Wed Apr  3 15:30:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.acquisitionControlPALM as palmControl
import Modules.pyTracer as pyTracer
import tifffile
from PyQt5 import QtCore, QtGui
from fast_histogram import histogram1d
import Modules.MM as MM
import numpy as np
import data
import time


class MovieThread(QtCore.QThread):
    """This class implements continuous frame acquisition and display.
    Each time a frame is acquired, the thread emits the data of the frame and of the computed histogram.
    """
    flag = 'movie'
    acquire = True
    showFrame = QtCore.pyqtSignal(object, object, object, object, object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer

    @QtCore.pyqtSlot()
    def run(self):
        self.acquire = True
        while self.acquire:
            frame = MM.getMovieFrame()
            
            if frame is not None and frame.shape[0] != 0:
                pix, x, y = processImage(frame, self.imageViewer)
                self.showFrame.emit(frame, pix, x, y, self.flag)
                time.sleep(data.waitTime)


class PALMThread(QtCore.QThread):
    """This class implements PALM acquisition of a fixed amount of frames.
    Each time a series of 10 frames are acquired, the thread emits a signal for displaying the last frame and its histogram.
    At the end of the acquisition, a signal is emitted to tell the main the program that it finished.
    """
    flag = 'PALM'
    acquire = True
    countThread = None
    countingState = False
    showFrame = QtCore.pyqtSignal(object, object, object, object, object)
    storeFrame = QtCore.pyqtSignal(object)
    stopPALM = QtCore.pyqtSignal()
    acquisitionState = QtCore.pyqtSignal(object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer
        self.imageNumber = 0
        self.frameStepShow = 10

    @QtCore.pyqtSlot()
    def run(self):
        idx = 1
        self.acquire = True
        while idx <= self.imageNumber and self.acquire:
            flag = str(idx) + "/" + str(self.imageNumber)
            self.acquisitionState.emit(flag)

            frame = MM.getMovieFrame()
            if frame is not None and frame.shape[0] != 0:
                if self.countingState:
                    self.countThread.frame = frame
                    self.countThread.idx = idx
                    self.countThread.start()
                self.storeFrame.emit(frame)
                if idx % self.frameStepShow == 0:
                    pix, x, y = processImage(frame, self.imageViewer)
                    self.showFrame.emit(frame, pix, x, y, self.flag)
                    
                idx += 1
                time.sleep(data.waitTime)

        self.stopPALM.emit()

class CountThread(QtCore.QThread):
    countSignal = QtCore.pyqtSignal(object, object)
    frame = []
    idx = 0

    def __init__(self):
        QtCore.QThread.__init__(self)

    @QtCore.pyqtSlot()
    def run(self):
        count = pyTracer.countParticules(self.frame, data.countThreshold)

        self.countSignal.emit(count, self.idx)

class BatchThread(QtCore.QThread):
    fileName = 'toto'
    flag = 'batch'
    acquire = True
    runPALMSignal = QtCore.pyqtSignal()
    savePALMSignal = QtCore.pyqtSignal(object, object)
    runMovieSignal = QtCore.pyqtSignal()
    stopMovieSignal = QtCore.pyqtSignal()
    closeViewersSignal = QtCore.pyqtSignal()
    stopBatchSignal = QtCore.pyqtSignal()

    def __init__(self, batchNumber):
        QtCore.QThread.__init__(self)
        self.batchNumber = batchNumber
        self.frameStepShow = 10
        self.isPALMRunning = False
        self.isSaving = False

    @QtCore.pyqtSlot()
    def run(self):
        idx = 0
        self.acquire = True
        self.isPALMRunning = False
        self.isSaving = False

        while idx < self.batchNumber and self.acquire:
            self.runPALMSignal.emit()
            self.isPALMRunning = True

            while self.isPALMRunning:
                time.sleep(1)

            self.savePALMSignal.emit(self.fileName, idx+1)

            self.runMovieSignal.emit()
            self.isSaving = True

            while self.isSaving:
                time.sleep(1)

            self.stopMovieSignal.emit()
            self.closeViewersSignal.emit()

            idx += 1

        self.stopBatchSignal.emit()

class savingThread(QtCore.QThread):

    imageSavedSignal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.pixels = []
        self.path = ""

    @QtCore.pyqtSlot()
    def run(self):
        """Saves an image or a stack
        """
        if type(self.pixels) is list:
            self.pixels = np.asarray(self.pixels)

        tifffile.imsave(self.path, self.pixels,
                        resolution=(1. / data.pixelSize * 10000, 1. / data.pixelSize * 10000, 'CENTIMETER'),
                        description=data.metadata)

        self.imageSavedSignal.emit()

def processImage(frame, imageViewer):
    if imageViewer.autoRange:
        minHist = frame.min()
        maxHist = frame.max()
    else:
        minHist = imageViewer.minHist
        maxHist = imageViewer.maxHist

    y = histogram1d(frame.ravel(), bins=maxHist-minHist, range=(minHist, maxHist))
    x = np.linspace(minHist, maxHist, maxHist-minHist)

    pix = array2Pixmap(frame, minHist, maxHist)
    return pix, x, y


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