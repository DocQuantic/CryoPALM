# -*- coding: utf-8 -*-
"""
This file contains two classes implementing threads in the main program. 
Those threads allow for execution a an infinite (or not) while loop during the execution of the main program.
This way, we can continue to interact with other functionnalities of the program while acquisition is running.

Created on Wed Apr  3 15:30:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.acquisitionControlPALM as palmControl
from PyQt5 import QtCore, QtGui
from fast_histogram import histogram1d
import Modules.MM as MM
import numpy as np
import data
import time


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


class MovieThread(QtCore.QThread):
    """This class implements continuous frame acquisition and display.
    Each time a frame is acquired, the thread emits the data of the frame and of the computed histogram.
    """
    showFrame = QtCore.pyqtSignal(object, object, object, object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer

    @QtCore.pyqtSlot()
    def run(self):
        self.pix = QtGui.QPixmap()
        while True:
            frame = MM.getMovieFrame()
            
            if frame is not None and frame.shape[0] != 0:
                pix, x, y = processImage(frame, self.imageViewer)
                self.showFrame.emit(frame, pix, x, y)

            time.sleep(data.waitTime)


class PALMThread(QtCore.QThread):
    """This class implements PALM acquisition of a fixed amount of frames.
    Each time a series of 10 frames are acquired, the thread emits a signal for displaying the last frame and its histogram.
    At the end of the acquisition, a signal is emitted to tell the main the program that it finished.
    """
    showFrame = QtCore.pyqtSignal(object, object, object)
    stopPALM = QtCore.pyqtSignal()
    closeShutter = QtCore.pyqtSignal()
    acquisitionState = QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.imageNumber = 0
        self.frameStepShow = 10

    @QtCore.pyqtSlot()
    def run(self):
        self.palmStack = []
        idx = 0
        waitTime = MM.cameraAcquisitionTime()
        while idx < self.imageNumber:
            flag = str(idx+1) + "/" + str(self.imageNumber)
            self.acquisitionState.emit(flag)

            frame = MM.getMovieFrame()
            if frame is not None and frame.shape[0] != 0:
                self.palmStack.append(frame)
                
                if idx % self.frameStepShow == 0:
                    pix, x, y = processImage(frame)
                    self.showFrame.emit(pix, x, y)
                    
                idx += 1
                time.sleep(waitTime)

        self.closeShutter.emit()
        data.palmStack = np.array(self.palmStack)

        flag = "Saving"
        self.acquisitionState.emit(flag)

        palmControl.saveStack()
        self.stopPALM.emit()


class SequencePALMThread(QtCore.QThread):
    """This class implements PALM acquisition of a fixed amount of frames at different stage positions stored in data file.
    Each time a series of 10 frames are acquired, the thread emits a signal for displaying the last frame and its histogram.
    At the end of the acquisition, a signal is emitted to tell the main the program that it finished.
    """
    showFrame = QtCore.pyqtSignal(object, object, object)
    stopPALM = QtCore.pyqtSignal()
    closeShutter = QtCore.pyqtSignal()
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.imageNumber = 0
        self.frameStepShow = 10

    @QtCore.pyqtSlot()
    def run(self):
        waitTime = MM.cameraAcquisitionTime()
        for pos in data.stagePos:
            print(pos)
            self.palmStack = []
            idx = 0
            MM.setXYPos(pos[0], pos[1])
            MM.setZPos(pos[2])
            time.sleep(2)
            while idx < self.imageNumber:
                frame = MM.getMovieFrame()
                if frame is not None and frame.shape[0] != 0:
                    self.palmStack.append(frame)
                    
                    if idx % self.frameStepShow == 0: 
                        pix, x, y = processImage(frame)
                        self.showFrame.emit(pix, x, y)
                        
                    idx += 1
                    time.sleep(waitTime)

            self.closeShutter.emit()
            data.palmStack = np.array(self.palmStack)
            palmControl.saveStack()
            
        self.stopPALM.emit()


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