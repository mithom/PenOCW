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
    set_left(1)
    set_right(1)
    offset_A= None
    offset_B= None
    while offset_A is None or offset_B is None:
        BrickPiUpdateValues()
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
    print "end calibrate"
    return (offset_A, offset_B)

def test1(offset_A,offset_B):
    list = [50, 100,150,200,250]
    for power in list:
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
        left_power = power
        right_power = power
        set_left(left_power)
        set_right(right_power)
        BrickPiUpdateValues()
        t = time.time()
        while time.time() - t < 10:
            BrickPiUpdateValues()
        encoder_A = BrickPi.Encoder[PORT_A] - offset_A
        encoder_B = BrickPi.Encoder[PORT_B] - offset_B
        print 'Power: ', power
        print '-------'
        print 'Encoder A: ', encoder_A
        print 'Encoder B: ', encoder_B
        ratio = encoder_A / float(encoder_B)
        print 'Ratio: ', ratio
        time.sleep(5)

def test2(offset_A,offset_B):
    list = [50, 100,150,200,250]
    for power in list:
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
        left_power = power
        right_power = power
        set_left(left_power)
        set_right(right_power)
        BrickPiUpdateValues()
        t = time.time()
        step = 1
        while time.time() - t < 10:
            BrickPiUpdateValues()
            if time.time()-t  > step:
                encoder_A = BrickPi.Encoder[PORT_A] - offset_A
                encoder_B = BrickPi.Encoder[PORT_B] - offset_B
                print 'Power: ', power
                print '-------'
                print 'Running for ', step, ' seconds.'
                print 'Encoder A: ', encoder_A
                print 'Encoder B: ', encoder_B
                ratio = encoder_A / float(encoder_B)
                print 'Ratio: ', ratio
                step += 1
        time.sleep(5)

def set_left(power):
    power += 15
    if power > 255:
        BrickPi.MotorSpeed[PORT_A] = 255
    elif power < -255:
        BrickPi.MotorSpeed[PORT_A] = -255
    else:
        BrickPi.MotorSpeed[PORT_A] = power  # Set the speed of MotorA (-255 to 255)


def set_right(power):
    if power > 255:
        BrickPi.MotorSpeed[PORT_B] = 255
    elif power < -255:
        BrickPi.MotorSpeed[PORT_B] = -255
    else:
        BrickPi.MotorSpeed[PORT_B] = power  # Set the speed of MotorA (-255 to 255)

(offset_A, offset_B) = calibrate()
test2(offset_A,offset_B)
