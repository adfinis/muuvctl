#!/usr/bin/env python3


import serial


def main():
    s = serial.Serial(port="/dev/ttyUSB3", baudrate=9600)
    is_pos=False
    nc=0
    while True:
        r = s.read(1)
        print(r)



if __name__ == '__main__':
    main()
