import time
import random

isUpdated = True


def go_straight_distance(*args, **kwargs):
    time.sleep(1)


def go_straight_pid(*args, **kwargs):
    time.sleep(0.1)
    pass


def make_circle_left(*args, **kwargs):
    pass


def make_circle_right(*args, **kwargs):
    pass


def rotate_angle_left(*args, **kwargs):
    pass


def rotate_angle_right(*args, **kwargs):
    pass


def turn_straight_left(*args, **kwargs):
    time.sleep(0.1)
    pass


def turn_straight_right(*args, **kwargs):
    time.sleep(0.1)
    pass

def set_motors(left, right,*args, **kwargs):
    pass

def go_straight_manual(*Args,**kwargs):
    pass

def go_straight_duration(*Args,**kwargs):
    pass

def rotate_left_angle(*Args,**kwargs):
    pass

def rotate_right_angle(*Args,**kwargs):
    pass

def rotate_left_duration(*Args,**kwargs):
    pass

def sleep(*Args,**kwargs):
    pass

def rotate_right_duration(*Args,**kwargs):
    pass




def get_functions():
    functions = {'go_straight_distance': go_straight_distance, 'go_straight_duration1': go_straight_duration,
                 'go_straight_manual': go_straight_manual, 'make_circle_left': make_circle_left,
                 'make_circle_right': make_circle_right, 'rotate_left_angle': rotate_left_angle,
                 'rotate_right_angle': rotate_right_angle, 'rotate_left_duration': rotate_left_duration,
                 'rotate_right_duration': rotate_right_duration, 'sleep': sleep,
                 'set_powers': set_motors}
    return functions


def get_power_values():
    return random.randint(0,255), random.randint(0,255)