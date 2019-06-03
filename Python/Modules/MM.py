# -*- coding: utf-8 -*-
"""
This code handles the communication between the main program and the Micro-Manager core for management of the microscope

Created on Fri Mar 29 16:49:30 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import data
import sys
import os

# Append MM directory to path and import the wrapper
sys.path.append('C:/Program Files/Micro-Manager-2.0beta')
prev_dir = os.getcwd()
os.chdir('C:/Program Files/Micro-Manager-2.0beta')

import numpy.core.multiarray
import MMCorePy



mmc = MMCorePy.CMMCore()

# Load system configuration (loads all devices)
try:
    mmc.loadSystemConfiguration(data.system_cfg_file)
except:
    raise AttributeError()

os.chdir(prev_dir)

def createAllowedPropertiesDictionnary(Device, Property):
    """ Returns a dictionnary containing the allowed values for a property associated with an integer for list selection
    :type Device: string
    :type Property: string
    :rtype: {string, int}
    """
    i=0
    dictionnary = dict()
    allowedProperties = mmc.getAllowedPropertyValues(Device, Property)
    while i<len(allowedProperties):
        dictionnary[allowedProperties[i]] = i
        i+=1
    return dictionnary

def createPropertyLimitsList(Device, Property):
    """ Returns a list containing the lower and upper values allowed for a property
    :type Device: string
    :type Property: string
    :rtype: [string, string]
    """
    limits = [mmc.getPropertyLowerLimit(Device, Property), mmc.getPropertyUpperLimit(Device, Property)]
    return limits

def setPropertyValue(Device, Property, Value):
    """ Sets a property to a specified value
    :type Device: string
    :type Property: string
    :type Value: string
    """
    mmc.setProperty(Device, Property, Value)
    
def getPropertyValue(Device, Property):
    """ Gets the value of a property
    :type Device: string
    :type Property: string
    :rtype: string
    """
    value = mmc.getProperty(Device, Property)
    return value

def snapImage():
    """ Takes a snapshot with the camera
    :rtype: 2d array
    """
    mmc.snapImage()
    img = mmc.getImage()
    return img

def startAcquisition():
    """ Start continuous acquisition with the camera
    """
    mmc.startContinuousSequenceAcquisition(1)
    
def stopAcquisition():
    """ Stops the acquisition
    """
    mmc.stopSequenceAcquisition()
    
def getMovieFrame():
    """ Returns the last frame acquirred by the camera during continuous acquisition
    :rtype: 2d array
    """
    if mmc.getRemainingImageCount() > 0:
        frame = mmc.getLastImage()
        return frame
    
def setROI(x0, y0, sizeX, sizeY):
    """ Sets the region of interest of the camera
    :type x0: int
    :type y0: int
    :type sizeX: int
    :type sizeY: int
    """
    mmc.setROI(x0, y0, sizeX, sizeY)
    
def clearROI():
    """ Clear the region of interest of the camera
    """
    mmc.clearROI()

def setZPos(pos):
    """ Sets the Z position of the objective
    :type pos:  int
    """
    mmc.setPosition(pos)
    
def getZPos():
    """ Returns the Z position of the objective
    :rtype:  int
    """
    pos = mmc.getPosition()
    return pos

def setXYPos(posX, posY):
    """ Sets the X and Y position of the translation stage
    :type posX:  int
    :type posY:  int
    """
    mmc.setXYPosition(posX, posY)
    
def getXYPos():
    """ Returns the X and Y position of the translation stage
    :rtype:  [int, int]
    """
    pos = mmc.getXYPosition()
    return pos

def cameraAcquisitionTime():
    """Returns the total acquisition time of the camera (exposure time + readout time) in milliseconds
    :rtype: float
    """
    exposure = float(mmc.getProperty('HamamatsuHam_DCAM', 'Exposure'))
    readout = float(mmc.getProperty('HamamatsuHam_DCAM', 'ReadoutTime'))
    acquisitionTime = exposure+readout
    return acquisitionTime/1000

def stop():
    """Stops the communication with the Micro-Manager core
    """
    mmc.reset()
    print("Program stopped")
