# -*- coding: utf-8 -*-
"""
This code implements several functions in relation with image manipulation or saving
Created on Mon Apr  1 15:48:58 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import bioformats.omexml as ome
from datetime import date
from PyQt5 import QtGui
import numpy as np
import tifffile
import data
import os

def array2Pixmap(frame):
    """ Returns an 8 bits image pixmap from a raw 16 bits 2D array for display
    Before conversion, image values are scaled to the full dynamic range of the 8 bits image for better display
    :type frame: 2d array
    :rtype: QPixmap
    """
    img8 = ((frame - frame.min()) / (frame.ptp() / 255.0)).astype(np.uint8)
    img8 = np.around(img8).astype(np.uint8)
    img = QtGui.QImage(img8, img8.shape[0], img8.shape[1], QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap(img)
    return pix

def saveImage2D(pixels, path):
    """ Saves an image to a tiff file in a specific location with some metadata
    Metatdata scheme needs to be improved for good reading in ImageJ
    :type pixels: 2d array
    :type path: string
    """
    sizeX = pixels.shape[0]
    sizeY = pixels.shape[1]
    
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
    
def createTodayDir():
    imageNum = []
    stackNum = []
    today=str(date.today())
    data.savePath = data.savePath + '\\' + today
    if os.path.exists(data.savePath):
        files = [f for f in os.listdir(data.savePath) if os.path.isfile(os.path.join(data.savePath, f))]
        for file in files:
            indexImg = file.find('img')
            if indexImg != -1:
                idxDot = file.find('.')
                imageNum.append(int(file[3:idxDot]))
            else:
                indexStack = file.find('stack')
                if indexStack != -1:
                    idxDot = file.find('.')
                    stackNum.append(int(file[5:idxDot]))
        
        if len(imageNum) != 0:
            data.savedImagesCounter = max(imageNum)+1
        else:
            data.savedImagesCounter = 0
        if len(stackNum) != 0:
            data.savedStacksCounter = max(stackNum)+1
        else:
            data.savedStacksCounter = 0
        return
    else:
        os.makedirs(data.savePath)
        return
        