# -*- coding: utf-8 -*-
"""
This file implements allows to analyze the PALM stack to reconstruct the super-resolved image on line.
Created on Fri June 14 10:07:10 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import cv2

img = cv2.imread('D:/Users/William_BIC/Images/PALM/2019-06-12/img0.tif', 0)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()