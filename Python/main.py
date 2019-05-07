# -*- coding: utf-8 -*-
"""
This program is made to control a microscopy setup aimed at imaging biological samples via PALM technique.
It allows to control the microscope (DM6000 from Leica), the camera (Hamamatsu Orca Flash v4.0 LT) and the lasers (Errol modified)
The microscope and the camera are controlled via the micromanager API and the lasers are controlled via communication with an Arduino board.

The program allows to :
    -Change microscope settings
    -Change camera settings
    -Acquire images live
    -Acquire images snapshot
    -Save snapshots
    -Find the best focus on the imaged area
    -Display the acquired images
    -Display the corresponding histogram
    -Control the different laser powers independently
    -Perform PALM acquisition

Created on Fri Mar 29 09:54:55 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
import arduinoComm
import guiMain
import data
import sys
import MM

#Start Qt application
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

#Run and initialize the main UI code
MainWindow = QMainWindow()
ui = guiMain.Ui_MainWindow()
ui.setupUi(MainWindow)

#Create the list of filters and available binning settings
data.filters = MM.createAllowedPropertiesDictionnary('IL-Turret', 'Label')
data.imageFormats = MM.createAllowedPropertiesDictionnary('HamamatsuHam_DCAM', 'Binning')
data.methods = MM.createAllowedPropertiesDictionnary('Scope', 'Method')

#Gets the limits values for TL intensity, diaphragms aperture and camera exposure time
limitsIntensity = MM.createPropertyLimitsList('Transmitted Light', 'Level')
limitsAperture = MM.createPropertyLimitsList('TL-ApertureDiaphragm', 'Position')
limitsField = MM.createPropertyLimitsList('TL-FieldDiaphragm', 'Position')
limitsExposure = MM.createPropertyLimitsList('HamamatsuHam_DCAM', 'Exposure')

#Show the main window of the program
MainWindow.showMaximized()

#Initialize the UI
ui.initShutterIL()
ui.initFilters()
ui.initMethod()
ui.initShutterTL()
ui.initBFLightState()
ui.initFormats()
ui.initIntensity(limitsIntensity, MM.getPropertyValue('Transmitted Light', 'Level'))
ui.initAperture(limitsAperture, MM.getPropertyValue('TL-ApertureDiaphragm', 'Position'))
ui.initFieldBF(limitsField, MM.getPropertyValue('TL-FieldDiaphragm', 'Position'))
ui.initExposure(limitsExposure, MM.getPropertyValue('HamamatsuHam_DCAM', 'Exposure'))

#Start the application
app.exec_()

#Stop the communications with Arduino and Micro-Manager
MM.stop()
arduinoComm.close()