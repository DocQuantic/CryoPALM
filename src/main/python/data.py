# -*- coding: utf-8 -*-
"""
This files stores data that needs to be srored in memory during the execution of the program and that need to be
accessed by more than one method.

Created on Fri Mar 29 14:59:39 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets

# Path for Micro-Manager and saving directories
mm_directory = 'C:/Program Files/Micro-Manager-2.0beta'
system_cfg_file = 'C:/Program Files/Micro-Manager-2.0beta/PALM-config.cfg'
demo_cfg_file = 'C:/Program Files/Micro-Manager-2.0beta/MMConfig_demo.cfg'
savePath = 'D:/Users1/'
filePath = ''

# Dictionnaries with allowed values limit arrays of some properties
methods = dict()
filters = dict()
imageFormats = dict()
limitsIntensity = []
limitsAperture = []
limitsField = []
limitsExposure = []

# Pixel size obtained from LAS X calibration
pixelSize = 211.25/2048

# Binning parameters
binning = 1

# Time to wait after an image was acquired
waitTime = 0.0

# Threshold for the counting algorithm
countThreshold = 110

# Shows one frame every frameStepShow during palm acq
frameStepShow = 10

# Image metadata variables
acquisitionTime = ''
metadata = dict()

# Booleans
canZoom = False
canSetROI = False
changedBinning = False
isAcquiring = False
countingState = False
showCenterQuad = False

# Variables for Autofocus
AFRange = 10.0
AFSteps = 10
AFStepSize = AFRange/AFSteps
AFZPos = []
AFStack = []
valStack = []
besfocus = 0.0
currentAFMethod = 'sobel'
methodsAF = {0: "absoluteGradient",
             1: "squaredGradient",
             2: "brennerGradient",
             3: "sobel",
             4: "laplace",
             5: "energyLaplace",
             6: "wavelet",
             7: "waveletW2",
             8: "waveletW3",
             9: "variance",
             10: "normalizedVariance",
             11: "autoCorrelation",
             12: "stdBasedAutoCorrelation",
             13: "range",
             14: "entropy",
             15: "imageContent",
             16: "imagePower"}

# RectItem creation for center quad display
rectItem256 = QtWidgets.QGraphicsRectItem(QtCore.QRectF(896, 896, 256, 256))
rectItem128 = QtWidgets.QGraphicsRectItem(QtCore.QRectF(448, 448, 128, 128))
rectItem64 = QtWidgets.QGraphicsRectItem(QtCore.QRectF(224, 224, 64, 64))
pen = QtGui.QPen(QtCore.Qt.blue, 3, QtCore.Qt.DashLine)
rectItem256.setPen(pen)
rectItem128.setPen(pen)
rectItem64.setPen(pen)

# Stage position list for PALM sequence acquisition (not in use)
# stagePos = []
