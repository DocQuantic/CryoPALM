# -*- coding: utf-8 -*-
"""
This widget adds control elements needed to change the display properties of an histogram.

Created on Tue May 21 10:38:59 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets


class Ui_Histogram(QtWidgets.QWidget):
    
    autoRangeSignal = QtCore.pyqtSignal(object)
    setMinSignal = QtCore.pyqtSignal(object)
    setMaxSignal = QtCore.pyqtSignal(object)
    autoRange = False
    
    def __init__(self):
        super(Ui_Histogram, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")
        
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

        self.horizontalLayoutSliders.addWidget(self.sliderMinimum)
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
        
        self.sliderMinimum.valueChanged['int'].connect(self.setMinimum)
        self.sliderMaximum.valueChanged['int'].connect(self.setMaximum)
        self.sliderMinimum.valueChanged['int'].connect(self.spinBoxMin.setValue)
        self.sliderMaximum.valueChanged['int'].connect(self.spinBoxMax.setValue)
        self.spinBoxMin.valueChanged['int'].connect(self.sliderMinimum.setValue)
        self.spinBoxMax.valueChanged['int'].connect(self.sliderMaximum.setValue)
        self.pushButtonAuto.clicked.connect(self.autoRange)
        
    def switchAuto(self):
        """
        Disables the automatic histogram range selection.
        """
        if self.autoRange:
            self.autoRange = False
            self.pushButtonAuto.setChecked(False)
    
    def autoRange(self):
        """
        Enables the automatic histogram range selection.
        """
        self.autoRange = self.pushButtonAuto.isChecked()
        self.autoRangeSignal.emit(self.autoRange)
    
    @QtCore.pyqtSlot()
    def setMinimum(self):
        """
        Sets the minimum value of the histogram display range.
        """
        self.setMinSignal.emit(self.sliderMinimum.value())
        if self.sliderMinimum.value() >= self.sliderMaximum.value()-1:
            self.sliderMaximum.setProperty("value", self.sliderMinimum.value()+1)
            self.spinBoxMax.setValue(self.sliderMinimum.value()+1)
    
    @QtCore.pyqtSlot()
    def setMaximum(self):
        """
        Sets the maximum value of the histogram display range.
        """
        self.setMaxSignal.emit(self.sliderMaximum.value())
        if self.sliderMaximum.value() <= self.sliderMinimum.value()+1:
            self.sliderMinimum.setProperty("value", self.sliderMaximum.value()-1)
            self.spinBoxMin.setValue(self.sliderMaximum.value()-1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Histogram()
    ui.show()
    app.exec_()
