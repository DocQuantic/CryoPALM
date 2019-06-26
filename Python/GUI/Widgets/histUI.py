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

        self.histPlotter = histPlot.Ui_HistPlot()
        self.histPlotter.setMinimumSize(QtCore.QSize(0,120))

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        
        self.spinBoxMin = QtWidgets.QSpinBox()
        self.spinBoxMin.setMaximum(65535)
        self.spinBoxMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMin.setMinimumSize(QtCore.QSize(70, 30))
        
        self.verticalLayoutSliders = QtWidgets.QVBoxLayout()
        
        self.labelMinimum = QtWidgets.QLabel("Minimum")
        self.labelMinimum.setAlignment(QtCore.Qt.AlignCenter)
        
        self.horizontalSliderMinimum = QtWidgets.QSlider()
        self.horizontalSliderMinimum.setMaximum(65535)
        self.horizontalSliderMinimum.setOrientation(QtCore.Qt.Horizontal)
        
        self.labelMaximum = QtWidgets.QLabel("Maximum")
        self.labelMaximum.setAlignment(QtCore.Qt.AlignCenter)
        
        self.horizontalSliderMaximum = QtWidgets.QSlider()
        self.horizontalSliderMaximum.setMaximum(65535)
        self.horizontalSliderMaximum.setProperty("value", 65535)
        self.horizontalSliderMaximum.setOrientation(QtCore.Qt.Horizontal)

        self.verticalLayoutSliders.addWidget(self.labelMinimum)
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMinimum)
        self.verticalLayoutSliders.addWidget(self.labelMaximum)
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMaximum)
        
        self.spinBoxMax = QtWidgets.QSpinBox()
        self.spinBoxMax.setMaximum(65535)
        self.spinBoxMax.setValue(65535)
        self.spinBoxMax.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBoxMax.setMinimumSize(QtCore.QSize(70, 30))
        
        self.pushButtonAuto = QtWidgets.QPushButton("Auto")
        self.pushButtonAuto.setCheckable(True)
        self.pushButtonAuto.setMinimumSize(QtCore.QSize(70, 40))

        self.horizontalLayout.addWidget(self.spinBoxMin)
        self.horizontalLayout.addLayout(self.verticalLayoutSliders)
        self.horizontalLayout.addWidget(self.spinBoxMax)
        self.horizontalLayout.addWidget(self.pushButtonAuto)

        self.mainLayout.addWidget(self.histPlotter)
        self.mainLayout.addLayout(self.horizontalLayout)
        
        self.horizontalSliderMinimum.valueChanged['int'].connect(self.setMinimum)
        self.horizontalSliderMaximum.valueChanged['int'].connect(self.setMaximum)
        self.horizontalSliderMinimum.sliderMoved['int'].connect(self.switchAuto)
        self.horizontalSliderMaximum.sliderMoved['int'].connect(self.switchAuto)
        self.horizontalSliderMinimum.valueChanged['int'].connect(self.spinBoxMin.setValue)
        self.horizontalSliderMaximum.valueChanged['int'].connect(self.spinBoxMax.setValue)
        self.spinBoxMin.valueChanged['int'].connect(self.horizontalSliderMinimum.setValue)
        self.spinBoxMax.valueChanged['int'].connect(self.horizontalSliderMaximum.setValue)
        self.pushButtonAuto.clicked.connect(self.autoRange)
        
    def switchAuto(self):
        if data.autoRange:
            data.autoRange = False
            self.pushButtonAuto.setChecked(False)
    
    def autoRange(self):
        data.autoRange = self.pushButtonAuto.isChecked()
        
        if data.autoRange==True and data.isAcquiring==False and data.frame!=[]:
            self.showFrame.emit(data.frame, data.histX, data.histY)
    
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
        if data.autoRange:
            self.horizontalSliderMinimum.setValue(data.histMin)
            self.spinBoxMin.setValue(data.histMin)
            self.horizontalSliderMaximum.setValue(data.histMax)
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