#!/usr/bin/env python3

# event_marking.py - 

__author__ = 'Nicholas Greene'
__copyright__ = 'Copyright 2021 Nicholas Greene'
__license__ = 'MIT'
__version__ = '1.0'

import serial
import serial.tools.list_ports
import sys

# two byte hexadecimal codes for event marking
NO_TRIAL = b'00'    # trial is not running
TRIAL = b'02'       # trial is running


# Dummy class for simulation mode
class DummySerial:
    def write(self, data):
        print(f"[SIM] Writing: {data}")
    def close(self):
        print("[SIM] Closing port")
    def open(self):
        print("[SIM] Opening port")
    def flush(self):
        pass


# Try to connect to COM9

if len(sys.argv) > 1:
    requested_port = sys.argv[1]
else:
    requested_port = "COM9"  # default

fallback_port = "COM9"
ser = None
available_ports = [p.device for p in serial.tools.list_ports.comports()]
try:
    if requested_port in available_ports:
        ser = serial.Serial(requested_port, 115200, timeout=1, write_timeout=1)
        print(f"Connected to device on {requested_port}")

    elif requested_port == "COM3" and fallback_port in available_ports:
        ser = serial.Serial(fallback_port, 115200, timeout=1, write_timeout=1)
        print(f"COM3 not available. Connected to {fallback_port} instead.")

    else:
        raise serial.SerialException("No valid COM port available")

except serial.SerialException as e:
    print("Could not connect to any COM port:", e)
    print("Running in simulation mode")
    ser = DummySerial()

# Send NO_TRIAL at startup
ser.write(NO_TRIAL)
ser.flush()

def begin_trial():
    try:
        ser.open()  # does nothing in pyserial if already open
    except Exception:
        pass
    ser.write(TRIAL)
    ser.flush()
    print("Marker sent: b'02' (Trial Started)")


def end_trial():
    ser.write(NO_TRIAL)
    ser.flush()
    print("Marker sent: b'00' (Trial Ended)")
