# -*- coding: utf-8 -*-
"""
This method allows the main program to communicate with the Arduino board to set the values of the different outputs

Created on Mon Apr 15 16:55:32 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

import serial

arduino = serial.Serial('COM6', 115200) # Establish the connection on a specific port at a specific baud rate

def writeChainArduino(channel, power):
    """Writes a character chain with a predefined format to set the right value on the right digital output channel
    :type channel: string
    :type power:string
    """
    chain = '<' + channel + ',' + power + '>'
    for char in chain:
        byteChar = char.encode('utf-8')
        arduino.write(byteChar)
        
def close():
    """Sets all the outputs to 0 and close the communication
    """
    channels = ['0', '1', '2', '3', '4', '5']
    for el in channels:
        writeChainArduino(el,'0')
        
    arduino.close()