#!/usr/bin/env python3


import serial
import time
import sys



def main():

    try:
        goto = int(sys.argv[1])
    except:
        print("Usage: moovctl [pos]")
        sys.exit(1)

    if goto not in range(66,129):
        print("pos needs to be between 66 and 128")
        sys.exit(1)

    # print("ok")
    # sys.exit(0)

    s = serial.Serial(port="/dev/ttyUSB3", baudrate=9600)
    msg_up = [ 102, 2, 2, 216, 216 ]
    msg_down = [ 102, 1, 1, 216, 216 ]
    msg_stop = [ 102, 0, 0, 216, 216 ]
    msg = msg_stop
    do_stop = False
    while True:

        r = s.read(1)
        if r not in [b'\x00', b'\x98', b'\x03' ]:
            pos = ord(r)
            if pos > goto:
                #print("go down")
                msg = msg_down
            if pos < goto:
                #print("go up")
                msg = msg_up
            if pos == goto:
                #print("stahp it")
                msg = msg_stop
                do_stop = True

            print("{0}".format(ord(r)))

        s.write(msg)
        time.sleep(0.01)
        if do_stop:
            sys.exit(0)



if __name__ == '__main__':
    main()
