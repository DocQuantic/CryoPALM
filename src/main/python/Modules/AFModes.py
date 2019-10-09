# -*- coding: utf-8 -*-
"""
This file implements different autofocus algorithms.

Created on Wed Oct 9 15:36:06 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import data
import numpy as np

def gradient(stack):
    for frame in stack:
        print(frame)