# -*- coding: utf-8 -*-
"""
This widget allows to display a raw image in a GUI and to interact with it.
If allowed, it is possible to zoom on a part of the image that is selected by left clicking and draging on this portion of the image.
By right clicking, the zoom value is reset and we are back to the initial image.

This interaction can be done during live acquisition.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import GUI.Widgets.imageDisplay as imageDisplay
import Modules.MM as MM
import data

class Ui_ImageViewer(QtWidgets.QWidget):
    
    #Initialization of the class
    def setupUi(self, Form):
        
        #Create the graphics scene that will host the image pixmap to display
        self.displayWindow = imageDisplay.Ui_ImageDispay()
        
        self.horizontalLayoutWidgetImage = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidgetImage.setGeometry(QtCore.QRect(10, 10, 1200, 1200))
        self.horizontalLayoutWidgetImage.setObjectName("horizontalLayoutWidgetImage")
        self.horizontalLayoutImage = QtWidgets.QHBoxLayout(self.horizontalLayoutWidgetImage)
        self.horizontalLayoutImage.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutImage.setObjectName("horizontalLayoutImage")
        
        self.horizontalLayoutImage.addWidget(self.displayWindow)
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 1200, 150, 100))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.pushButtonZoom = QtWidgets.QPushButton(Form)
        self.pushButtonZoom.setObjectName("pushButtonZoom")
        self.pushButtonZoom.setCheckable(True)
        self.pushButtonZoom.setChecked(False)
        self.pushButtonZoom.setText("Zoom")
        self.horizontalLayout.addWidget(self.pushButtonZoom)
        
        self.pushButtonSetROI = QtWidgets.QPushButton(Form)
        self.pushButtonSetROI.setObjectName("pushButtonSetROI")
        self.pushButtonSetROI.setCheckable(True)
        self.pushButtonSetROI.setChecked(False)
        self.pushButtonSetROI.setText("Set ROI")
        self.horizontalLayout.addWidget(self.pushButtonSetROI)
           
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
            data.canZoom=True
            if self.pushButtonSetROI.isChecked():
                self.pushButtonSetROI.setCheked(False)
                data.canSetROI=False
        else:
            data.canZoom=False
            
    def setROI(self):
        """Sets the ROI of the camera.
        If active, the ROI is set to a 256x256 pixels square area centered on the camera chip.
        When deactivated, it is set back to full chip.
        """
        if self.pushButtonSetROI.isChecked():
#            data.canSetROI=True
            data.changedBinning=True
#            if self.pushButtonZoom.isChecked():
#                self.pushButtonZoom.setChecked(False)
#                data.canZoom=False
            MM.setROI(896, 896, 256, 256)
        else:
#            data.canSetROI=False
            data.changedBinning=True
            MM.clearROI()