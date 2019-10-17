# -*- coding: utf-8 -*-
"""
Implements different auto-focus algorithms.

Created on Wed Oct 9 16:46:00 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import data
from scipy import ndimage
import numpy as np
import math
import pywt
import time


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
        frame = ndimage.gaussian_filter(frame, sigma=1)
        npFrame = np.array(frame, float)
        val = np.sum(abs(np.diff(npFrame, 0)))

        data.valStack.append(1/val)

    def squaredGradient(self, frame):
        """
        Computes the 1D squared gradient of an image.
        :param frame: 2d-array
        """
        frame = ndimage.gaussian_filter(frame, sigma=1)
        npFrame = np.array(frame, float)
        val = np.sum(np.square(np.diff(npFrame, 0)))

        data.valStack.append(1/val)

    def brennerGradient(self, frame):
        """
        Computes the 1D Brenner gradient of an image.
        :param frame: 2d-array
        """
        frame = ndimage.gaussian_filter(frame, sigma=1)
        npFrame1 = np.array(frame, float)[1:-3, ::]
        npFrame2 = np.array(frame, float)[3:-1, ::]
        val = np.sum(np.square(npFrame1-npFrame2))

        data.valStack.append(1 / val)

    def sobel(self, frame):
        """
        Convolves and image with x and y sobel operators.
        :param frame: 2d-array
        """
        dx = ndimage.sobel(frame, 0)
        dy = ndimage.sobel(frame, 1)
        mag = np.hypot(dx, dy)
        val = np.sum(mag)
        data.valStack.append(val)

    def laplace(self, frame):
        """
        Convolves and image with laplacian operator.
        :param frame: 2d-array
        """
        frame = ndimage.gaussian_filter(frame, sigma=1)
        mag = ndimage.laplace(frame)
        val = np.sum(mag)
        data.valStack.append(val)

    def energyLaplace(self, frame):
        """
        Convolves the image with this mask : [[-1, -4, -1], [-4, 20, -4], [-1, -4, -20]] and sums the square of each
        obtained value.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        kernel = np.matrix([[-1, -4, -1], [-4, 20, -4], [-1, -4, -20]])
        mag = ndimage.convolve(npFrame, kernel)
        val = np.sum(np.square(mag))
        data.valStack.append(1/val)

    def wavelet(self, frame):
        """
        Applies a level-1 discrete wavelet transform with db6 filter and sums absolute value of each subarray.
        :param frame: 2d-array
        """
        wp = pywt.WaveletPacket2D(data=frame, wavelet='db6', mode='symmetric')
        LH = abs(wp['h'].data)
        HL = abs(wp['v'].data)
        HH = abs(wp['d'].data)

        mag = np.add(LH, np.add(HH, HL))
        val = np.sum(mag)

        data.valStack.append(val)

    def waveletW2(self, frame):
        """
        Applies a level-1 discrete wavelet transform with db6 filter and sums absolute value of each subarray after
        subtracting mean value of each subarray.
        :param frame: 2d-array
        """
        shape = frame.shape
        surf = shape[0]*shape[1]

        wp = pywt.WaveletPacket2D(data=frame, wavelet='db6', mode='symmetric')
        wLH = abs(wp['h'].data)
        wHL = abs(wp['v'].data)
        wHH = abs(wp['d'].data)

        muLH = np.mean(wLH)
        muHL = np.mean(wHL)
        muHH = np.mean(wHH)

        LH = np.square(wLH-muLH)
        HL = np.square(wHL-muHL)
        HH = np.square(wHH-muHH)

        mag = np.add(LH, np.add(HH, HL))
        val = np.sum(mag)/surf

        data.valStack.append(1/val)

    def waveletW3(self, frame):
        """
        Same as W2 except that we don't use absolute values.
        :param frame: 2d-array
        """
        shape = frame.shape
        surf = shape[0]*shape[1]

        wp = pywt.WaveletPacket2D(data=frame, wavelet='db6', mode='symmetric')
        wLH = wp['h'].data
        wHL = wp['v'].data
        wHH = wp['d'].data

        muLH = np.mean(wLH)
        muHL = np.mean(wHL)
        muHH = np.mean(wHH)

        LH = np.square(wLH-muLH)
        HL = np.square(wHL-muHL)
        HH = np.square(wHH-muHH)

        mag = np.add(LH, np.add(HH, HL))
        val = np.sum(mag)/surf

        data.valStack.append(1/val)

    def variance(self, frame):
        """
        Computes the variance of an image.
        :param frame: 2d-array
        """
        frame = ndimage.gaussian_filter(frame, sigma=1)
        npFrame = np.array(frame, float)
        shape = npFrame.shape
        mu = np.mean(npFrame)
        val = np.sum(np.square(npFrame - mu))

        data.valStack.append(1/(val / (shape[0] * shape[1])))

    def normalizedVariance(self, frame):
        """
        Computes the normalized variance of an image.
        :param frame: 2d-array
        """
        frame = ndimage.gaussian_filter(frame, sigma=1)
        npFrame = np.array(frame, float)
        mu = np.mean(npFrame)
        shape = npFrame.shape
        val = np.sum(np.square(npFrame - mu))

        data.valStack.append(1/(val / (shape[0] * shape[1] * mu)))

    def autoCorrelation(self, frame):
        """
        Computes the auto-correlation of the image.
        :param frame: 2d-array
        """
        npFrame1 = np.array(frame, float)[1:-3, ::]
        npFrame21 = np.array(frame, float)[2:-2, ::]
        npFrame22 = np.array(frame, float)[3:-1, ::]

        val = np.sum(np.multiply(npFrame1, npFrame21) - np.multiply(npFrame1, npFrame22))

        data.valStack.append(1 / val)

    def stdBasedAutoCorrelation(self, frame):
        """
        Computes the auto-correlation of the image based on standard deviation.
        :param frame: 2d-array
        """
        npFrame1 = np.array(frame, float)[1:-2, ::]
        npFrame2 = np.array(frame, float)[2:-1, ::]
        mu = np.mean(frame)
        shape = frame.shape

        val = np.sum(np.multiply(npFrame1, npFrame2)) - shape[0] * shape[1] * math.pow(mu, 2)

        data.valStack.append(1 / val)

    def range(self, frame):
        """
        Computes the dynamic range of the image.
        :param frame: 2d-array
        """
        val = frame.max()-frame.min()

        data.valStack.append(1/val)

    def entropy(self, frame):
        """
        Computes the entropy value of the image.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        shape = npFrame.shape
        surf = shape[0]*shape[1]
        histY, histX = np.histogram(npFrame.ravel(), frame.max()-frame.min())
        p = histY/surf

        val = np.sum(np.multiply(p, np.log2(p)))

        data.valStack.append(1/val)

    def imageContent(self, frame):
        """
        Sums all the pixels of the image.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        val = np.sum(npFrame)

        data.valStack.append(val)

    def imagePower(self, frame):
        """
        Sums the square value of each pixel.
        :param frame: 2d-array
        """
        npFrame = np.array(frame, float)
        val = np.sum(np.square(npFrame))

        data.valStack.append(1/val)