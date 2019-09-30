# -*- coding: utf-8 -*-
"""


Created on Thu Jul  11 10:33:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import data

class Ui_CounterControl(QtWidgets.QWidget):

    def __init__(self):
        super(Ui_CounterControl, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.labelThreshold = QtWidgets.QLabel('Threshold')
        self.spinBoxThreshold = QtWidgets.QSpinBox()
        self.spinBoxThreshold.setValue(80)
        self.spinBoxThreshold.setMinimum(0)
        self.spinBoxThreshold.setMaximum(65535)
        data.countThreshold = self.spinBoxThreshold.value()

        self.horizontalLayout.addWidget(self.labelThreshold)
        self.horizontalLayout.addWidget(self.spinBoxThreshold)

        self.checkBox = QtWidgets.QCheckBox('Count Particles')

        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addWidget(self.checkBox)

        self.checkBox.toggled.connect(self.changeCountState)
        self.spinBoxThreshold.valueChanged.connect(self.changeCount)

    def changeCountState(self):
        data.countingState = self.checkBox.isChecked()

    def changeCount(self):
        data.countThreshold = self.spinBoxThreshold.value()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    counterControl = QtWidgets.QWidget()
    ui = Ui_CounterControl()
    counterControl.show()
    app.exec_()
