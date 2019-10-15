# -*- coding: utf-8 -*-
"""
Implements different auto-focus algorithms.

Created on Wed Oct 9 16:46:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import data
from scipy import ndimage
import numpy as np


class SwitcherAF:

    def getFocusValue(self, frame, argument):
        """Dispatch method"""
        method_name = str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid month")
        # Call the method as we return it
        return method(frame)

    def absoluteGradient(self, frame):
        """
        Computes the 1D absolute gradient of an image.
        :param frame: 2d-array
        """
        print("Absolute Gradient Method")
        npFrame = np.array(frame, float)
        shape = npFrame.shape
        val = 0
        for x in range(shape[0]-1):
            for y in range(shape[1]):
                val += abs(npFrame[x+1][y]-npFrame[x][y])

        data.valStack.append(val)

    def squaredGradient(self, frame):
        """
        Computes the 1D squared gradient of an image.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        shape = npFrame.shape
        val = 0
        for x in range(shape[0] - 1):
            for y in range(shape[1]):
                val += (npFrame[x + 1][y] - npFrame[x][y])**2

        data.valStack.append(val)

    def sobel(self, frame):
        """
        Convolves and image with x and y sobel operators.
        :param frame: 2d-array
        """
        dx = ndimage.sobel(frame, 0)
        dy = ndimage.sobel(frame, 1)
        mag = np.hypot(dx, dy)
        val = np.sum(mag)
        data.valStack.append(1/val)

    def laplace(self, frame):
        """
        Convolves and image with laplacian operator.
        :param frame: 2d-array
        """
        mag = ndimage.laplace(frame)
        val = np.sum(mag)
        data.valStack.append(val)

    def energyLaplace(self, frame):
        kernel = np.matrix([[-1, -4, -1], [-4, 20, -4], [-1, -4, -20]])
        mag = ndimage.convolve(frame, kernel)
        val = np.sum(mag)
        data.valStack.append(val)

    def wavelet(self, frame):
        print("Not implemented yet")
        data.valStack.append(0)

    def waveletW2(self, frame):
        print("Not implemented yet")
        data.valStack.append(0)

    def waveletW3(self, frame):
        print("Not implemented yet")
        data.valStack.append(0)

    def variance(self, frame):
        """
        Computes the variance of an image.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        mu = np.mean(npFrame)
        shape = npFrame.shape
        val = 0
        for x in range(shape[0]):
            for y in range(shape[1]):
                val += (npFrame[x][y] - mu) ** 2

        data.valStack.append(val / (shape[0] * shape[1]))

    def normalizedVariance(self, frame):
        """
        Computes the normalized variance of an image.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        mu = np.mean(npFrame)
        shape = npFrame.shape
        val = 0
        for x in range(shape[0]):
            for y in range(shape[1]):
                val += (npFrame[x][y] - mu) ** 2

        data.valStack.append(val / (shape[0] * shape[1] * mu))

    def autoCorrelation(self, frame):
        """
        Computes the auto-correlation of the image.
        :param frame:
        """
        npFrame = np.array(frame, float)
        shape = npFrame.shape
        val1 = 0
        val2 = 0
        for x in range(shape[0]-2):
            for y in range(shape[1]):
                val1 += npFrame[x][y] * npFrame[x+1][y]
                val2 += npFrame[x][y] * npFrame[x+2][y]

        data.valStack.append(1/abs(val1 - val2))

    def stdBasedAutoCorrelation(self, frame):
        """
        Computes the auto-correlation of the image based on standard deviation.
        :param frame:
        """
        npFrame = np.array(frame, float)
        mu = np.mean(npFrame)
        shape = npFrame.shape
        val = 0
        for x in range(shape[0]-1):
            for y in range(shape[1]):
                val += npFrame[x][y] * npFrame[x+1][y]

        data.valStack.append(1/(val - shape[0] * shape[1] * mu ** 2))

    def range(self, frame):
        """
        Computes the dynamic range of the image.
        :param frame:
        """
        val = frame.max()-frame.min()

        data.valStack.append(1/val)
