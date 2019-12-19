# -*- coding: utf-8 -*-
"""
This file contains the UI code for the particule counter control window.

Created on Wed Dec 11 18:04:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.mosaic as mosaic
from PyQt5 import QtWidgets, QtCore


class Ui_MosaicControl(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MosaicControl, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.mosaicControlWidget = mosaic.Ui_MosaicControl()

        self.mainLayout.addWidget(self.mosaicControlWidget)

        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("Mosaic")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_CounterControl()
    ui.show()
    app.exec_()
