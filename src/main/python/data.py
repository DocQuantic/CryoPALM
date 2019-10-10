# -*- coding: utf-8 -*-
"""
This files stores data that needs to be srored in memory during the execution of the program and that need to be
accessed by more than one method.

Created on Fri Mar 29 14:59:39 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

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

# Image metadata variables
acquisitionTime = ''
metadata = dict()

# Booleans
canSetROI = False
changedBinning = False
isAcquiring = False
countingState = False

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
             2: "sobel",
             3: "laplace",
             4: "energyLaplace",
             5: "wavelet",
             6: "waveletW2",
             7: "waveletW3",
             8: "variance",
             9: "normalizedVariance",
             10: "autoCorrelation",
             11: "stdBasedAutoCorrelation",
             12: "range"}

# Stage position list for PALM sequence acquisition (not in use)
# stagePos = []
