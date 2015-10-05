from BrickPi import *   #import BrickPi.py file to use BrickPi operations

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

power = 0

class Car():
    """ Movement of the car """
    def __init__(self):

    def move_left(self, power):
        BrickPi.MotorSpeed[PORT_A] = power  #Set the speed of MotorA (-255 to 255)

    def move_right(self, power):
        BrickPi.MotorSpeed[PORT_B] = power  #Set the speed of MotorB (-255 to 255)

    def stop(self):
        BrickPi.MotorSpeed[PORT_A] = 0
        BrickPi.MotorSpeed[PORT_B] = 0

    def turn_straight_left(self, power):
        BrickPi.MotorSpeed[PORT_A] = - power
        BrickPi.MotorSpeed[PORT_B] = power

    def turn_straight_right(self, power):
        BrickPi.MotorSpeed[PORT_A] = power
        BrickPi.MotorSpeed[PORT_B] = - power

