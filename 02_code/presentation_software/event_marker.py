#!/usr/bin/env python3

# event_marking.py - 

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

import serial

# two byte hexadecimal codes for event marking
NO_TRIAL = b'00'    # trial is not running
TRIAL = b'02'       # trial is running

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(NO_TRIAL)

def begin_trial():
    try:
        ser.open()
    except serial.serialutil.SerialException:
        pass
    ser.write(TRIAL)

def end_trial():
    ser.write(NO_TRIAL)
    ser.close()

