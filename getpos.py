#!/usr/bin/env python3

import sys
import serial


def main():
    s = serial.Serial(port="/dev/ttyUSB3", baudrate=9600)
    is_pos=False
    nc=0
    while True:
        r = s.read(1)
        if r not in [b'\x00', b'\x98', b'\x03' ]:
            print("{0}".format(ord(r)))
            sys.exit(0)


if __name__ == '__main__':
    main()
