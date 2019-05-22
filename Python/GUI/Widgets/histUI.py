# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:38:59 2019

@author: LEICACRYOCLEM
"""

import GUI.Widgets.histPlot as histPlot
from PyQt5 import QtCore, QtWidgets, QtGui
import data

class Ui_Histogram(QtWidgets.QWidget):
    
    showFrame = QtCore.pyqtSignal(object, object, object)
    
    def setupUi(self, Form):
        
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        
        self.histPlotter = histPlot.Ui_HistPlot()
        
        self.verticalLayoutWidgetHist = QtWidgets.QWidget(Form)
        self.verticalLayoutWidgetHist.setGeometry(QtCore.QRect(0, 0, 1250, 250))
        self.verticalLayoutWidgetHist.setObjectName("verticalLayoutWidgetHist")
        self.verticalLayoutHist = QtWidgets.QVBoxLayout(self.verticalLayoutWidgetHist)
        self.verticalLayoutHist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutHist.setObjectName("verticalLayoutHist")
        self.verticalLayoutHist.addWidget(self.histPlotter)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.spinBoxMin = QtWidgets.QSpinBox(self.verticalLayoutWidgetHist)
        self.spinBoxMin.setObjectName("spinBoxMin")
#        self.spinBoxMin.setReadOnly(True)
        self.spinBoxMin.setMaximum(65535)
        self.spinBoxMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMin.setMinimumSize(QtCore.QSize(70, 30))
        self.spinBoxMin.setFont(font)
        self.horizontalLayout.addWidget(self.spinBoxMin)
        
        self.verticalLayoutSliders = QtWidgets.QVBoxLayout()
        self.verticalLayoutSliders.setObjectName("verticalLayoutSliders")
        
        self.labelMinimum = QtWidgets.QLabel(self.verticalLayoutWidgetHist)
        self.labelMinimum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMinimum.setObjectName("labelMinimum")
        self.labelMinimum.setText("Minimum")
        self.labelMinimum.setFont(font)
        self.verticalLayoutSliders.addWidget(self.labelMinimum)
        
        self.horizontalSliderMinimum = QtWidgets.QSlider(self.verticalLayoutWidgetHist)
        self.horizontalSliderMinimum.setMaximum(65535)
        self.horizontalSliderMinimum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMinimum.setObjectName("horizontalSliderMinimum")
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMinimum)
        
        self.labelMaximum = QtWidgets.QLabel(self.verticalLayoutWidgetHist)
        self.labelMaximum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMaximum.setObjectName("labelMaximum")
        self.labelMaximum.setFont(font)
        self.verticalLayoutSliders.addWidget(self.labelMaximum)
        
        self.horizontalSliderMaximum = QtWidgets.QSlider(self.verticalLayoutWidgetHist)
        self.horizontalSliderMaximum.setMaximum(65535)
        self.horizontalSliderMaximum.setProperty("value", 65535)
        self.horizontalSliderMaximum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMaximum.setObjectName("horizontalSliderMaximum")
        self.labelMaximum.setText("Maximum")
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMaximum)

        self.horizontalLayout.addLayout(self.verticalLayoutSliders)
        
        self.spinBoxMax = QtWidgets.QSpinBox(self.verticalLayoutWidgetHist)
        self.spinBoxMax.setObjectName("spinBoxMax")
#        self.spinBoxMax.setReadOnly(True)
        self.spinBoxMax.setMaximum(65535)
        self.spinBoxMax.setValue(65535)
        self.spinBoxMax.setFont(font)
        self.spinBoxMax.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMax.setMinimumSize(QtCore.QSize(70, 30))
        self.horizontalLayout.addWidget(self.spinBoxMax)
        
        self.pushButtonAuto = QtWidgets.QPushButton(self.verticalLayoutWidgetHist)
        self.pushButtonAuto.setObjectName("pushButtonAuto")
        self.pushButtonAuto.setText("Auto")
        self.pushButtonAuto.setFont(font)
        self.pushButtonAuto.setMinimumSize(QtCore.QSize(70, 40))
        self.horizontalLayout.addWidget(self.pushButtonAuto)
        
        self.verticalLayoutHist.addLayout(self.horizontalLayout)
        
        self.horizontalSliderMinimum.valueChanged['int'].connect(self.setMinimum)
        self.horizontalSliderMaximum.valueChanged['int'].connect(self.setMaximum)
        self.horizontalSliderMinimum.valueChanged['int'].connect(self.spinBoxMin.setValue)
        self.horizontalSliderMaximum.valueChanged['int'].connect(self.spinBoxMax.setValue)
        self.spinBoxMin.valueChanged['int'].connect(self.horizontalSliderMinimum.setValue)
        self.spinBoxMax.valueChanged['int'].connect(self.horizontalSliderMaximum.setValue)
#        self.pushButtonAuto.clicked.connect(self.autoRange)
      
    @QtCore.pyqtSlot()
    def setMinimum(self):
        data.histMin = self.horizontalSliderMinimum.value()
        if data.histMin > data.histMax:
            data.histMax = data.histMin
            self.horizontalSliderMaximum.setProperty("value", data.histMin)
            self.spinBoxMax.setValue(data.histMin)
            
        if data.isAcquiring==False and data.frame!=[] :
            self.showFrame.emit(data.frame, data.histX, data.histY)
    
    @QtCore.pyqtSlot()
    def setMaximum(self):
        data.histMax = self.horizontalSliderMaximum.value()
        if data.histMax < data.histMin:
            data.histMin = data.histMax
            self.horizontalSliderMinimum.setProperty("value", data.histMax)
            self.spinBoxMin.setValue(data.histMax)
            
        if data.isAcquiring==False and data.frame!=[]:
            self.showFrame.emit(data.frame, data.histX, data.histY)
            
    def updateHist(self, x, y):
        self.histPlotter.p1.clear()
        self.histPlotter.p1.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,0,255))