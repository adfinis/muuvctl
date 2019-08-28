
cables
gnd => black
5v  => red
RX  => green
TX  => white

cable to serial:
gnd => gnd
rx  => tx
tx  => rx

proto pos move

b'f'  > 102
b'\x00' > 0 (no move) 1 (up) 2(down)
b'\x00' > 0
b'\xd8' > 216
b'\xd8' > 216


proto pos get

moved

b'\x98'
b'\x98'
b'\x03'
b'\x03'
b'O' <- position ord(pos)
b'O' <- position ord(pos)

idle

b'\x98'
b'\x98'
b'\x00'
b'\x00'
b'\x00'
b'L' <- position ord(pos)
b'L' <- position ord(pos)
