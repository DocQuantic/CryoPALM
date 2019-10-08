# -*- coding: utf-8 -*-
"""
This widget allows to display a raw image in a GUI.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import data


class Ui_ImageDispay(QtWidgets.QGraphicsView):
    
    # Initialization of the class
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)
        
        # Create the graphics scene that will host the image pixmap to display
        self.imageScene = QtWidgets.QGraphicsScene()
        self.setObjectName("graphicsView")
        self.setStyleSheet("background: black")
        self.setScene(self.imageScene)
        
        # Stack of QRectF zoom boxes in scene coordinates.
        self.zoomStack = []
        
        # Store a local handle to the scene's current image pixmap.
        self._pixmapHandle = None
        
    # Image viewer functions
    def hasImage(self):
        """
        Returns whether or not the scene contains an image pixmap.
        """
        return self._pixmapHandle is not None
    
    def clearImage(self):
        """
        Removes the current image pixmap from the scene if it exists.
        """
        if self.hasImage():
            self.imageScene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def pixmap(self):
        """
        Returns the scene's current image pixmap as a QPixmap, or else None if no image exists.
        :return: QPixmap | None
        """
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None
    
    def setImage(self, pixmap):
        """
        Sets the scene's current image pixmap to the input QPixmap.
        The zoom value is conserved from the previous displayed image unless the image format changed (binning).
        :param pixmap: QPixmap
        """
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.imageScene.addPixmap(pixmap)
            self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
            
        if data.changedBinning:
            self.setSceneRect(QtCore.QRectF(pixmap.rect()))
            self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
            data.changedBinning = False
            
    def mousePressEvent(self, event):
        """
        Starts or reset mouse zoom mode (left or right button clicked).
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        elif event.button() == QtCore.Qt.RightButton:
            self.zoomStack = []
            self.updateViewer()
        QtWidgets.QGraphicsView.mousePressEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        """
        Stops mouse zoom mode and apply zoom if valid.
        """
        if event.button() == QtCore.Qt.LeftButton:
            viewBBox = self.zoomStack[-1] if len(self.zoomStack) else self.sceneRect()
            selectionBBox = self.imageScene.selectionArea().boundingRect().intersected(viewBBox)
            self.imageScene.setSelectionArea(QtGui.QPainterPath())  # Clear current selection area.
            if selectionBBox.isValid() and (selectionBBox != viewBBox):
                self.zoomStack.append(selectionBBox)
                self.updateViewer()
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
                
    def updateViewer(self):
        """
        Shows current zoom (if showing entire image, apply current aspect ratio mode).
        """
        
        if not self.hasImage():
            return
        if len(self.zoomStack) and self.sceneRect().contains(self.zoomStack[-1]):
            self.fitInView(self.zoomStack[-1], QtCore.Qt.KeepAspectRatio)  # Show zoomed rect (ignore aspect ratio).
        else:
            self.zoomStack = []  # Clear the zoom stack (in case we got here because of an invalid zoom).
            self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)  # Show entire image (use current aspect ratio mode).
