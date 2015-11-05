from BrickPi import BrickPi, BrickPiSetup, BrickPiSetupSensors, PORT_A, PORT_B, motorRotateDegree # import BrickPi.py file to use BrickPi operations
from BrickPi import BrickPiUpdateValues as update
import time
import math
import PID

BrickPiSetup()  # setup the serial port for communication from BrickPi import *

BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
car_width = 11.5
wheel_contour = 17.8
offset_A = None
offset_B = None
BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
d = 5.6  # diameter of the wheels
O = math.pi * d # circumference of the wheels

last_left_power = 0
last_right_power = 0

isUpdated = False


def BrickPiUpdateValues():
    global isUpdated
    update()
    isUpdated = True

def calibrate():
    global offset_A, offset_B
    print "start calibrate"
    BrickPi.MotorEnable[PORT_A] = 1
    BrickPi.MotorEnable[PORT_B] = 1
    set_left(1)
    set_right(1)
    offset_A = BrickPi.Encoder[PORT_A]
    offset_B = BrickPi.Encoder[PORT_B]
    while offset_A is None or offset_B is None:
        BrickPiUpdateValues()
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
    print "end calibrate"


def go_straight_distance(power, distance):
    global offset_A, offset_B, O, d
    print 'start go straight distance'
    calibrate()
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    update_interval = 0.01
    pid_controller = PID.PID(5, 5, 0, offset_A, offset_B, update_interval)
    last_update = 0
    average = 0
    print O, "omtrek"
    degree = (distance / O) * 360
    print degree, "degree"
    # counter = 0  # uitgecomment omdat niet nodig (eerst inwhile geset voor gebruikt
    # difference = 0
    while average < degree:
        print "while"
        average = ((BrickPi.Encoder[PORT_A] - offset_A) + (BrickPi.Encoder[PORT_B] - offset_B)) / 2
        difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
        pid_value = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            print "time to update our values"
            if pid_value < difference:
                # left_power -= int(abs(difference-pid_value))
                right_power += int(abs(difference - pid_value))
                set_left(power)
                set_right(right_power)
            elif pid_value > difference:
                left_power += int(abs(difference - pid_value))
                # right_power -= int(abs(difference-pid_value))
                set_left(left_power)
                set_right(power)
            else:
                set_left(power)
                set_right(power)
        print 'left: ' + str(left_power) + ", right: " + str(right_power)
        BrickPiUpdateValues()


def go_straight_duration1(power, duration):
    global offset_A, offset_B
    calibrate()
    left_power = power
    right_power = power
    set_motors(left_power,right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    update_interval = 0.1
    proportional_factor = 1.6
    derivative_factor = 0.01
    integral_factor = 1.5
    pid_controller = PID.PID(proportional_factor,derivative_factor, integral_factor, 1, offset_A, offset_B, update_interval)
    last_update = time.time()
    with open('values.txt', 'w') as f:
        f.write('New PID --------')
        while (time.time() - start_time) < duration:
	    if derivative_factor < 0.5:
	        derivative_factor += 0.02
	    else:
	        print 'MAX DERIVATIVE ---------------------------------------------------------'
            encoder_A = BrickPi.Encoder[PORT_A] - offset_A
            encoder_B = BrickPi.Encoder[PORT_B] - offset_B
            if encoder_B != 0:
                ratio = encoder_A / float(encoder_B)
            else:
                ratio = 1
            f.write(str(ratio) + ',')
            print 'Ratio: ', ratio
            pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
            print 'PID ratio: ', pid_ratio
            if (time.time() - last_update) > update_interval:
                last_update = time.time()
                right_power = int((2*power)/(pid_ratio+1))
                left_power = int(pid_ratio*right_power)
                set_motors(left_power, right_power) 
            BrickPiUpdateValues()

def go_straight_duration(power, duration):
    global offset_A, offset_B
    calibrate()
    print 'start'
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    update_interval = 0.01
    pid_controller = PID.PID(5, 5, 0, offset_A, offset_B, update_interval)
    last_update = 0
    # difference = 0  # uitgecomment omdat eerst geset in while, dus nog niet nodig
    # counter = 0
    with open('values.txt', 'w') as f:
        # f = open('values.txt','w')
        while (time.time() - start_time) < duration:
            difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
            f.write(str(difference) + ',')
            print "difference", difference
            pid_value = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
            if (time.time() - last_update) > update_interval:
                last_update = time.time()
                if pid_value < difference:
                    # rechts sneller
                    # left_power -= abs(difference-pid_value)
                    right_power += int(abs(difference - pid_value))
                    set_left(power)
                    set_right(right_power)
                elif pid_value > difference:
                    # rechts sneller
                    left_power += int(abs(difference - pid_value))
                    # right_power += abs(difference-pid_value)power
                    set_left(left_power)
                    set_right(power)
                else:
                    set_left(power)
                    set_right(power)
            print 'left: ' + str(left_power) + ", right: " + str(right_power)
            BrickPiUpdateValues()
            # f.close()


def make_circle_left(power, radius):  # radius in cm
    calibrate()
    left_power = int(((radius - car_width) / radius) * power)
    set_left(left_power)
    set_right(power)
    BrickPiUpdateValues()


def make_circle_right(power, radius):
    calibrate()
    right_power = int(((radius - car_width) / radius) * power)
    set_left(power)
    set_right(right_power)
    BrickPiUpdateValues()


def rotate_angle_left(power, angle):
    """Angle in degrees"""
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_B, PORT_A])


def rotate_angle_right(power, angle):
    """Angle in degrees"""
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_A, PORT_B])


def turn_straight_left(power, duration):  # Voor rechte hoek buitenste wiel 360 laten draaien (via motorRotateDegree)
    start_time = time.time()
    if (time.time() - start_time) < duration:
        set_left(-power)
        set_right(power)
        BrickPiUpdateValues()
        # motorRotateDegree([power],[360],[PORT_B])


def turn_straight_right(power, duration):
    start_time = time.time()
    if (time.time() - start_time) < duration:
        set_left(power)
        set_right(-power)
        BrickPiUpdateValues()


deviations_per_power = {50: 1.2, 100: 1.0}


def set_left(power):
    global last_left_power
    if power > 255:
        last_left_power = 255
        BrickPi.MotorSpeed[PORT_A] = 255
    elif power < -255:
        last_left_power = -255
        BrickPi.MotorSpeed[PORT_A] = -255
    else:
        last_left_power = power
        BrickPi.MotorSpeed[PORT_A] = power  # Set the speed of MotorA (-255 to 255)


def set_motors(power_A, power_B):
    if abs(power_A - power_B) < 100:
        if power_A >= 50 and power_A < 100:
            power_A = int(power_A*0.952)
        elif power_B > 150:
            power_B = int(power_B*0.96)
    set_left(power_A)
    set_right(power_B)


def set_right(power):
    global last_right_power
    if power > 255:
        last_right_power = 255
        BrickPi.MotorSpeed[PORT_B] = 255
    elif power < -255:
        last_right_power = -255
        BrickPi.MotorSpeed[PORT_B] = -255
    else:
        last_right_power = power
        BrickPi.MotorSpeed[PORT_B] = power  # Set the speed of MotorA (-255 to 255)


def get_functions():
    functions = {'go_straight_distance': go_straight_distance, 'go_straight_pid': go_straight_duration,
                 'make_circle_left': make_circle_left, 'make_circle_right': make_circle_right,
                 'rotate_angle_left': rotate_angle_left, 'rotate_angle_right': rotate_angle_left,
                 'turn_straight_left': turn_straight_left, 'turn_straight_right': turn_straight_right}
    return functions


def get_encoder_values():
    return BrickPi.Encoder[PORT_A] - offset_A, BrickPi.Encoder[PORT_B] - offset_B


def get_power_values():
    return last_left_power, last_right_power

"""
def brake():
    while(power>5):
        set_left(power-10)
        set_right(power-10)
        BrickPiUpdateValues()
        power -= 10
    set_left(0)
    set_right(0)
    BrickPiUpdateValues()
    power = 0"""

calibrate()

if __name__ == '__main__':
    print "car.py is the main module, running the go straight distance"
    go_straight_duration1(150,10)
