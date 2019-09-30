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

# import tifffile
print("Loading libraries...")
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
import data
import sys

print("done")
print("Opening laser communications...")
try:
    import Modules.arduinoComm as arduinoComm
except AttributeError:
    print("Couldn't open laser communication. Please ensure the control box USB cable is plugged to the computer.")
else:
    print("done")

    print("Opening Microscope communication...")
    try:
        import Modules.MM as MM
    except AttributeError:
        print("Couldn't open microscope communication. Please ensure the controller and the camera are switched on.")
    else:
        print("done")
        print("Loading GUI...")
        import GUI.guiMain as guiMain
        print("done")

        print(MM.getPropertyValue("Scope", "Method"))

        #Create the list of filters and available binning settings
        data.filters = MM.createAllowedPropertiesDictionnary('IL-Turret', 'Label')
        data.imageFormats = MM.createAllowedPropertiesDictionnary('HamamatsuHam_DCAM', 'Binning')
        data.methods = MM.createAllowedPropertiesDictionnary('Scope', 'Method')

        #Gets the limits values for TL intensity, diaphragms aperture and camera exposure time
        data.limitsIntensity = MM.createPropertyLimitsList('Transmitted Light', 'Level')
        data.limitsAperture = MM.createPropertyLimitsList('TL-ApertureDiaphragm', 'Position')
        data.limitsField = MM.createPropertyLimitsList('TL-FieldDiaphragm', 'Position')
        data.limitsExposure = MM.createPropertyLimitsList('HamamatsuHam_DCAM', 'Exposure')

        #Start Qt application
        # appctxt = ApplicationContext()
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        app.setStyle('Fusion')

        #Run the main UI code
        ui = guiMain.Ui_MainWindow()

        #Show the main window of the program
        ui.show()
        ui.setFixedSize(ui.size())
        ui.move(0, 0)

        #Start the application
        app.exec_()
        # exit_code = appctxt.app.exec_()

        #Stop the communications with Arduino and Micro-Manager
        MM.stop()
        arduinoComm.close()
        # sys.exit(exit_code)