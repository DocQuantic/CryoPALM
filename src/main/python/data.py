# -*- coding: utf-8 -*-
"""
This files stores data that needs to be srored in memory during the execution of the program and that need to be
accessed by more than one method.

Created on Fri Mar 29 14:59:39 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets

# Path for Micro-Manager and saving directories
mm_directory = ''
system_cfg_file = []
demo_cfg_file = ''
savePath = ''
filePath = ''
cameraName = ''

# Dictionnaries with allowed values limit arrays of some properties
methods = dict()
filters = dict()
imageFormats = dict()
limitsIntensity = []
limitsAperture = []
limitsField = []
limitsExposure = []
limitsEMGain = []
limitsGain = []

# Pixel size obtained from LAS X calibration in microns
pixelSize = 211.25/2048

# Binning parameters
binning = 1

# Time to wait after an image was acquired
waitTime = 0.0

# Threshold for the counting algorithm
countThreshold = 80

# Shows one frame every frameStepShow during palm acq
frameStepShow = 10

# Image metadata variables
acquisitionTime = ''
metadata = dict()

# Camera chip size
xDim = 0
yDim = 0
zoomFactor = 0

# Booleans
canZoom = False
canSetROI = False
changedBinning = False
isAcquiring = False
countingState = False
previewState = False
showCenterQuad = False
isCameraEM = False
isDemoMode = False

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

# EllipseItem pen creation for particule detection
penEllipse = QtGui.QPen(QtCore.Qt.green, 1)

# Stage position list for PALM sequence acquisition (not in use)
# stagePos = []
