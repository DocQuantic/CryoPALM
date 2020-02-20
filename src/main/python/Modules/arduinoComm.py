# -*- coding: utf-8 -*-
"""
This method allows the main program to communicate with the Arduino board to set the values of the different outputs.

Created on Mon Apr 15 16:55:32 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from serial import Serial
from PyQt5 import QtCore, QtGui
import data
import time

try:
    arduino = Serial('COM6', 115200, timeout=0) # Establish the connection on a specific port at a specific baud rate
except Serial.serialutil.SerialException:
    raise AttributeError

isRunning = True

def writeChainArduino(channel, power):
    """
    Writes a character chain with a predefined format to set the right value on the right digital output channel.
    :param channel: string
    :return power: string
    """
    chain = '<' + channel + ',' + power + '>'
    for char in chain:
        byteChar = char.encode('utf-8')
        arduino.write(byteChar)

def listens():
    """
    Reads the serial channel and returns the read line.
    :return: string
    """
    line = arduino.readline().decode("utf-8")
    return line[0:-2]

def close():
    """
    Sets all the outputs to 0 and close the communication.
    """
    isRunning = False
    channels = ['0', '1', '2', '3', '4']
    for el in channels:
        writeChainArduino(el,'0')
        
    arduino.close()


class ArduinoListener(QtCore.QThread):
    """
    This class continuously listens the the serial port of the Arduino for an interlock signal.
    """

    interlockSignal = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while isRunning:
            interlockState = listens()
            if interlockState == 'true':
                data.isInterlocked = True
                self.interlockSignal.emit(data.isInterlocked)
            elif interlockState == 'false':
                data.isInterlocked = False
                self.interlockSignal.emit(data.isInterlocked)

            time.sleep(0.02)
