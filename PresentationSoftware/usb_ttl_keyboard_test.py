#!/usr/bin/env python3
"""
usb_ttl_keyboard_test.py

Requirements:
python -m pip install pyserial

Keyboard-driven test utility for a BIOPAC USB-TTL serial trigger module.
No PsychoPy.

Keys:
  SPACE : toggle TRIAL on/off (02 <-> 00)
  1..9  : pulse codes 01..09 (code then clear to 00)
  q     : quit (clears to 00)

Run:
  Windows: python usb_ttl_keyboard_test.py --port COM3
  macOS:   python usb_ttl_keyboard_test.py --port /dev/tty.usbserial-XXXX
"""

import argparse
import sys
import time
import serial

TRIAL_ON = 0x02
TRIAL_OFF = 0x00


def write_code(ser: serial.Serial, code: int) -> None:
    if not (0 <= code <= 255):
        raise ValueError("code must be 0..255")
    ser.write(f"{code:02X}".encode("ascii"))
    ser.flush()


def pulse(ser: serial.Serial, code: int, pulse_ms: int = 10) -> None:
    write_code(ser, code)
    time.sleep(pulse_ms / 1000.0)
    write_code(ser, 0x00)


def getch():
    """Read a single keypress (1 char) without Enter. Cross-platform."""
    if sys.platform.startswith("win"):
        import msvcrt
        ch = msvcrt.getch()
        # msvcrt returns bytes; decode safely
        try:
            return ch.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True, help="COM3 or /dev/tty.usbserial-XXXX")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--pulse-ms", type=int, default=10)
    ap.add_argument("--reset", action="store_true", help='Send "RR" on start (device-dependent)')
    args = ap.parse_args()

    ser = serial.Serial(args.port, args.baud, timeout=1, write_timeout=1)

    trial_state = False
    try:
        if args.reset:
            ser.write(b"RR")
            ser.flush()
            time.sleep(0.05)

        write_code(ser, TRIAL_OFF)

        print(f"Connected: {args.port} @ {args.baud}")
        print("SPACE=toggle 02/00, 1..9=pulse 01..09, q=quit")

        while True:
            ch = getch()

            if ch == "q":
                break

            if ch == " ":
                trial_state = not trial_state
                write_code(ser, TRIAL_ON if trial_state else TRIAL_OFF)
                print("TRIAL ON (02)" if trial_state else "TRIAL OFF (00)")
                continue

            if ch.isdigit() and ch != "0":
                code = int(ch)  # 1..9
                pulse(ser, code, pulse_ms=args.pulse_ms)
                print(f"PULSE {code:02X} then 00")
                continue

            # ignore other keys

    finally:
        try:
            write_code(ser, 0x00)
        except Exception:
            pass
        try:
            ser.close()
        except Exception:
            pass
        print("Exited (cleared to 00, port closed).")


if __name__ == "__main__":
    main()