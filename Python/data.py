# -*- coding: utf-8 -*-
"""
This files stores data that needs to be srored in memory during the execution of the program and that need to be accessed by more than one method

Created on Fri Mar 29 14:59:39 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

#Path for Micro-Manager directories and saving directory
mm_directory = 'C:\\Program Files\\Micro-Manager-2.0beta'
system_cfg_file = 'C:\\Program Files\\Micro-Manager-2.0beta\\CLEM_config.cfg'
demo_cfg_file = 'C:\\Program Files\\Micro-Manager-2.0beta\\MMConfig_demo.cfg'
savePath = 'D:\\Users\\William BIC\\Python\\CLEM'

#Counters for number of stack and images saved since the program was launched
savedImagesCounter = 0
savedStacksCounter = 0

#Dictionnaries with allowed property values for the filter installed and the image formats
methods = dict()
filters = dict()
imageFormats = dict()

#Pixel size obtained from LAS X calibration
pixelSize = 211.25/2048

#Binning parameters
binning = 1
changedBinning = False

#Store the current image and the current stack before saving to disk
frame = []
palmStack = 0

#Boolean storing the state of the Zoom and Set ROI functions
canZoom = False
canSetROI = False

#Variables for Autofocus
AFRange = 10.0
AFSteps = 10
AFStepSize = AFRange/AFSteps
AFZPos = []
AFStack = []
varStack = []
besfocus = 0.0