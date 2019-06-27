# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:38:59 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

# import histPlot
import GUI.Widgets.histPlot as histPlot
from PyQt5 import QtCore, QtWidgets, QtGui
import data

class Ui_Histogram(QtWidgets.QWidget):
    
    showFrame = QtCore.pyqtSignal(object, object, object)
    
    def __init__(self):
        super(Ui_Histogram, self).__init__()
        # self.mainLayout = QtWidgets.QVBoxLayout(self)
        
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        
        self.spinBoxMin = QtWidgets.QSpinBox()
        self.spinBoxMin.setMaximum(65535)
        self.spinBoxMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMin.setMinimumSize(QtCore.QSize(70, 30))
        
        self.horizontalLayoutSliders = QtWidgets.QHBoxLayout()
        
        self.labelMinimum = QtWidgets.QLabel("Minimum")
        self.labelMinimum.setAlignment(QtCore.Qt.AlignCenter)
        
        self.sliderMinimum = QtWidgets.QSlider()
        self.sliderMinimum.setMaximum(65535)
        
        self.labelMaximum = QtWidgets.QLabel("Maximum")
        self.labelMaximum.setAlignment(QtCore.Qt.AlignCenter)
        
        self.sliderMaximum = QtWidgets.QSlider()
        self.sliderMaximum.setMaximum(65535)
        self.sliderMaximum.setProperty("value", 65535)

        # self.verticalLayoutSliders.addWidget(self.labelMinimum)
        self.horizontalLayoutSliders.addWidget(self.sliderMinimum)
        # self.verticalLayoutSliders.addWidget(self.labelMaximum)
        self.horizontalLayoutSliders.addWidget(self.sliderMaximum)
        
        self.spinBoxMax = QtWidgets.QSpinBox()
        self.spinBoxMax.setMaximum(65535)
        self.spinBoxMax.setValue(65535)
        self.spinBoxMax.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMax.setMinimumSize(QtCore.QSize(70, 30))
        
        self.pushButtonAuto = QtWidgets.QPushButton("Auto")
        self.pushButtonAuto.setCheckable(True)
        self.pushButtonAuto.setMinimumSize(QtCore.QSize(70, 40))

        self.mainLayout.addWidget(self.spinBoxMax)
        self.mainLayout.addLayout(self.horizontalLayoutSliders)
        self.mainLayout.addWidget(self.spinBoxMin)
        self.mainLayout.addWidget(self.pushButtonAuto)

        # self.mainLayout.addWidget(self.histPlotter)
        # self.mainLayout.addLayout(self.horizontalLayout)
        
        self.sliderMinimum.valueChanged['int'].connect(self.setMinimum)
        self.sliderMaximum.valueChanged['int'].connect(self.setMaximum)
        self.sliderMinimum.sliderMoved['int'].connect(self.switchAuto)
        self.sliderMaximum.sliderMoved['int'].connect(self.switchAuto)
        self.sliderMinimum.valueChanged['int'].connect(self.spinBoxMin.setValue)
        self.sliderMaximum.valueChanged['int'].connect(self.spinBoxMax.setValue)
        self.spinBoxMin.valueChanged['int'].connect(self.sliderMinimum.setValue)
        self.spinBoxMax.valueChanged['int'].connect(self.sliderMaximum.setValue)
        self.pushButtonAuto.clicked.connect(self.autoRange)
        
    def switchAuto(self):
        if data.autoRange:
            data.autoRange = False
            self.pushButtonAuto.setChecked(False)
    
    def autoRange(self):
        data.autoRange = self.pushButtonAuto.isChecked()
        
        if data.autoRange == True and data.isAcquiring == False and data.frame != []:
            self.showFrame.emit(data.frame, data.histX, data.histY)
    
    @QtCore.pyqtSlot()
    def setMinimum(self):
        data.histMin = self.sliderMinimum.value()
        if data.histMin > data.histMax:
            data.histMax = data.histMin
            self.sliderMaximum.setProperty("value", data.histMin)
            self.spinBoxMax.setValue(data.histMin)
            
        if data.isAcquiring==False and data.frame!=[] :
            self.showFrame.emit(data.frame, data.histX, data.histY)
    
    @QtCore.pyqtSlot()
    def setMaximum(self):
        data.histMax = self.sliderMaximum.value()
        if data.histMax < data.histMin:
            data.histMin = data.histMax
            self.sliderMinimum.setProperty("value", data.histMax)
            self.spinBoxMin.setValue(data.histMax)
            
        if data.isAcquiring==False and data.frame!=[]:
            self.showFrame.emit(data.frame, data.histX, data.histY)
            
    def updateHist(self, x, y):
        if data.autoRange:
            self.sliderMinimum.setValue(data.histMin)
            self.spinBoxMin.setValue(data.histMin)
            self.sliderMaximum.setValue(data.histMax)
            self.spinBoxMax.setValue(data.histMax)
        self.histPlotter.p1.clear()
        self.histPlotter.p1.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,0,255))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Histogram()
    ui.show()
    app.exec_()