# -*- coding: utf-8 -*-
"""
This method displays a 2d plot containing an histogram.

Created on Tue Apr  9 15:18:20 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import pyqtgraph as pg


class  Ui_HistPlot(pg.GraphicsWindow):
    pg.setConfigOption('background', (0,0,0,0))
    pg.setConfigOption('foreground', 'k')
    
    def __init__(self):
        super(Ui_HistPlot, self).__init__()
        self.p1 = self.addPlot()

    def updateHist(self, x, y):
        """
        Displays the histogram in the plot area.
        :param x: 1d array
        :paraam y: 1d array
        """
        self.p1.clear()
        self.p1.plot(x, y, stepMode=False, fillLevel=0, brush=(0,0,0,255))
