# -*- coding: utf-8 -*-
"""

Created on Thu Jul  11 11:20:20 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import pyqtgraph as pg
from PyQt5 import QtWidgets

class Ui_CounterGraph(QtWidgets.QMainWindow):
    x = []
    y = []

    def __init__(self):
        super(Ui_CounterGraph, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.graphWidget = pg.PlotWidget()
        self.plotItem = self.graphWidget.getPlotItem()

        self.mainLayout.addWidget(self.graphWidget)

        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle("Particules count")

    def updateGraph(self, count, idx):
        self.x.append(idx)
        self.y.append(count)

        self.plotItem.clear()
        self.plotItem.plot(self.x, self.y)

        # print(idx)
        # print(count)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_CounterGraph()
    ui.show()
    app.exec_()