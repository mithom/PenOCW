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
    set_left(1)
    set_right(1)
    BrickPiUpdateValues()
    offset_A= None
    offset_B= None
    while offset_A is None or offset_B is None:
        offset_A = BrickPi.Encoder[PORT_A]
        offset_B = BrickPi.Encoder[PORT_B]
    return (offset_A, offset_B)


def go_straight_distance(power, distance):
    print 'start'
    global offset_A, offset_B
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    update_interval = 0.05
    difference = 0
    pid_controller = PID.PID(5,5,0,offset_A,offset_B,update_interval)
    last_update = 0
    counter = 0
    average = 0
    d=56
    O=math.pi*d
    degree = (distance/O)*360
    print degree
    while average < degree:
        average = ((BrickPi.Encoder[PORT_A]-offset_A)+(BrickPi.Encoder[PORT_B]-offset_B))/2
        difference = (BrickPi.Encoder[PORT_A]-offset_A)-(BrickPi.Encoder[PORT_B]-offset_B)
        pid_value = pid_controller.update(BrickPi.Encoder[PORT_A],BrickPi.Encoder[PORT_B])
        if ((time.time()-last_update)>update_interval):
            if pid_value < difference:
                left_power -= int(abs(difference-pid_value))
                right_power += int(abs(difference-pid_value))
                set_left(power)
                set_right(right_power)
                BrickPiUpdateValues()
            elif pid_value > difference:
                left_power += int(abs(difference-pid_value))
                right_power -= int(abs(difference-pid_value))
                set_left(left_power)
                set_right(power)
                BrickPiUpdateValues()
            else:
                set_left(power)
                set_right(power)
                BrickPiUpdateValues()
        last_update = time.time()


def go_straight_duration(power, duration):
    global offset_A, offset_B
    print 'start'
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    update_interval = 0.05
    difference = 0
    pid_controller = PID.PID(5,5,0,offset_A,offset_B,update_interval)
    last_update = 0
    counter = 0
    f = open('values.txt','w')
    while ((time.time() - start_time) < duration):
        difference = (BrickPi.Encoder[PORT_A]-offset_A)-(BrickPi.Encoder[PORT_B]-offset_B)
        f.write(str(difference) + ',')
        print difference
        pid_value = pid_controller.update(BrickPi.Encoder[PORT_A],BrickPi.Encoder[PORT_B])
        if ((time.time()-last_update)>update_interval):
            if pid_value < difference:
                #rechts sneller
    ##          left_power -= abs(difference-pid_value)
                right_power += int(abs(difference-pid_value))
                set_left(power)
                set_right(right_power)
                BrickPiUpdateValues()
            elif pid_value > difference:
                #rechts sneller
                left_power += int(abs(difference-pid_value))
    ##          right_power += abs(difference-pid_value)power
                set_left(left_power)
                set_right(power)
                BrickPiUpdateValues()
            else:
                set_left(power)
                set_right(power)
                BrickPiUpdateValues()
        last_update = time.time()
    f.close()

def make_circle_left(power, radius): #radius in cm
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

def turn_straight_left(power, duration):      # Voor rechte hoek buitenste wiel 360 laten draaien (via motorRotateDegree)
    start_time = time.time()
    if (time.time() - start_time) < duration:
        set_left(-power)
        set_right(power)
        BrickPiUpdateValues()
        #motorRotateDegree([power],[360],[PORT_B])


def turn_straight_right(power, duration):
    start_time = time.time()
    if (time.time() - start_time) < duration:
        set_left(-power)
        set_right(power)
        BrickPiUpdateValues()


def set_left(power):
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

def get_functions():
    functions = {'go_straight_distance': go_straight_distance, 'go_straight_pid': go_straight_pid,
                    'make_circle_left': make_circle_left, 'make_circle_right': make_circle_right,
                    'rotate_angle_left': rotate_angle_left, 'rotate_angle_right': rotate_angle_left,
                    'turn_straight_left': turn_straight_left, 'turn_straight_right': turn_straight_right}
    return functions

def get_motor_values():
    return(BrickPi.Encoder[PORT_A]-offset_A, BrickPi.Encoder[PORT_B]-offset_B)

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


(offset_A,offset_B) = calibrate()

if __name__ == '__main__':
    print "i am the main module, running the go straight duration"
    time.sleep(15)
    go_straight_duration(120,100)
##turn_straight_left(200)

##            print 'left',
##            print left_power,
##            print
##            print 'right',
##            print right_power,
##            print left_power
##            print right_power
