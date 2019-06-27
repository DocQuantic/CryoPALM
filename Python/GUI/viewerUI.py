# -*- coding: utf-8 -*-
"""
This file contains the UI code for image viewer window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 26 16:31:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.histCommands as histCommands
import GUI.Widgets.imageViewerUI as imageViewerUI
import GUI.Widgets.histPlot as histPlot
from PyQt5 import QtWidgets, QtCore


class Ui_Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        """Setups all the elements positions and connections with functions
        """
        super(Ui_Viewer, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)

        #Image Display Widget
        self.imageDisplay = imageViewerUI.Ui_ImageViewer()

        #Histogram Commands Widget
        self.histogramCommands = histCommands.Ui_Histogram()

        #Histogram display Widget
        self.histogramDisplay = histPlot.Ui_HistPlot()
        self.histogramDisplay.setMinimumSize(QtCore.QSize(0, 120))

        self.mainLayout.addWidget(self.histogramCommands, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.imageDisplay, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.histogramDisplay, 1, 1, 1, 1)

        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Image Viewer")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Viewer()
    ui.show()
    app.exec_()