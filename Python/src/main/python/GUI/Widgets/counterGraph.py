# -*- coding: utf-8 -*-
"""
This method displays a 2d plot containing an histogram.

Created on Thu Jul  9 15:02:20 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import pyqtgraph as pg


class Ui_CounterGraph(pg.GraphicsWindow):

    def __init__(self):
        super(Ui_CounterGraph, self).__init__()
        self.clear()
        self.p1 = self.addPlot()
        self.p1.plot([0, 0], [0, 0])
        self.data = self.p1.listDataItems()[0]

    def updateGraph(self, x, y):
        """Displays the updated graph in the plot area.
        :type x: 1d array
        :type y: 1d array
        """
        self.data.setData(x, y)
