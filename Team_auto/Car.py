from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

def set_left(power):
    BrickPi.MotorSpeed[PORT_A] = power  #Set the speed of MotorA (-255 to 255)

def set_right(power):
    BrickPi.MotorSpeed[PORT_B] = power  #Set the speed of MotorB (-255 to 255)

def turn_straight_left(power):
    BrickPi.MotorSpeed[PORT_A] = - power
    BrickPi.MotorSpeed[PORT_B] = power

def turn_straight_right(power):
    BrickPi.MotorSpeed[PORT_A] = power
    BrickPi.MotorSpeed[PORT_B] = - power

set_left(100)
