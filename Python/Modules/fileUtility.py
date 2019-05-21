# -*- coding: utf-8 -*-
"""
This file implements several file utilities such as creating today's directory or accessing text files for data extraction
Created on Mon May 20 10:00:52 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from xml.dom import minidom
from datetime import date
import data
import os

    
def createTodayDir():
    """ Creates a directory with today's date as name if it doesn't already exist.
    It also initializes the counters for saved images and stacks if some have already been saved with the same naming convention.
    """
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
        
def readFileSerialEM(path):
    xPos = 0
    yPos = 0
    pos = []
    file = minidom.parse(path)
    points = file.getElementsByTagName("MarkerPoint")
    for point in points:
        xPos = float(point.attributes['XPosition'].value)
        yPos = float(point.attributes['YPosition'].value)
        pos.append([xPos, yPos])
    return pos
                
            
                