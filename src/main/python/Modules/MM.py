# -*- coding: utf-8 -*-
"""
This code handles the communication between the main program and the Micro-Manager core for management of the microscope.

Created on Fri Mar 29 16:49:30 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import data
import sys
import os

# Append MM directory to path and import the wrapper
sys.path.append(data.mm_directory)
prev_dir = os.getcwd()
os.chdir(data.mm_directory)

import MMCorePy


mmc = MMCorePy.CMMCore()

# Load system configuration (loads all devices)
noCfgFound = True
idx = 0
idxMax = len(data.system_cfg_file)
while noCfgFound:
    try:
        mmc.loadSystemConfiguration(data.system_cfg_file[idx])
        noCfgFound = False
    except:
        if idx < idxMax:
            idx += 1
        else:
            try:
                mmc.loadSystemConfiguration(data.demo_cfg_file)
                data.isDemoMode = True
                print(
                    "Couldn't open microscope communication. Please ensure the controller and the camera are switched on. Run demo mode instead.")
                noCfgFound = False
            except:
                raise AttributeError()

os.chdir(prev_dir)

mmc.setAutoShutter(False)

def getCameraName():
    """
    Finds the current camera name and setup chip size and EM ui if needed.
    """
    data.cameraDeviceName = mmc.getCameraDevice()

    frameShape = snapImage().shape
    data.xDim = frameShape[0]
    data.yDim = frameShape[1]
    data.zoomFactor = data.xDim/256

    data.isCameraEM = hasProperty(data.cameraDeviceName, 'MultiplierGain')

    if hasProperty(data.cameraDeviceName, 'Gain'):
        data.limitsGain = createPropertyLimitsList(data.cameraDeviceName, 'Gain')
        if data.limitsGain[1] == 0:
            data.limitsGain = [1, 3]

    #Checks the camera driver family (DCAM or PVCAM)
    if data.cameraDeviceName == "HamamatsuHam_DCAM":
        cameraName = getPropertyValue(data.cameraDeviceName, 'CameraName')
        if cameraName == 'C14440-20UP':
            #Set slow mode (low noise) if hamamatsu fusion camera is loaded
            setPropertyValue(data.cameraDeviceName, "ScanMode", "1")
    elif data.cameraDeviceName == "Camera-1":
        cameraName = getPropertyValue(data.cameraDeviceName, 'Name')

def hasProperty(device, property):
    """
    Checks if a given device has a specific property
    :param Device: string
    :param Property: string
    :return: bool
    """
    propList = mmc.getDevicePropertyNames(device)
    for prop in propList:
        if prop == property:
            return True
    return False

def createAllowedPropertiesDictionnary(Device, Property):
    """
    Returns a dictionnary containing the allowed values for a property associated with an integer for list selection.
    :param Device: string
    :param Property: string
    :return: {string, int}
    """
    i = 0
    dictionnary = dict()
    allowedProperties = mmc.getAllowedPropertyValues(Device, Property)
    while i < len(allowedProperties):
        dictionnary[allowedProperties[i]] = i
        i += 1
    return dictionnary

def createPropertyLimitsList(Device, Property):
    """
    Returns a list containing the lower and upper values allowed for a property.
    :param Device: string
    :param Property: string
    :return: [string, string]
    """
    limits = [mmc.getPropertyLowerLimit(Device, Property), mmc.getPropertyUpperLimit(Device, Property)]
    return limits

def setPropertyValue(Device, Property, Value):
    """
    Sets a property to a specified value.
    :param Device: string
    :param Property: string
    :param Value: string
    """
    mmc.setProperty(Device, Property, Value)

def getPropertyValue(Device, Property):
    """
    Gets the value of a property.
    :param Device: string
    :param Property: string
    :return: string
    """
    value = mmc.getProperty(Device, Property)
    return value

def snapImage():
    """
    Takes a snapshot with the camera.
    :return: 2d array
    """
    mmc.snapImage()
    img = mmc.getImage()
    return img

def startAcquisition():
    """
    Start continuous acquisition with the camera.
    """
    mmc.startContinuousSequenceAcquisition(1)

def stopAcquisition():
    """
    Stops the acquisition.
    """
    mmc.stopSequenceAcquisition()

def getMovieFrame():
    """
    Returns the last frame acquirred by the camera during continuous acquisition.
    :return: 2d array
    """
    if mmc.getRemainingImageCount() > 0:
        frame = mmc.getLastImage()
        return frame

def setROI(x0, y0, sizeX, sizeY):
    """
    Sets the region of interest of the camera.
    :param x0: int
    :param y0: int
    :param sizeX: int
    :param sizeY: int
    """
    mmc.setROI(x0, y0, sizeX, sizeY)

def clearROI():
    """
    Clear the region of interest of the camera.
    """
    mmc.clearROI()

def setZPos(pos):
    """
    Sets the Z position of the objective.
    :param pos:  int
    """
    mmc.setPosition(pos)

def getZPos():
    """
    Returns the Z position of the objective.
    :return:  int
    """
    pos = mmc.getPosition()
    return pos

def setRelXYPos(dX, dY):
    """
    Sets the X and Y position of the translation stage relatively to the current position.
    :param dX:  int
    :param dY:  int
    """
    mmc.setRelativeXYPosition(dX, dY)

def getXYPos():
    """ Returns the X and Y position of the translation stage.
    :return:  [int, int]
    """
    pos = [mmc.getXPosition(), mmc.getYPosition()]
    return pos

def cameraAcquisitionTime():
    """
    Returns the total acquisition time of the camera (exposure time + readout time) in milliseconds.
    :return: float
    """
    exposure = float(mmc.getProperty(data.cameraDeviceName, 'Exposure'))
    readout = 0#float(mmc.getProperty(data.cameraDeviceName, 'ReadoutTime'))
    acquisitionTime = exposure/1000+readout
    return acquisitionTime

def stop():
    """
    Stops the communication with the Micro-Manager core.
    """
    mmc.reset()
    print("Program stopped")
