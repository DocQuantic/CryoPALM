# -*- coding: utf-8 -*-
"""
This file contains two classes implementing threads in the main program. 
Those threads allow for execution a an infinite (or not) while loop during the execution of the main program.
This way, we can continue to interact with other functionnalities of the program while acquisition is running.

Created on Wed Apr  3 15:30:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui
import Modules.MM as MM
import numpy as np
import data
import time

class MovieThread(QtCore.QThread):
    """This class implements continuous frame acquisition and display.
    Each time a frame is acquired, the thread emits the data of the frame and of the computed histogram.
    """
    loop = QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer
        self.pix = QtGui.QPixmap()
        self.x = []
        self.y = []

    @QtCore.pyqtSlot()
    def run(self):
        self.pix = QtGui.QPixmap()
        self.x = []
        self.y = []
        waitTime = MM.cameraAcquisitionTime()
        while True:
            frame = MM.getMovieFrame()
            data.frame = frame
            
            if frame is not None:
                img8 = ((frame - frame.min()) / (frame.ptp() / 255.0)).astype(np.uint8)
                img = QtGui.QImage(img8, img8.shape[0], img8.shape[1], QtGui.QImage.Format_Grayscale8)
                self.pix = QtGui.QPixmap(img)
                
                self.y, self.x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 10000))
                self.loop.emit(self.pix, self.x, self.y)
            
            time.sleep(waitTime)
            
class PALMThread(QtCore.QThread):
    """This class implements PALM acquisition of a fixed amount of frames.
    Each time a series of 10 frames are acquired, the thread emits a signal for displaying the last frame and its histogram.
    At the end of the acquisition, a signal is emitted to tell the main the program that it finished.
    """
    showFrame = QtCore.pyqtSignal(object, object, object)
    stopPALM = QtCore.pyqtSignal()
    
    def __init__(self, imageViewer):
        QtCore.QThread.__init__(self)
        self.imageViewer = imageViewer
        self.pix = QtGui.QPixmap()
        self.x = []
        self.y = []
        self.imageNumber = 0
        self.frameStepShow = 10

    @QtCore.pyqtSlot()
    def run(self):
        self.pix = QtGui.QPixmap()
        self.x = []
        self.y = []
        self.palmStack = []
        idx = 0
        waitTime = MM.cameraAcquisitionTime()
        while idx < self.imageNumber:
            frame = MM.getMovieFrame()
            if frame is not None and frame.size != 0:
                self.palmStack.append(frame)
                
                if idx % self.frameStepShow == 0:
                    img8 = ((frame - frame.min()) / (frame.ptp() / 255.0)).astype(np.uint8)
                    img = QtGui.QImage(img8, img8.shape[0], img8.shape[1], QtGui.QImage.Format_Grayscale8)
                    self.pix = QtGui.QPixmap(img)
                    
                    self.y, self.x = np.histogram(frame.ravel(), bins=np.linspace(0, 65535, 10000))
                    self.showFrame.emit(self.pix, self.x, self.y)
                    
                idx+=1
                time.sleep(waitTime)
        
        data.palmStack = np.array(self.palmStack)
#        data.palmStack = np.swapaxes(data.palmStack, 0, 2)
#        data.palmStack = np.swapaxes(data.palmStack, 0, 1)
#        data.palmStack = np.expand_dims(data.palmStack, 2)
#        data.palmStack = np.expand_dims(data.palmStack, 3)
        self.stopPALM.emit()