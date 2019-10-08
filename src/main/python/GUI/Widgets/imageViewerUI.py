# -*- coding: utf-8 -*-
"""
This widget allows to display a raw image in a GUI and to interact with it.
If allowed, it is possible to zoom on a part of the image that is selected by left clicking and draging on this portion
of the image.
By right clicking, the zoom value is reset and we are back to the initial image.

This interaction can be done during live acquisition.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import GUI.Widgets.imageDisplay as imageDisplay
import data


class Ui_ImageViewer(QtWidgets.QWidget):

    saveImageSignal = QtCore.pyqtSignal()

    # Initialization of the class
    def __init__(self):
        super(Ui_ImageViewer, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        # Create the graphics scene that will host the image pixmap to display
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.displayWindow = imageDisplay.Ui_ImageDispay()
        self.displayWindow.setMinimumSize(QtCore.QSize(1200, 1200))

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        
        self.pushButtonZoom = QtWidgets.QPushButton("Zoom")
        self.pushButtonZoom.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButtonZoom.setCheckable(True)

        self.pushButtonSave = QtWidgets.QPushButton("Save As ...")
        self.pushButtonSave.setMinimumSize(QtCore.QSize(80, 40))
        self.pushButtonSave.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonZoom)
        self.horizontalLayout.addWidget(self.pushButtonSave)

        self.mainLayout.addWidget(self.displayWindow)
        self.mainLayout.addLayout(self.horizontalLayout)
           
        self.pushButtonZoom.clicked.connect(self.handleZoom)
        self.pushButtonSave.clicked.connect(self.saveImage)
        
        # Stack of QRectF zoom boxes in scene coordinates.
        self.zoomStack = []
        
        # Store a local handle to the scene's current image pixmap.
        self._pixmapHandle = None
     
    # Button interactions
    def handleZoom(self):
        """
        Sets the zoom on the image window active or inactive.
        """
        if self.pushButtonZoom.isChecked():
            data.canZoom = True
        else:
            data.canZoom = False

    @QtCore.pyqtSlot()
    def saveImage(self):
        """
        Sends a signal to save the image.
        """
        self.saveImageSignal.emit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_ImageViewer()
    ui.show()
    app.exec_()
