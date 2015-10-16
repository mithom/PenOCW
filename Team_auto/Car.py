from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import time

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
       
def set_left(power):
    BrickPi.MotorSpeed[PORT_A] = power  #Set the speed of MotorA (-255 to 255)

def set_right(power):
    BrickPi.MotorSpeed[PORT_B] = power  #Set the speed of MotorB (-255 to 255)

def turn_straight_left(power):
    set_left(-power)
    set_right(power)
    BrickPiUpdateValues()

def turn_straight_right(power):
    set_left(power)
    set_right(-power)
    BrickPiUpdateValues()

def go_straight(power, duration):
	BrickPi.nMotorEncoder[PORT_A] = 0 #reset the value of encoder A to zero
	BrickPi.nMotorEncoder[PORT_B] = 0 #reset the value of encoder B to zero
	left_power = power
	right_power = power
	start_time = time.clock()
	while (time.clock() - start_time < duration):
		if (BrickPi.nMotorEncoder[PORT_A] +10 > BrickPi.nMotorEncoder[PORT_B]) and (BrickPi.nMotorEncoder[PORT_B] +10 > BrickPi.nMotorEncoder[PORT_A]):
			set_left(left_power)
			set_right(right_power)
			BrickPiUpdateValues()
		elif (BrickPi.nMotorEncoder[PORT_A] > BrickPi.nMotorEncoder[PORT_B]):
			correction_factor = "blehbleh"
			left_power -= correction_factor
			right_power += correction_factor
			set_left(left_power)
			set_right(right_power)
			BrickPiUpdateValues()
		else:
			correction_factor = "blehbleh"
			left_power += correction_factor
			right_power -= correction_factor
			set_left(left_power)
			set_right(right_power)
			BrickPiUpdateValues
			
def make_circle_left(power, radius)
    left_power = int (((radius - 11.5)/ radius)*power)
    set_left(left_power)
    set_right (power)
    BrickPiUpdateValues()

