from BrickPi import *  # import BrickPi.py file to use BrickPi operations
import time

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
car_width = 11.5
wheel_contour = 17.8  # foute waarde

BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
offset_A= None
offset_B= None

def execute_function_with_id(function_id, *args, **kwargs):
    for f in functions:
        if id(f) == function_id:
            f(*args, **kwargs)


def get_function_ids():
    function_ids = {'go_straight': id(go_straight), 'make_circle_left': id(make_circle_left),
                    'make_circle_right': id(make_circle_right), 'rotate_angle_left': id(rotate_angle_left),
                    'rotate_angle_right': id(rotate_angle_left),
                    'set_left': id(set_left), 'set_right': id(set_right), 'turn_straight_left': id(turn_straight_left),
                    'turn_straight_right': id(turn_straight_right)}
    return function_ids


def go_straight(power, duration):
    BrickPi.Encoder[PORT_A] = 0
    BrickPi.Encoder[PORT_B] = 0  # reset the value of encoder B to zero
    left_power = power
    right_power = power
    start_time = time.time()
    while (time.time() - start_time) < duration:
        if (BrickPi.Encoder[PORT_A] + 100 > BrickPi.Encoder[PORT_B]) and (
                BrickPi.Encoder[PORT_B] + 100 > BrickPi.Encoder[PORT_A]):
            set_left(left_power)
            set_right(right_power)
            BrickPiUpdateValues()
        elif BrickPi.Encoder[PORT_A] > BrickPi.Encoder[PORT_B]:
            left_power -= 1
            right_power += 1
            set_left(left_power)
            set_right(right_power)
            #BrickPi.Encoder[PORT_A] = 0
            #BrickPi.Encoder[PORT_B] = 0
            BrickPi.EncoderOffset[PORT_A] = BrickPi.Encoder[PORT_A]
            BrickPi.EncoderOffset[PORT_B] = BrickPi.Encoder[PORT_B]
            BrickPiUpdateValues()
        else:
            left_power += 1
            right_power -= 1
            set_left(left_power)
            set_right(right_power)
            #BrickPi.Encoder[PORT_A] = 0
            #BrickPi.Encoder[PORT_B] = 0
            BrickPi.EncoderOffset[PORT_A] = BrickPi.Encoder[PORT_A]
            BrickPi.EncoderOffset[PORT_B] = BrickPi.Encoder[PORT_B]
            BrickPiUpdateValues()


def make_circle_left(power, radius):
    left_power = int(((radius - car_width) / radius) * power)
    set_left(left_power)
    set_right(power)
    BrickPiUpdateValues()


def make_circle_right(power, radius):
    right_power = int(((radius - car_width) / radius) * power)
    set_left(power)
    set_right(right_power)
    BrickPiUpdateValues()


def rotate_angle_left(power, angle):
    """Angle in radians"""
    BrickPi.Encoder[PORT_B] = 0
    goal_angle_wheel = int((angle * car_width * 360) / (2 * wheel_contour))  # in graden
    while BrickPi.Encoder[PORT_B] < goal_angle_wheel:
        turn_straight_left(power)


def rotate_angle_right(power, angle):
    """Angle in radians"""
    BrickPi.Encoder[PORT_A] = 0
    goal_angle_wheel = int((angle * car_width * 360) / (2 * wheel_contour))  # in graden
    while BrickPi.Encoder[PORT_A] < goal_angle_wheel:
        turn_straight_right(power)


def set_left(power):
    BrickPi.MotorSpeed[PORT_A] = power  # Set the speed of MotorA (-255 to 255)


def set_right(power):
    BrickPi.MotorSpeed[PORT_B] = power  # Set the speed of MotorB (-255 to 255)


def turn_straight_left(power):      # Voor rechte hoek buitenste wiel 360 laten draaien (via motorRotateDegree)
    set_left(-power)
    set_right(power)
    BrickPiUpdateValues()


def turn_straight_right(power):
    set_left(power)
    set_right(-power)
    BrickPiUpdateValues()


def stop():
    set_right(0)
    set_left(0)
    BrickPiUpdateValues()


def brake():
    while(power>5):
        set_left(power-10)
        set_right(power-10)
        BrickPiUpdateValues()
        power -= 10
    set_left(0)
    set_right(0)
    BrickPiUpdateValues()
    power = 0

functions = [go_straight, make_circle_left, make_circle_right, rotate_angle_left, rotate_angle_right, set_left,
             set_right, turn_straight_left, turn_straight_right]

time.sleep(10)

while True:
    go_straight(100,10)
    BrickPiUpdateValues()
    #if offset_A == None or offset_B == None:
    #    offset_A = BrickPi.Encoder[PORT_A]
    #    offset_B = BrickPi.Encoder[PORT_B]
##    else:
##        print BrickPi.Encoder[PORT_A] - offset_A
##        print BrickPi.Encoder[PORT_B] - offset_B
    


##            print 'left',
##            print left_power,
##            print
##            print 'right',
##            print right_power,
##            print left_power
##            print right_power
