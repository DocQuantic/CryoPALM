# -*- coding: utf-8 -*-
"""
This file contains the UI code for image viewer window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 26 16:31:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.histUI as histUI
import GUI.Widgets.imageViewerUI as imageViewerUI
from PyQt5 import QtWidgets


class Ui_Viewer(QtWidgets.QMainWindow):

    def __init__(self):
        """Setups all the elements positions and connections with functions
        """
        super(Ui_Viewer, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        #Image Display Widget
        self.imageDisplay = imageViewerUI.Ui_ImageViewer()

        #Histogram Display Widget
        self.histogramDisplay = histUI.Ui_Histogram()

        self.mainLayout.addWidget(self.imageDisplay)
        self.mainLayout.addWidget(self.histogramDisplay)

        self.setCentralWidget(self.centralWidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Viewer()
    ui.show()
    app.exec_()