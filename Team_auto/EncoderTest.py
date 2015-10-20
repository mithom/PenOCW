from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import math
import time

BrickPiSetup()  # setup the serial port for sudo su communication
BrickPiSetupSensors()       #Send the properties of sensors to BrickPi
BrickPiUpdateValues()

d=56
O=math.pi*d

BrickPi.EncoderOffset[PORT_C] = BrickPi.Encoder[PORT_C]
BrickPi.EncoderOffset[PORT_D] = BrickPi.Encoder[PORT_D]
print BrickPi.Encoder[PORT_C]
print BrickPi.EncoderOffset[PORT_C]
print BrickPi.Encoder[PORT_D]
print BrickPi.EncoderOffset[PORT_D]

motorRotateDegree([150,150],[360,360],[PORT_D,PORT_C])

print BrickPi.Encoder[PORT_C]
print BrickPi.EncoderOffset[PORT_C]
print BrickPi.Encoder[PORT_D]
print BrickPi.EncoderOffset[PORT_D]
