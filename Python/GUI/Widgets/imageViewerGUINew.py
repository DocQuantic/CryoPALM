# -*- coding: utf-8 -*-
"""
This widget allows to display a raw image in a GUI and to interact with it.
If allowed, it is possible to zoom on a part of the image that is selected by left clicking and draging on this portion of the image.
By right clicking, the zoom value is reset and we are back to the initial image.

This interaction can be done during live acquisition.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.MM as MM
import data

class Ui_ImageViewer(object):
    
    #Initialization of the class
    def setupUi(self, Form):
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 1200, 1200))
        self.graphicsView.setObjectName("graphicsView")
        
        #Create the graphics scene that will host the image pixmap to display
        self.imageScene = QtWidgets.QGraphicsScene(Form)
        self.graphicsView.setStyleSheet("background: transparent")
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setScene(self.imageScene)
        
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
            data.canSetROI=True
            if self.pushButtonZoom.isChecked():
                self.pushButtonZoom.setChecked(False)
                data.canZoom=False
            MM.setROI(896, 896, 256, 256)
        else:
            data.canSetROI=False
            MM.clearROI()
        
    ######### Image viewer functions #########
    def hasImage(self):
        """ Returns whether or not the scene contains an image pixmap.
        """
        return self._pixmapHandle is not None
    
    def clearImage(self):
        """ Removes the current image pixmap from the scene if it exists.
        """
        if self.hasImage():
            self.imageScene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def pixmap(self):
        """ Returns the scene's current image pixmap as a QPixmap, or else None if no image exists.
        :rtype: QPixmap | None
        """
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None
    
    def setImage(self, pixmap):
        """ Set the scene's current image pixmap to the input QPixmap.
        The zoom value is conserved from the previous displayed image unless the image format changed (binning).
        :type image: QPixmap
        """
        
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.imageScene.addPixmap(pixmap)
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)
            
        if data.changedBinning:
            self.graphicsView.setSceneRect(QtCore.QRectF(pixmap.rect()))
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)
            data.changedBinning = False
            
    def mousePressEvent(self, event):
        """ Start or reset mouse zoom mode (left or right button clicked)
        """
        print("Press mouse")
        if data.canZoom:
            if event.button() == QtCore.Qt.LeftButton:
                self.graphicsView.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            elif event.button() == QtCore.Qt.RightButton:
                self.zoomStack = []
                self.updateViewer()
        QtWidgets.QGraphicsView.mousePressEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        """ Stop mouse zoom mode and apply zoom if valid.
        """
        print("Release mouse")
        
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        if data.canZoom:
            if event.button() == QtCore.Qt.LeftButton:
                viewBBox = self.zoomStack[-1] if len(self.zoomStack) else self.graphicsView.sceneRect()
                selectionBBox = self.imageScene.selectionArea().boundingRect().intersected(viewBBox)
                self.imageScene.setSelectionArea(QtGui.QPainterPath())  # Clear current selection area.
                if selectionBBox.isValid() and (selectionBBox != viewBBox):
                    self.zoomStack.append(selectionBBox)
                    self.updateViewer()
                
    def updateViewer(self):
        """ Show current zoom (if showing entire image, apply current aspect ratio mode).
        """
        
        if not self.hasImage():
            return
        if len(self.zoomStack) and self.graphicsView.sceneRect().contains(self.zoomStack[-1]):
            self.graphicsView.fitInView(self.zoomStack[-1], QtCore.Qt.KeepAspectRatio)  # Show zoomed rect (ignore aspect ratio).
        else:
            self.zoomStack = []  # Clear the zoom stack (in case we got here because of an invalid zoom).
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)  # Show entire image (use current aspect ratio mode).