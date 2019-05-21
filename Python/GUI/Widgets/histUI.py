# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:38:59 2019

@author: LEICACRYOCLEM
"""

import Modules.imageFunctions as imageFunctions
import GUI.Widgets.histPlot as histPlot
from PyQt5 import QtCore, QtWidgets
import numpy as np
import data

class Ui_Histogram(QtWidgets.QWidget):
    
    showFrame = QtCore.pyqtSignal(object, object, object)
    
    def setupUi(self, Form):
        self.histPlotter = histPlot.Ui_HistPlot()
        
        self.verticalLayoutWidgetHist = QtWidgets.QWidget(Form)
        self.verticalLayoutWidgetHist.setGeometry(QtCore.QRect(0, 0, 1250, 250))
        self.verticalLayoutWidgetHist.setObjectName("verticalLayoutWidgetHist")
        self.verticalLayoutHist = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetHist)
        self.verticalLayoutHist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHist.setObjectName("verticalLayoutHist")
        self.verticalLayoutHist.addWidget(self.histPlotter)
        
        self.labelMinimum = QtWidgets.QLabel(self.verticalLayoutWidgetHist)
        self.labelMinimum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMinimum.setObjectName("labelMinimum")
        self.verticalLayoutHist.addWidget(self.labelMinimum)
        
        self.horizontalSliderMinimum = QtWidgets.QSlider(self.verticalLayoutWidgetHist)
        self.horizontalSliderMinimum.setMaximum(65535)
        self.horizontalSliderMinimum.setProperty("value", 0)
        self.horizontalSliderMinimum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMinimum.setObjectName("horizontalSliderMinimum")
        self.labelMinimum.setText("Minimum")
        self.verticalLayoutHist.addWidget(self.horizontalSliderMinimum)
        
        self.labelMaximum = QtWidgets.QLabel(self.verticalLayoutWidgetHist)
        self.labelMaximum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMaximum.setObjectName("labelMaximum")
        self.labelMaximum.setText("Maximum")
        self.verticalLayoutHist.addWidget(self.labelMaximum)
        
        self.horizontalSliderMaximum = QtWidgets.QSlider(self.verticalLayoutWidgetHist)
        self.horizontalSliderMaximum.setMaximum(65535)
        self.horizontalSliderMaximum.setProperty("value", 65535)
        self.horizontalSliderMaximum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMaximum.setObjectName("horizontalSliderMaximum")
        self.verticalLayoutHist.addWidget(self.horizontalSliderMaximum)
        
        self.horizontalSliderMinimum.sliderMoved['int'].connect(self.setMinimum)
        self.horizontalSliderMaximum.sliderMoved['int'].connect(self.setMaximum)
      
    @QtCore.pyqtSlot()
    def setMinimum(self):
        data.histMin = self.horizontalSliderMinimum.value()
        if data.histMin > data.histMax:
            data.histMax = data.histMin
            self.horizontalSliderMaximum.setProperty("value", data.histMin)
            
        if data.isAcquiring==False and data.frame!=[] :
            self.showFrame.emit(data.frame, data.histX, data.histY)
        
    def setMaximum(self):
        data.histMax = self.horizontalSliderMaximum.value()
        if data.histMax < data.histMin:
            data.histMin = data.histMax
            self.horizontalSliderMinimum.setProperty("value", data.histMax)
            
        if data.isAcquiring==False and data.frame!=[]:
            self.showFrame.emit(data.frame, data.histX, data.histY)
            
    def updateHist(self, x, y):
        self.histPlotter.p1.clear()
        self.histPlotter.p1.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,0,255))