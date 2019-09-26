# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import tifffile as tif
import numpy as np
from numba import jit
from skimage import color
from skimage.measure import label
from skimage.morphology import extrema
import math
import time
import cv2


def tileImage(image, tileSize, numTiles, overlap):
    tileStack = np.zeros(shape=(tileSize, tileSize, numTiles**2))

    idxX = 0
    idxTile = 0
    while idxX < numTiles:
        idxY = 0
        while idxY < numTiles:
            tileStack[:, :, idxTile] = image[idxX * (tileSize - overlap):idxX * (tileSize - overlap) + tileSize,
                                       idxY * (tileSize - overlap):idxY * (tileSize - overlap) + tileSize]
            idxY += 1
            idxTile += 1
        idxX += 1

    return tileStack


def reconstructImage(tileStack, tileSize, numTiles, overlap):
    filteredImage = np.zeros(shape=(tileSize**2, tileSize**2))

    idxX = 0
    idxTile = 0
    while idxX < numTiles:
        idxY = 0
        while idxY < numTiles:
            filteredImage[idxX * (tileSize - overlap):idxX * (tileSize - overlap) + tileSize,
                                       idxY * (tileSize - overlap):idxY * (tileSize - overlap) + tileSize] = tileStack[:, :, idxTile]
            idxY += 1
            idxTile += 1
        idxX += 1

def imageAutoRescale(image):
    img8 = abs((image - image.min()) / (image.max() - image.min()))
    img8 = (img8 * 255).astype(np.uint8)

    return img8

def findLocalMaxima(image, h):
    """"Long to execute
    """
    h_maxima = extrema.h_maxima(image, h)
    label_h_maxima = label(h_maxima)
    overlay_h = color.label2rgb(label_h_maxima, image, alpha=0.7, bg_label=0,
                                bg_color=None, colors=[(1, 0, 0)])

    return overlay_h

def easyWatershed(image, start, stop):
    blurredImage = np.zeros(shape=(256, 256, stop-start))

    idx = start
    while idx < stop:
        blurredImage[:, :, idx-start] = cv2.GaussianBlur(image, (2*idx+1, 2*idx+1), cv2.BORDER_DEFAULT)
        idx += 1

    deltaImage = np.diff(blurredImage, n=1, axis=2)*(-1)
    sumImage = np.sum(deltaImage, 2)

    return sumImage

@jit(nopython = True)
def easyWatershedGPU(imageStack, rangeWatershed, blurredImage, rangePlane):
    start = rangeWatershed[0]

    for planeIdx in rangePlane:
        image = imageStack[:, :, planeIdx]
        for idx in rangeWatershed:
            # stop = 8
            blurredImage[:, :, idx-start] = image
        #
        # deltaImage = np.diff(blurredImage, n=1, axis=2)*(-1)
        # imageStack[:, :, planeIdx] = np.sum(deltaImage, 2)

    return imageStack

def computeGaussianKernels():
    maxSigma = 6
    kernelSize = 1*maxSigma-1
    idxX = -((kernelSize-1)/2)
    idx = 0
    xVector = np.zeros(shape=(kernelSize))
    G = np.zeros(shape=(kernelSize, kernelSize))
    K = []

    while idxX <kernelSize/2:
        xVector[idx] = idxX
        idx += 1
        idxX += 1
    yVector = xVector

    idx = 1
    while idx < maxSigma+1:
        sigma = idx

        idxX = 0
        for x in xVector:
            idxY = 0
            for y in yVector:
                G[idxX, idxY] = math.exp(-(x**2+y**2)/(2*sigma**2))
                idxY += 1
            idxX += 1
        normFactor = np.sum(G)
        G = G/normFactor

        K[:, :, idx-1] = G
        idx += 1

    return K

def countParticules(image, threshold):
    start = 1
    stop = 6

    filteredImage = easyWatershed(image, start, stop)

    ret, binaryImage = cv2.threshold(filteredImage, threshold, 65535, cv2.THRESH_BINARY)
    binaryImage8 = imageAutoRescale(binaryImage)
    contours, hierarchy = cv2.findContours(binaryImage8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = len(contours)

    return count


if __name__ == '__main__':
    imagePath = 'D:/Users/William_BIC/Python/FastPALM/Images/singleImage1.tif'

    image = tif.imread(imagePath)
    count = countParticules(image, 110)

    print(count)

    #
    # tileSize = 16
    # numTiles = 21
    # overlap = int(tileSize - (256 - tileSize) / (numTiles - 1))

    # tileStack = tileImage(image, tileSize, numTiles, overlap)
    # rangeWatershed = np.linspace(start, stop, num=6, dtype=np.uint16)
    # rangePlane = np.linspace(0, tileStack.shape[2]-1, num=tileStack.shape[2], dtype=np.uint16)
    # blurredImage = np.zeros(shape=(tileStack.shape[0], tileStack.shape[1], int(stop-start)+1))

    # G = computeGaussianKernels()
