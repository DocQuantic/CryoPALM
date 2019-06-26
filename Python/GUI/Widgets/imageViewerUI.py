# -*- coding: utf-8 -*-
"""
This widget allows to display a raw image in a GUI and to interact with it.
If allowed, it is possible to zoom on a part of the image that is selected by left clicking and draging on this portion of the image.
By right clicking, the zoom value is reset and we are back to the initial image.

This interaction can be done during live acquisition.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets, QtGui
import GUI.Widgets.imageDisplay as imageDisplay
import Modules.MM as MM
import data

class Ui_ImageViewer(QtWidgets.QWidget):
    
    #Initialization of the class
    def __init__(self):
        super(Ui_ImageViewer, self).__init__()
        
        #Create the graphics scene that will host the image pixmap to display
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.displayWindow = imageDisplay.Ui_ImageDispay()
        self.displayWindow.setMinimumSize(QtCore.QSize(1200, 1200))

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        
        self.pushButtonZoom = QtWidgets.QPushButton("Zoom")
        self.pushButtonZoom.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButtonZoom.setCheckable(True)
        self.pushButtonZoom.setChecked(False)
        
        self.pushButtonSetROI = QtWidgets.QPushButton("Set ROI")
        self.pushButtonSetROI.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButtonSetROI.setCheckable(True)
        self.pushButtonSetROI.setChecked(False)

        self.horizontalLayout.addWidget(self.pushButtonZoom)
        self.horizontalLayout.addWidget(self.pushButtonSetROI)

        self.mainLayout.addWidget(self.displayWindow)
        self.mainLayout.addLayout(self.horizontalLayout)
           
        self.pushButtonZoom.clicked.connect(self.handleZoom)
        self.pushButtonSetROI.clicked.connect(self.setROI)
        
        # Stack of QRectF zoom boxes in scene coordinates.
        self.zoomStack = []
        
        # Store a local handle to the scene's current image pixmap.
        self._pixmapHandle = None
     
    ######### Button interactions #########
    def handleZoom(self):
        """Sets the zoom on the image window active or inactive.
        """
        if self.pushButtonZoom.isChecked():
            data.canZoom = True
            if self.pushButtonSetROI.isChecked():
                self.pushButtonSetROI.setChecked(False)
                data.canSetROI = False
        else:
            data.canZoom = False
            
    def setROI(self):
        """Sets the ROI of the camera.
        If active, the ROI is set to a 256x256 pixels square area centered on the camera chip.
        When deactivated, it is set back to full chip.
        """
        if self.pushButtonSetROI.isChecked():
            data.changedBinning = True
            MM.setROI(896, 896, 256, 256)
        else:
            data.changedBinning = True
            MM.clearROI()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_ImageViewer()
    ui.show()
    app.exec_()