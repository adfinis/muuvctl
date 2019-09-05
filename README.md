# muuvctl

Control muuv tables with a command line tool

## Wiring

### Basics

* Open the frontend controller
* Solder a 3-Pin cable to `RX`,`TX` and `GND`
* Connect `RX`,`TX` and `GND` to a USB-> UART controller

![](./doc/board.png)

### Using controller while USB plugged in

The basic wiring has the disadvantage that only the UART-Controller can control the table and the muuv-device is disfunctional. It can be fixed with a relay connected to `RTS` line of the UART which breaks the `RX` line. It is important that the relay is high trigger.

![](./doc/relay-circuit.png)

## Installing

### System wide:
```
pip install .
```

### For current user:
```
pip install --user .
```
In order to run `muuvctl` from commandline, make sure that `/home/$USER/.local/bin` is in your `$PATH`

### Bash completion

Add the following to your  `.bashrc`:
```
complete -W "--debug --port get goto --follow" muuvctl
```

## Usage

Move the table to position 80:
```
muuvctl goto 80
```

Get current position of the table:
```
muuvctl get
```

Get live position of the table:
```
muuvctl get --follow
```



## Serial protocol

The protocol seemst to be called TiMOTION F-Bus.
Baudrate is: `9600`
The following is known (possibly not everything that the controller can do):

### RX
The controller tin the table sends the following:
```c
uint8_t StartByte =  0x98;
uint8_t StartByte =  0x98;
uint8_t Param;
uint8_t Param;
uint8_t Data;
uint8_t Data;
```
`Param` is the following:
```c
STOPPED      =  0x00;
SAVE_TRIGGED =  0x01;
MOVING       =  0x03;
```
`Data` is normally the position of the table.

### TX

You need to send the following struct to control it
```c
uint8_t StartByte = 0xD8;
uint8_t StartByte = 0xD8;
uint8_t Param;
uint8_t Command;
uint8_t Command;
```
Only known value for `Param` is `0x66` which is used in all commands.


`Command` is the following:
```c
STOP  = 0x00;
DOWN  = 0x01;
UP    = 0x02;
RESET = 0x03;
POS1  = 0x04;
POS2  = 0x08;
POS3  = 0x10;
POS4  = 0x20;
SAVE  = 0x40;
```

#### TX Examples

* Move up: `0xD8, 0xD8, 0x66, 0x02, 0x02`
* Move down: `0xD8, 0xD8, 0x66, 0x01, 0x01`
* Stop: `0xD8, 0xD8, 0x66, 0x00, 0x00`
* Goto POS1: `0xD8, 0xD8, 0x66, 0x04, 0x04`
* Goto POS4: `0xD8, 0xD8, 0x66, 0x20, 0x20`
* Reset: `0xD8, 0xD8, 0x66, 0x03, 0x03`   

##### Save
* Send min. 32x SAFE: `0xD8, 0xD8, 0x66, 0x40, 0x40`
* Optional: wait until table sends: `0x98, 0x98, 0x01, 0x01, POS, POS `
* Send 4x wanted POS, for POS1: `0xD8, 0xD8, 0x66, 0x04, 0x04`
* Send 1x STOP: `0xD8, 0xD8, 0x66, 0x00, 0x00`


#### Notes

There seems to be no way to move the table to an specific position. You need to send up or down until the table reaches the desired position, then send stop.




## Contributing

Please let us know what you would like to contribute before you get invested! This is really just a proof of concept at this stage.

### pre-commit hook

```bash
pip install pre-commit
pip install -r requirements-dev.txt -U
pre-commit install
```
