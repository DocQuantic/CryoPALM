# -*- coding: utf-8 -*-
"""
This file contains the UI code for the experiment control window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 25 14:11:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.AutoFocus as autoFocus
from PyQt5 import QtWidgets


class Ui_AutoFocus(QtWidgets.QMainWindow):

    def __init__(self):
        """Setups all the elements positions and connectionss with functions
        """
        super(Ui_AutoFocus, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        #Lasers control Widget
        self.autoFocus = autoFocus.Ui_AutoFocus()

        self.mainLayout.addWidget(self.autoFocus)

        self.setCentralWidget(self.centralWidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_AutoFocus()
    ui.show()
    app.exec_()