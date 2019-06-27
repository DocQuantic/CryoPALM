# -*- coding: utf-8 -*-
"""
This file contains the UI code for image viewer window
Form implementation generated from reading ui file 'guiMain.ui'

Created on Tue Jun 26 16:31:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""


import GUI.Widgets.histCommands as histCommands
import GUI.Widgets.imageViewerUI as imageViewerUI
import GUI.Widgets.histPlot as histPlot
import Modules.imageFunctions as imageFunctions
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import tifffile
import data


class Ui_Viewer(QtWidgets.QMainWindow):

    frame = []
    histX = []
    histY = []
    canZoom = False
    autoRange = False
    minHist = 0
    maxHist = (2**16)-1

    def __init__(self):
        """Setups all the elements positions and connections with functions
        """
        super(Ui_Viewer, self).__init__()

        self.centralWidget = QtWidgets.QWidget()

        self.setStyleSheet("background-color: rgb(64, 64, 64);\n"
                           "font: 12pt ''Berlin Sans FB'';\n"
                           "color: rgb(255, 255, 255);\n")

        self.mainLayout = QtWidgets.QGridLayout(self.centralWidget)

        #Image Display Widget
        self.imageDisplay = imageViewerUI.Ui_ImageViewer()

        #Histogram Commands Widget
        self.histogramCommands = histCommands.Ui_Histogram()

        #Histogram display Widget
        self.histogramDisplay = histPlot.Ui_HistPlot()
        self.histogramDisplay.setMinimumSize(QtCore.QSize(0, 120))

        self.mainLayout.addWidget(self.histogramCommands, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.imageDisplay, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.histogramDisplay, 1, 1, 1, 1)

        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Image Viewer")

        # self.histogramCommands.showFrame.connect(self.showFrame)
        self.histogramCommands.autoRangeSignal.connect(self.setAutoRange)
        self.histogramCommands.setMinSignal.connect(self.setMinHist)
        self.histogramCommands.setMaxSignal.connect(self.setMaxHist)

    def showFrame(self, frame):
        """Displays the image sent by the movie thread and its histogram
        """

        if type(frame) is not QtGui.QPixmap:
            self.frame = frame

            y, x = np.histogram(self.frame.ravel(), bins=np.linspace(self.minHist, self.maxHist, self.maxHist-self.minHist))

            self.histX = x
            self.histY = y

            if self.autoRange:
                self.minHist = frame.min()
                self.maxHist = frame.max()

            pix = array2Pixmap(frame, self.minHist, self.maxHist)
            self.imageDisplay.displayWindow.setImage(pix)
        else:
            self.imageDisplay.displayWindow.setImage(frame)

        if len(x) == len(y)+1:
            self.updateHist(self.histX, self.histY)

    def setAutoRange(self, signal):
        self.autoRange = signal

        if self.autoRange is True and data.isAcquiring is False and self.frame != []:
            self.showFrame(self.frame)

    def setMinHist(self, valueMin):
        if self.autoRange:
            self.autoRange = False

        self.minHist = valueMin
        if self.minHist > self.maxHist:
            self.maxHist = self.minHist

        if data.isAcquiring is False and self.frame != []:
            self.showFrame(self.frame)

    def setMaxHist(self, valueMax):
        if self.autoRange:
            self.autoRange = False

        self.maxHist = valueMax
        if self.maxHist < self.minHist:
            self.minHist = self.maxHist

        if data.isAcquiring is False and self.frame != []:
            self.showFrame(self.frame)

    def updateHist(self, x, y):
        if self.autoRange:
            self.histogramCommands.sliderMinimum.setValue(self.minHist)
            self.histogramCommands.spinBoxMin.setValue(self.minHist)
            self.histogramCommands.sliderMaximum.setValue(self.maxHist)
            self.histogramCommands.spinBoxMax.setValue(self.maxHist)
        self.histogramDisplay.p1.clear()
        self.histogramDisplay.p1.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 0, 255))


def array2Pixmap(frame, minHist, maxHist):
    """ Returns an 8 bits image pixmap from a raw 16 bits 2D array for display
    Before conversion, image values are scaled to the full dynamic range of the 8 bits image for better display
    :type frame: 2d array
    :rtype: QPixmap
    """
    idxHigh = np.where(frame > maxHist)
    idxLow = np.where(frame < minHist)
    frame[idxHigh] = maxHist-1
    frame[idxLow] = minHist
    img8 = abs((frame - minHist) / (maxHist-minHist))
    img8 = (img8*255).astype(np.uint8)
    img = QtGui.QImage(img8, img8.shape[0], img8.shape[1], QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap(img)
    return pix

def saveImage2D(pixels, path):
    """ Saves an image to a tiff file in a specific location with some metadata
    Metatdata scheme needs to be improved for good reading in ImageJ
    :type pixels: 2d array
    :type path: string
    """
    tifffile.imsave(path, pixels,
                    resolution=(1. / data.pixelSize * 10000, 1. / data.pixelSize * 10000, 'CENTIMETER'),
                    description=data.metadata)

def saveImageStack(pixels, path):
   """ Saves an image stack to a tiff file in a specific location with some metadata
   Metatdata scheme needs to be improved for good reading in ImageJ
   :type pixels: 3d array
   :type path: string
   """
   sizeX = pixels.shape[0]
   sizeY = pixels.shape[1]
   sizeT = pixels.shape[2]

   scaleX = data.pixelSize
   scaleY = scaleX
   pixelType = 'uint16'
   dimOrder = 'XY'

   # Getting metadata info
   omexml = ome.OMEXML()
   omexml.image(0).Name = path
   p = omexml.image(0).Pixels

   p.SizeX = sizeX
   p.SizeY = sizeY
   p.SizeT = sizeT
   p.PhysicalSizeX = np.float(scaleX)
   p.PhysicalSizeY = np.float(scaleY)
   p.PixelType = pixelType
   p.channel_count = 1
   p.plane_count = 1

   p.Channel(0).SamplesPerPixel = 2

   omexml.structured_annotations.add_original_metadata(ome.OM_SAMPLES_PER_PIXEL, str(1))

   # Converting to omexml
   xml = omexml.to_xml()

   # write file and save OME-XML as description
   tifffile.imsave(path, pixels, metadata={'axes': dimOrder}, description=xml)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_Viewer()
    ui.show()
    app.exec_()