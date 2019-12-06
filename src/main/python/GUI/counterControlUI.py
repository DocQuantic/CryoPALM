# -*- coding: utf-8 -*-
"""
This file contains the UI code for the particule counter control window.

Created on Tue Jul 11 10:46:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.counterControl as counterControl
from PyQt5 import QtWidgets, QtCore


class Ui_CounterControl(QtWidgets.QMainWindow):

    clearMarksSignal = QtCore.pyqtSignal()
    showMarksSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_CounterControl, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.counterControlWidget = counterControl.Ui_CounterControl()

        self.mainLayout.addWidget(self.counterControlWidget)

        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("PyTracer")

        self.counterControlWidget.checkBoxPreview.clicked.connect(self.handleMarks)

    @QtCore.pyqtSlot()
    def handleMarks(self):
        if self.counterControlWidget.checkBoxPreview.isChecked() is not True:
            self.clearMarksSignal.emit()
        else:
            self.showMarksSignal.emit()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_CounterControl()
    ui.show()
    app.exec_()
