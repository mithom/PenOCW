from BrickPi import BrickPi, BrickPiSetup, BrickPiSetupSensors, PORT_A, PORT_B, motorRotateDegree
from BrickPi import BrickPiUpdateValues as update
import time
import math
import PID
import webserver


BrickPiSetup()  # setup the serial port for communication from BrickPi import *

last_right_power = 0
last_left_power = 0


BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
car_width = 11.5
wheel_contour = 17.8
offset_A = None
offset_B = None
BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
d = 5.6  # diameter of the wheels
O = math.pi * d  # circumference of the wheels

isUpdated = time.time()

def BrickPiUpdateValues():
    global isUpdated
    if time.time() - isUpdated > 0.1:
        print "sending powers"
        webserver.hostfile.sendPower(get_power_values())
        isUpdated = time.time()
    update()

def calibrate(power_left = 1, power_right = 1):
    global offset_A, offset_B
    BrickPi.MotorEnable[PORT_A] = 1
    BrickPi.MotorEnable[PORT_B] = 1
    set_left(power_left)
    set_right(power_right)
    BrickPiUpdateValues()
    offset_A = BrickPi.Encoder[PORT_A]
    offset_B = BrickPi.Encoder[PORT_B]
    while offset_A is None or offset_B is None:
        BrickPiUpdateValues()
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]


def go_straight_manual(power, duration):
    # TODO: blijvende PID over functies heen, enkel bij starten 
    # opnieuw instellen, niet in deze functies dus
    calibrate(power,power)
    left_power = power
    right_power = power
    set_motors(left_power, right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    while time.time() - start_time < duration:
        set_motors(left_power, right_power)
        BrickPiUpdateValues()


def go_straight_camera1(left, right, duration):
    # calibrate(main_power, main_power)
    # right_power = int((2*main_power)/(ratio+1))
    # left_power = int(ratio*right_power)
    calibrate(left, right)
    set_motors(left, right)
    BrickPiUpdateValues()
    start_time = time.time()
    while time.time() - start_time < duration:
        set_motors(left, right)
        BrickPiUpdateValues()
    left_power = left
    right_power = right
    set_motors(left_power, right_power)
    BrickPiUpdateValues()

    proportional_factor = 250 #250 -> 300 -> 190 # 93
    derivative_factor = 0 # 10 / 0
    integral_factor = 500 #500
    update_interval = 0.0001
    target_ratio = 1
    pid_controller = PID.PID(proportional_factor, derivative_factor, integral_factor,
                             target_ratio, offset_A, offset_B, update_interval)
    start_time = time.time()
    last_update = time.time()
    while time.time() - start_time < duration: # encoders are in half degrees
#        if (time.time()-start_time) > step and main_power < power:
#            left_power += power_increase
#            right_power += power_increase
#            main_power += power_increase
#            step += 1
        pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            right_power = int((2*right_power)/(pid_ratio+1))
            left_power = int(pid_ratio*right_power)
        #set_left(left_power)
        #set_right(right_power)
        set_motors(left_power, int(right_power))
        BrickPiUpdateValues()
        average = ((BrickPi.Encoder[PORT_A] - offset_A) + #-10000
                   (BrickPi.Encoder[PORT_B] - offset_B)) / 2 #-10000
    #encoder_difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
    #if encoder_difference > 0:
    #    motorRotateDegree([100],[int(encoder_difference/2)],[PORT_B])
    #if encoder_difference < 0:
    #    motorRotateDegree([100],[-int(encoder_difference/2)],[PORT_A])
    set_motors(0,0)
    BrickPiUpdateValues()
    time.sleep(0.05)
    results = pid_controller.get_results()
    # print str(results)


def go_straight_camera(left, right, duration):
    # calibrate(main_power, main_power)
    # right_power = int((2*main_power)/(ratio+1))
    # left_power = int(ratio*right_power)
    calibrate(left, right)
    set_motors(left, right)
    BrickPiUpdateValues()
    start_time = time.time()
    while time.time() - start_time < duration:
        set_motors(left, right)
        BrickPiUpdateValues()


def go_straight_distance(power, distance):
    global offset_A, offset_B

    main_power = 150
    calibrate(main_power, main_power)
    left_power = main_power
    right_power = main_power
    set_motors(left_power, right_power)
    BrickPiUpdateValues()

#    power_increase = (power-main_power)/(distance/20)
#    step = 1

    average = 0
    degree = (distance / O) * 360

    proportional_factor = 250 #250 -> 300 -> 190 # 93
    derivative_factor = 0 # 10 / 0
    integral_factor = 500 #500
    update_interval = 0.0001
    target_ratio = 1
    pid_controller = PID.PID(proportional_factor, derivative_factor, integral_factor,
                             target_ratio, offset_A, offset_B, update_interval)
    start_time = time.time()
    last_update = time.time()
    while average < degree*2: # encoders are in half degrees
#        if (time.time()-start_time) > step and main_power < power:
#            left_power += power_increase
#            right_power += power_increase
#            main_power += power_increase
#            step += 1
        pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            right_power = int((2*main_power)/(pid_ratio+1))
            left_power = int(pid_ratio*right_power)
        #set_left(left_power)
        #set_right(right_power)
        set_motors(left_power, int(right_power))
        BrickPiUpdateValues()
        average = ((BrickPi.Encoder[PORT_A] - offset_A) + #-10000
                   (BrickPi.Encoder[PORT_B] - offset_B)) / 2 #-10000
    #encoder_difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
    #if encoder_difference > 0:
    #    motorRotateDegree([100],[int(encoder_difference/2)],[PORT_B])
    #if encoder_difference < 0:
    #    motorRotateDegree([100],[-int(encoder_difference/2)],[PORT_A])
    set_motors(0,0)
    BrickPiUpdateValues()
    time.sleep(0.05)
    results = pid_controller.get_results()
    # print str(results)


def make_circle_left(power, radius, degree):  # radius in cm
    global O, car_width
    calibrate()
    outer_distance = (2*radius + car_width)*math.pi
    inned_distance = (2*radius - car_width)*math.pi
    outer_rotations = outer_distance/O
    inner_rotations = inned_distance/O
    inner_degrees = inner_rotations*degree
    outer_degrees = outer_rotations*degree
    ratio = inner_degrees/outer_degrees
    motorRotateDegree([power, int(power*ratio)],[int(outer_degrees),int(inner_degrees)],[PORT_B,PORT_A])
    #int versie want floats mogen niet vor deze functie. geeft kleine afrondingsfiout bij reiden cirkel!


def make_circle_right(power, radius, degree):
    global O, car_width
    calibrate()
    outer_distance = ((radius+car_width/2.0)*2)*math.pi
    inned_distance = ((radius - car_width/2.0)*2)*math.pi
    outer_rotations = outer_distance/O
    inner_rotations = inned_distance/O
    inner_degrees = inner_rotations*degree
    outer_degrees = outer_rotations*degree
    ratio = inner_degrees/outer_degrees
    motorRotateDegree([power, int(power*ratio)],[int(outer_degrees),int(inner_degrees)],[PORT_A,PORT_B])


def rotate_left_angle(power, angle):
    # Angle in degrees
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_B, PORT_A], 0.01)


def rotate_right_angle(power, angle):
    # Angle in degrees
    goal_angle_wheel = int((angle * car_width * 2) / 5.6)  # in graden
    motorRotateDegree([power, 0], [goal_angle_wheel, 0], [PORT_A, PORT_B])
#    motorRotateDegree([power, -power], [goal_angle_wheel, -goal_angle_wheel],
#	[PORT_A, PORT_B])

def rotate_left_duration(power, duration):
    calibrate(-power,power)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        set_left(-power)
        set_right(power)
        BrickPiUpdateValues()
        # motorRotateDegree([power],[360],[PORT_B])


def rotate_right_duration(power, duration):
    calibrate(power,-power)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        set_left(power)
        set_right(-power)
        BrickPiUpdateValues()


def set_left(power):
    global last_left_power
    BrickPi.MotorEnable[PORT_A] = 1
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
    BrickPi.MotorEnable[PORT_B] = 1
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


def sleep(duration):
    time.sleep(duration)


def get_functions():
    functions = {'go_straight_distance': go_straight_distance,
                 'go_straight_manual': go_straight_manual, 'make_circle_left': make_circle_left,
                 'make_circle_right': make_circle_right, 'rotate_left_angle': rotate_left_angle,
                 'rotate_right_angle': rotate_right_angle, 'rotate_left_duration': rotate_left_duration,
                 'rotate_right_duration': rotate_right_duration, 'sleep': sleep,
                 'set_powers': go_straight_camera}
    return functions


def get_power_values():
    return last_left_power, last_right_power

if __name__ == '__main__':
    print "car.py is the main module, running the go straight distance"
    go_straight_distance(100,200)
