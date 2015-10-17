from BrickPi import *  # import BrickPi.py file to use BrickPi operations
import time

BrickPiSetup()  # setup the serial port for communicationfrom BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
car_width = 11.5
wheel_contour = 5  # foute waarde

BrickPiSetupSensors()  # Send the properties of sensors to BrickPi


def execute_function_with_id(function_id, *args):
    for f in functions:
        if id(f) == function_id:
            f(*args)


def get_function_ids():
    function_ids = {'go_straight': id(go_straight), 'make_circle_left': id(make_circle_left),
                    'make_circle_right': id(make_circle_right), 'rotate_angle_left': id(rotate_angle_left),
                    'rotate_angle_right': id(rotate_angle_left),
                    'set_left': id(set_left), 'set_right': id(set_right), 'turn_straight_left': id(turn_straight_left),
                    'turn_straight_right': id(turn_straight_right)}
    return function_ids


def go_straight(power, duration):
    BrickPi.nMotorEncoder[PORT_A] = 0  # reset the value of encoder A to zero
    BrickPi.nMotorEncoder[PORT_B] = 0  # reset the value of encoder B to zero
    left_power = power
    right_power = power
    start_time = time.clock()
    while (time.clock() - start_time) < duration:
        if (BrickPi.nMotorEncoder[PORT_A] + 10 > BrickPi.nMotorEncoder[PORT_B]) and (
                BrickPi.nMotorEncoder[PORT_B] + 10 > BrickPi.nMotorEncoder[PORT_A]):
            set_left(left_power)
            set_right(right_power)
            BrickPiUpdateValues()
        elif BrickPi.nMotorEncoder[PORT_A] > BrickPi.nMotorEncoder[PORT_B]:
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
    BrickPi.nMotorEncoder[PORT_B] = 0
    goal_angle_wheel = int((angle * car_width * 360) / (2 * wheel_contour))  # in graden
    while BrickPi.nMotorEncoder[PORT_B] < goal_angle_wheel:
        turn_straight_left(power)


def rotate_angle_right(power, angle):
    """Angle in radians"""
    BrickPi.nMotorEncoder[PORT_A] = 0
    goal_angle_wheel = int((angle * car_width * 360) / (2 * wheel_contour))  # in graden
    while BrickPi.nMotorEncoder[PORT_A] < goal_angle_wheel:
        turn_straight_right(power)


def set_left(power):
    BrickPi.MotorSpeed[PORT_A] = power  # Set the speed of MotorA (-255 to 255)


def set_right(power):
    BrickPi.MotorSpeed[PORT_B] = power  # Set the speed of MotorB (-255 to 255)


def turn_straight_left(power):
    set_left(-power)
    set_right(power)
    BrickPiUpdateValues()


def turn_straight_right(power):
    set_left(power)
    set_right(-power)
    BrickPiUpdateValues()


functions = [go_straight, make_circle_left, make_circle_right, rotate_angle_left, rotate_angle_right, set_left,
             set_right, turn_straight_left, turn_straight_right]
