# -*- coding: utf-8 -*-
"""
This widget allows to run mosaic acquisitions.

Created on Wed Dec  11 17:41:12 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtWidgets, QtCore
import Modules.threads as threads
import data


class Ui_MosaicControl(QtWidgets.QWidget):

    initSpiralSignal = QtCore.pyqtSignal()
    stopSpiralSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_MosaicControl, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.runSpiralButton = QtWidgets.QPushButton("Run Spiral")
        self.runSpiralButton.setCheckable(True)

        self.verticalLayout.addWidget(self.runSpiralButton)

        self.mainLayout.addLayout(self.verticalLayout)

        self.isSpiralRunning = False

        self.runSpiralButton.clicked.connect(self.runSpiral)

    @QtCore.pyqtSlot()
    def runSpiral(self):
        """
        Runs a spiral acquisition.
        """
        if self.runSpiralButton.isChecked():
            self.initSpiralSignal.emit()
        else:
            self.stopSpiralSignal.emit()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    counterControl = QtWidgets.QWidget()
    ui = Ui_CounterControl()
    counterControl.show()
    app.exec_()