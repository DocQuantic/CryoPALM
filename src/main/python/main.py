# -*- coding: utf-8 -*-
"""
This program is made to control a microscopy setup aimed at imaging biological samples via PALM technique.
It allows to control the microscope (DM6000 from Leica), the camera (Hamamatsu Orca Flash v4.0 LT) and the lasers
(Errol modified).
The microscope and the camera are controlled via the micromanager API and the lasers are controlled via communication
with an Arduino board.

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

from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys, os, time

print("Loading libraries...")
import data

# Start Qt application
appctxt = ApplicationContext()
appctxt.app.setStyle('Fusion')

# Read the conf file to fill data.py
confRes = appctxt.get_resource('configs/conf.txt')
txt = 'empty'
idx = 0
with open(confRes, 'r') as confFile:
    while txt is not '':
        txt = confFile.readline()
        if idx == 0:
            data.mm_directory = txt[0:-1]
            idx += 1
        elif idx == 1:
            data.savePath = txt[0:-1]
            idx += 1
        elif idx == 2:
            data.demo_cfg_file = appctxt.get_resource('configs/' + txt[0:-1])
            idx += 1
        elif idx > 2:
            data.system_cfg_file.append(appctxt.get_resource('configs/' + txt[0:-1]))

# Display and setup splash screen
splashResource = appctxt.get_resource('images/SplashScreen.png')
splashPix = QPixmap(splashResource)
splash = QSplashScreen(splashPix)
progressBar = QProgressBar(splash)
progressBar.setGeometry(150, 500, 500, 25)
progressBar.setTextVisible(True)
progressBar.setStyleSheet("QProgressBar::chunk::horizontal{background:QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #e36868, stop:0.499 #ab0f0f, stop:0.5 #aa0f0f, stop:1 #7a0b0b); border-radius:8px}\n"
                          "QProgressBar:horizontal{border-style:outset; border-width:2px; border-color:black; border-radius:10px; text-align:center; font: 12pt ''Berlin Sans FB''}\n")
splash.setMask(splashPix.mask())
splash.show()

print("done")
print("Opening laser communications...")
progressBar.setFormat("Optimizing lasers power...")
try:
    import Modules.arduinoComm as arduinoComm
except AttributeError:
    print("Couldn't open laser communication. Please ensure the control box USB cable is plugged to the computer.")
else:
    print("done")
    progressBar.setValue(33)

    print("Opening Microscope communication...")
    progressBar.setFormat("Aligning microscope lenses...")
    try:
        import Modules.MM as MM
    except AttributeError:
        print("Couldn't open microscope communication. Please ensure the controller and the camera are switched on.")
    else:
        print("done")
        progressBar.setValue(77)
        print("Loading GUI...")
        progressBar.setFormat("Drawing the buttons...")
        import GUI.guiMain as guiMain
        print("done")
        progressBar.setValue(99)

        MM.getCameraName()

        if data.isDemoMode is not True:
            if data.isCameraEM:
                data.pixelSize = 16/62.5
            else:
                data.pixelSize = 6.5/62.5

            # Create the list of filters and available binning settings
            data.filters = MM.createAllowedPropertiesDictionnary('IL-Turret', 'Label')
            data.methods = MM.createAllowedPropertiesDictionnary('Scope', 'Method')

            # Get the limits values for TL intensity, diaphragms aperture and camera exposure time
            data.limitsIntensity = MM.createPropertyLimitsList('Transmitted Light', 'Level')
            data.limitsAperture = MM.createPropertyLimitsList('TL-ApertureDiaphragm', 'Position')
            data.limitsField = MM.createPropertyLimitsList('TL-FieldDiaphragm', 'Position')

        data.imageFormats = MM.createAllowedPropertiesDictionnary(data.cameraDeviceName, 'Binning')
        data.limitsExposure = MM.createPropertyLimitsList(data.cameraDeviceName, 'Exposure')
        if data.limitsExposure[1] == 0:
            data.limitsExposure = [1, 1000]
        if data.isCameraEM:
            data.limitsEMGain = MM.createPropertyLimitsList(data.cameraDeviceName, 'MultiplierGain')

        # Enables output from AOTF on startup
        arduinoComm.writeChainArduino('3', '255')

        # Run the main UI code
        ui = guiMain.Ui_MainWindow()

        splash.close()

        # Show the main window of the program
        ui.show()
        ui.setFixedSize(ui.size())
        ui.move(0, 0)

        # Start the application
        exitCode = appctxt.app.exec_()

        # Stop the communications with Arduino and Micro-Manager
        MM.stop()
        arduinoComm.close()
        sys.exit(exitCode)
