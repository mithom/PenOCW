from BrickPi import *  # import BrickPi.py file to use BrickPi operations
import time
import math
import PID

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
car_width = 11.5
wheel_contour = 17.8

BrickPiSetupSensors()  # Send the properties of sensors to BrickPi

def calibrate():
    print "start calibrate"
    set_left(150)
    set_right(150)
    offset_A= None
    offset_B= None
    while offset_A is None or offset_B is None:
        BrickPiUpdateValues()
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
    print "end calibrate"
    return (offset_A, offset_B)

def test(offset_A,offset_B):
    list = [50,100,150,200,250]
    for power in list:
        left_power = power
        right_power = power
        set_left(left_power)
        set_right(right_power)
        BrickPiUpdateValues()
        t = time.time()
        while time.time() - t < 5:
            pass
        encoder_A = BrickPi.Encoder[PORT_A] - offset_A
        encoder_B = BrickPi.Encoder[PORT_B] - offset_B
        print 'Power: ', power
        print '-------'
        print 'Encoder A: ', encoder_A
        print 'Encoder B: ', encoder_B
        ratio = encoder_A / float(encoder_B)
        print 'Ratio: ', ratio
        time.sleep(5)

time.sleep(2)
(offset_A, offset_B) = calibrate()
test(offset_A,offset_B)