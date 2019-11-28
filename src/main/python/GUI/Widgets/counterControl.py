# -*- coding: utf-8 -*-
"""
This widget displays allows to enable or disable live particule counting and to change the detection threshold.

Created on Thu Jul  11 10:33:40 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtWidgets
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

        self.checkBoxPreview = QtWidgets.QCheckBox('Show Particules')

        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addWidget(self.checkBox)
        self.mainLayout.addWidget(self.checkBoxPreview)

        self.checkBox.toggled.connect(self.changeCountState)
        self.checkBoxPreview.toggled.connect(self.togglePreview)
        self.spinBoxThreshold.valueChanged.connect(self.changeCount)

    def changeCountState(self):
        """
        Enables or disables live particule counting.
        """
        data.countingState = self.checkBox.isChecked()

    def togglePreview(self):
        """
        Activates or desactivates the preview of the particules on the image.
        """
        data.previewState = self.checkBoxPreview.isChecked()

    def changeCount(self):
        """
        Changes the detection threshold for the count function.
        """
        data.countThreshold = self.spinBoxThreshold.value()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    counterControl = QtWidgets.QWidget()
    ui = Ui_CounterControl()
    counterControl.show()
    app.exec_()
