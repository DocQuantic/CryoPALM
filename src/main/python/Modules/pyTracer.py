# -*- coding: utf-8 -*-
"""
This file implements functions used to count particules on an image.

Created on Thu Jul  11 16:22:54 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import numpy as np
import cv2


def imageAutoRescale(image):
    """
    Rescales the image to 8 bits.
    :param image: 2d array
    :return: 2d array
    """
    img8 = abs((image - image.min()) / (image.max() - image.min()))
    img8 = (img8 * 255).astype(np.uint8)

    return img8


def easyWatershed(image, start, stop):
    """
    Applies a watershed filter on the input image.
    :param image: 2d array
    :param start: int
    :param stop: int
    :return: 2d array
    """
    blurredImage = np.zeros(shape=(256, 256, stop-start))

    idx = start
    while idx < stop:
        blurredImage[:, :, idx-start] = cv2.GaussianBlur(image, (2*idx+1, 2*idx+1), cv2.BORDER_DEFAULT)
        idx += 1

    deltaImage = np.diff(blurredImage, n=1, axis=2)*(-1)
    sumImage = np.sum(deltaImage, 2)

    return sumImage


def countParticules(image, threshold):
    """
    Counts the particules with intensity higher than threshold value on the input image.
    :param image: 2d array
    :param threshold: int
    :return: int
    """
    start = 1
    stop = 6

    filteredImage = easyWatershed(image, start, stop)

    ret, binaryImage = cv2.threshold(filteredImage, threshold, 65535, cv2.THRESH_BINARY)
    binaryImage8 = imageAutoRescale(binaryImage)
    contours, hierarchy = cv2.findContours(binaryImage8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = len(contours)

    return count
