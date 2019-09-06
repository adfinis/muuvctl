#!/usr/bin/env python3

import logging
import math
import sys
import time

import click
import serial

logger = logging.getLogger(__name__)

MUUV_UP = [0xD8, 0xD8, 0x66, 0x02, 0x02]
MUUV_DOWN = [0xD8, 0xD8, 0x66, 0x01, 0x01]
MUUV_STOP = [0xD8, 0xD8, 0x66, 0x00, 0x00]



def main():
    cli(obj={})


def setup_logging(debug=False):
    """Configure logging to stdout."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)

    stdout_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stdout_handler.setLevel(logging.INFO)
    if debug:
        stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(stdout_formatter)

    root.addHandler(stdout_handler)


def get_serial(port):
    s = serial.Serial(port=port, baudrate=9600)
    try:
        s = serial.Serial(port=port, baudrate=9600)
    except (OSError, serial.SerialException):
        logger.exception(f"ERROR: cannot open serial port {port}", exc_info=False)
        sys.exit(1)
    # delay for relay to kick in
    time.sleep(0.13)
    return s


def search_pos(r):
    if r not in [b"\x00", b"\x98", b"\x03", b"\x01"]:
        return ord(r)
    return False


@click.group()
@click.option("--port", default="/dev/ttyUSB0")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug, port):
    ctx.obj["port"] = port
    setup_logging(debug)


@cli.command(name="get")
@click.option("--follow", default=False, is_flag=True)
@click.pass_context
def get_pos(ctx, follow):
    s = get_serial(ctx.obj["port"])
    s.rts = 0
    while True:
        pos = search_pos(s.read(1))
        if pos:
            print(pos)
            if not follow:
                sys.exit(0)


@cli.command(name="goto")  # noqa: C901
@click.argument("pos", type=click.IntRange(66, 129))
@click.pass_context
def set_pos(ctx, pos):
    s = get_serial(ctx.obj["port"])
    while True:
        cpos = search_pos(s.read(1))
        if cpos:
            break

    time.sleep(0.13)
    diff = cpos - pos

    logger.debug(f"diff: {diff}")

    # We need to correct the final position to take the time it takes to stop
    # the movement into account.
    # TODO: export into dedicated function and implement PID loop :P

    # If the difference is > 4 we need to correct the position by 2
    if abs(diff) > 4:
        logger.debug("corr: 2")
        corr = 2
    # For a difference of > 1 we need to correct the position by 1
    elif abs(diff) > 1:
        logger.debug("corr: 1")
        corr = 1
    # For a difference of 1 we don't need to correct the position
    elif abs(diff) == 1:
        logger.debug("corr: 0")
        corr = 0
    # For a difference of 0 we don't need to change the height of the table
    elif abs(diff) == 0:
        sys.exit(0)

    # Set position to move to
    goto = pos + math.copysign(corr, diff)

    logger.debug(f"current pos: {cpos} goto: {goto}")

    do_stop = False
    msg = MUUV_STOP
    while True:
        cpos = search_pos(s.read(1))
        s.write(msg)
        if cpos:
            if cpos > goto:
                msg = MUUV_DOWN
            if cpos < goto:
                msg = MUUV_UP
            if cpos == goto:
                msg = MUUV_STOP
                do_stop = True
            logger.debug(f"{cpos}")

        logger.debug(msg)
        s.write(msg)
        time.sleep(0.01)
        if do_stop:
            sys.exit(0)


if __name__ == "__main__":
    main()
