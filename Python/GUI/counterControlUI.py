# -*- coding: utf-8 -*-
"""

Created on Tue Jul 111 10:46:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.counterControl as counterControl
from PyQt5 import QtWidgets

class Ui_CounterControl(QtWidgets.QMainWindow):

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

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_CounterControl()
    ui.show()
    app.exec_()