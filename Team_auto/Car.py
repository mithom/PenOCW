from BrickPi import BrickPi, BrickPiSetup, BrickPiSetupSensors, PORT_A, PORT_B, motorRotateDegree
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
O = math.pi * d  # circumference of the wheels

last_left_power = 0
last_right_power = 0

isUpdated = False


def BrickPiUpdateValues():
    global isUpdated
    update()
    isUpdated = True


def calibrate():
    global offset_A, offset_B
    BrickPi.MotorEnable[PORT_A] = 1
    BrickPi.MotorEnable[PORT_B] = 1
    set_left(1)
    set_right(1)
    offset_A = BrickPi.Encoder[PORT_A]
    offset_B = BrickPi.Encoder[PORT_B]
    while offset_A is None or offset_B is None:
        BrickPiUpdateValues()
        offset_A = BrickPi.Encoder[PORT_A]
        print offset_A
        print offset_B
        offset_B = BrickPi.Encoder[PORT_B]
    offset_A -= 10000
    offset_B -= 10000


def go_straight_manual(power, duration):
    # TODO: blijvende PID over functies heen, enkel bij starten 
	# opnieuw instellen, niet in deze functies dus
    left_power = power
    right_power = power
    set_motors(left_power, right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    while time.time() - start_time < duration:
        set_motors(left_power, right_power)
        BrickPiUpdateValues()


def go_straight_distance(power, distance):
    global offset_A, offset_B
    calibrate()

    main_power = 80
    left_power = main_power
    right_power = main_power
    set_motors(left_power, right_power)
    BrickPiUpdateValues()

    power_increase = (power-main_power)/(distance/20)
    step = 1

    average = 0
    degree = (distance / O) * 360

    proportional_factor = 100
    derivative_factor = 0
    integral_factor = 2000 #2000
    update_interval = 0.01
    pid_controller = PID.PID(proportional_factor, derivative_factor, integral_factor,
                             1, offset_A, offset_B, update_interval)
    start_time = time.time()
    last_update = time.time()
    while average < degree*2: # encoders are in half degrees
        if (time.time()-start_time) > step and main_power < power:
            left_power += power_increase
            right_power += power_increase
            main_power += power_increase
            step += 1
        pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            right_power = int((2*main_power)/(pid_ratio+1))
            left_power = int(pid_ratio*right_power)
	set_left(left_power)
	set_right(right_power)
#        set_motors(left_power, int(right_power))
        BrickPiUpdateValues()
        average = ((BrickPi.Encoder[PORT_A] - offset_A - 10000) +
                   (BrickPi.Encoder[PORT_B] - offset_B - 10000)) / 2


def go_straight_duration(power, duration):
    global offset_A, offset_B
    calibrate()
    main_power = 80
    left_power = main_power
    right_power = main_power
    set_motors(left_power, right_power)
    BrickPiUpdateValues()

    power_increase = (power-main_power)/(duration/20)
    step = 1

    start_time = time.time()
    update_interval = 0.01
    # proportional_factor = 3
    # derivative_factor = 0.3
    # integral_factor = 4
    proportional_factor = 0  # 12 # 100
    #    derivative_factor = 7
    derivative_factor = 0
    integral_factor = 2000  # 20 # 300
    pid_controller = PID.PID(proportional_factor, derivative_factor, integral_factor,
                             1, offset_A, offset_B, update_interval)
    last_update = time.time()
    while (time.time() - start_time) < duration:
        if (time.time()-start_time) > step and main_power < power:
            left_power += power_increase
            right_power += power_increase
            main_power += power_increase
            step += 1
            # encoder_A = BrickPi.Encoder[PORT_A] - offset_A
            # encoder_B = BrickPi.Encoder[PORT_B] - offset_B
        #        ratio = encoder_A / float(encoder_B)
        #        print 'Ratio: ', ratio
        pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        #        print 'PID ratio: ', pid_ratio
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            right_power = int((2*main_power)/(pid_ratio+1))
            # right_power = int(main_power/(pid_ratio/2.0))
            # left_power = int((pid_ratio/2.0)*right_power)
            left_power = int(pid_ratio*right_power)
        set_motors(left_power, int(0.9999*right_power))
        BrickPiUpdateValues()


def make_circle_left(power, radius):  # radius in cm
    global O, car_width
    calibrate()
    outer_distance = ((radius+car_width/2.0)*2)*math.pi
    inned_distance = ((radius - car_width/2.0)*2)*math.pi
    outer_rotations = outer_distance/O
    inner_rotations = inned_distance/O
    inner_degrees = inner_rotations*360
    outer_degrees = outer_rotations*360
    ratio = inner_degrees/outer_degrees
    motorRotateDegree([power, int(power*ratio)],[int(outer_degrees),int(inner_degrees)],[PORT_B,PORT_A])
    #int versie want floats mogen niet vor deze functie. geeft kleine afrondingsfiout bij reiden cirkel!


def make_circle_right(power, radius):
    calibrate()
    right_power = int(((radius - car_width) / radius) * power)
    set_left(power)
    set_right(right_power)
    BrickPiUpdateValues()


def rotate_angle_left(power, angle):
    # Angle in degrees
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_B, PORT_A], 0.01)


def rotate_angle_right(power, angle):
    # Angle in degrees
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_A, PORT_B])
#    motorRotateDegree([power, -power], [goal_angle_wheel, -goal_angle_wheel],
#	[PORT_A, PORT_B])

def turn_straight_left(power, duration):  # Voor rechte hoek buitenste wiel 360 laten draaien (via motorRotateDegree)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        set_left(-power)
        set_right(power)
        BrickPiUpdateValues()
        # motorRotateDegree([power],[360],[PORT_B])


def turn_straight_right(power, duration):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        set_left(power)
        set_right(-power)
        BrickPiUpdateValues()


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


def set_motors(power_A, power_B):
    if abs(power_A - power_B) < 100:
        if power_A in range(50, 100):  # power_A >= 50 and power_A < 100:
            power_A = int(power_A*0.952)
        elif power_B > 150:
            power_B = int(power_B*0.96)
    set_left(power_A)
    set_right(power_B)


def get_functions():
    functions = {'go_straight_distance': go_straight_distance, 'go_straight_duration1': go_straight_duration,
                 'go_straight_manual': go_straight_manual, 'make_circle_left': make_circle_left,
                 'make_circle_right': make_circle_right, 'rotate_angle_left': rotate_angle_left,
                 'rotate_angle_right': rotate_angle_left, 'turn_straight_left': turn_straight_left,
                 'turn_straight_right': turn_straight_right}
    return functions


def get_encoder_values():
    return BrickPi.Encoder[PORT_A] - offset_A, BrickPi.Encoder[PORT_B] - offset_B


def get_power_values():
    return last_left_power, last_right_power


calibrate()

if __name__ == '__main__':
    print "car.py is the main module, running the go straight distance"
#    go_straight_distance(100,40)
#    rotate_angle_right(100,100)
#    go_straight_distance(100,40)
#    rotate_angle_right(100,100)
#    go_straight_distance(100,40)
#    rotate_angle_right(100,100)
#    go_straight_distance(100,40)
    go_straight_distance(100,200)
