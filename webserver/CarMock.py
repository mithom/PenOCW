def go_straight_distance(*args, **kwargs):
    pass

def go_straight_pid(*args, **kwargs):
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
    pass

def turn_straight_right(*args, **kwargs):
    pass


def get_functions():
    functions = {'go_straight_distance': go_straight_distance, 'go_straight_pid': go_straight_pid,
                    'make_circle_left': make_circle_left, 'make_circle_right': make_circle_right,
                    'rotate_angle_left': rotate_angle_left, 'rotate_angle_right': rotate_angle_left,
                    'turn_straight_left': turn_straight_left, 'turn_straight_right': turn_straight_right}
    return functions
