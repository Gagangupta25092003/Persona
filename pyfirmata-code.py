from pyfirmata import Arduino, SERVO, util
from time import sleep

port = '/dev/ttyUSB0'
board = Arduino(port)

board.digital[8].mode = SERVO
while True:
    board.digital[8].write(0)
