#!/usr/bin/env python3


import sys
import time
import click
import serial

MUUV_UP   = [ 102, 2, 2, 216, 216 ]
MUUV_DOWN = [ 102, 1, 1, 216, 216 ]
MUUV_STOP = [ 102, 0, 0, 216, 216 ]


def get_serial(port):
    try:
        s = serial.Serial(port=port, baudrate=9600)
    except:
        print(f"ERROR: cannot open serial port {port}")
        sys.exit(1)
    # delay for relay to kick in
    time.sleep(0.08)
    return s


def search_pos(r):
    if r not in [b'\x00', b'\x98', b'\x03' ]:
        return ord(r)
    return False


@click.group()
@click.option('--port', default="/dev/ttyUSB3")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug, port):
    ctx.obj['debug']  = debug
    ctx.obj['port'] = port
    pass


@cli.command(name='get')
@click.option('--follow', default=False, is_flag=True)
@click.pass_context
def get_pos(ctx, follow):
    s = get_serial(ctx.obj['port'])
    s.rts = 0
    while True:
        pos = search_pos(s.read(1))
        if pos:
            print(pos)
            if not follow:
                sys.exit(0)


@cli.command(name='goto')
@click.argument('pos', type=click.IntRange(66, 129))
@click.pass_context
def set_pos(ctx, pos):
    s = get_serial(ctx.obj['port'])
    while True:
        cpos = search_pos(s.read(1))
        if cpos:
            break


    time.sleep(0.1)
    diff = cpos - pos
    if diff==0:
        sys.exit(0)
    if ctx.obj['debug']:
        print(f"diff: {diff}")
    if (diff >= 1) or (diff <= -1) :
        if ctx.obj['debug']:
            print("corr: 0")
        goto = pos
    if (diff > 1) or (diff < -1) :
        if ctx.obj['debug']:
            print("corr: 1")
        if cpos > pos:
            goto = pos+1
        else:
            goto = pos-1
    if (diff > 4) or (diff < -4) :
        if ctx.obj['debug']:
            print("corr: 2")
        if cpos > pos:
            goto = pos+2
        else:
            goto = pos-2

    if ctx.obj['debug']:
        print(f"current pos: {cpos} goto: {goto}")

    do_stop = False
    msg=MUUV_STOP
    while True:
        cpos = search_pos(s.read(1))

        if cpos:
            if cpos > goto:
                msg = MUUV_DOWN
            if cpos < goto:
                msg = MUUV_UP
            if cpos == goto:
                msg = MUUV_STOP
                do_stop = True
            if ctx.obj['debug']:
                print(f"{cpos}")

        if ctx.obj['debug']:
            print(msg)
        s.write(msg)
        time.sleep(0.01)
        if do_stop:
            sys.exit(0)



if __name__ == '__main__':
    cli(obj={})
