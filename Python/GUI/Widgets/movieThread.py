# -*- coding: utf-8 -*-
"""
This file contains two classes implementing threads in the main program. 
Those threads allow for execution a an infinite (or not) while loop during the execution of the main program.
This way, we can continue to interact with other functionnalities of the program while acquisition is running.

Created on Wed Apr  3 15:30:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import GUI.Widgets.PALMAcquisitionControl as palmControl
from Modules.imageFunctions import array2Pixmap
from PyQt5 import QtCore, QtGui
import Modules.MM as MM
import numpy as np
import data
import time


def processImage(frame):
    y, x = np.histogram(frame.ravel(), bins=np.linspace(data.histMin, data.histMax, data.histMax-data.histMin))
    pix = array2Pixmap(frame)
    data.frame = frame
    data.histX = x
    data.histY = y
    return pix, x, y


class MovieThread(QtCore.QThread):
    """This class implements continuous frame acquisition and display.
    Each time a frame is acquired, the thread emits the data of the frame and of the computed histogram.
    """
    showFrame = QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer

    @QtCore.pyqtSlot()
    def run(self):
        self.pix = QtGui.QPixmap()
        waitTime = MM.cameraAcquisitionTime()
        while True:
            frame = MM.getMovieFrame()
            
            if frame is not None and frame.shape[0] != 0:
                pix, x, y = processImage(frame)
                self.showFrame.emit(pix, x, y)

            time.sleep(waitTime)


class PALMThread(QtCore.QThread):
    """This class implements PALM acquisition of a fixed amount of frames.
    Each time a series of 10 frames are acquired, the thread emits a signal for displaying the last frame and its histogram.
    At the end of the acquisition, a signal is emitted to tell the main the program that it finished.
    """
    showFrame = QtCore.pyqtSignal(object, object, object)
    stopPALM = QtCore.pyqtSignal()
    closeShutter = QtCore.pyqtSignal()
    acquisitionState = QtCore.pyqtSignal(object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer
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
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer
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
