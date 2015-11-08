__author__ = 'Gilles'

import time


# ---- PSEUDOCODE ----

# previous_error = 0
# integral = 0
# start:
#   error = setpoint - measured_value
#   integral = integral + error*dt
#   derivative = (error - previous_error)/dt
#   output = Kp*error + Ki*integral + Kd*derivative
#   previous_error = error
#   wait(dt)
#   goto start

# ---- PSEUDOCODE ----

class PID:
    def __init__(self, kp, kd, ki, setpoint, offset_A, offset_B, dt):
        self.kp = kp
        self.kp_backup = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt

        self.offset_A = offset_A
        self.offset_B = offset_B

        self.previous_error = 0
        self.integral = 0
        self.integral_limit = 0.001

    def update(self, encoder_A, encoder_B):
        encoder_A = encoder_A - self.offset_A
        encoder_B = encoder_B - self.offset_B
        ratio = encoder_A / float(encoder_B)

        error = ratio - self.setpoint

        derivative = (error - self.previous_error) / self.dt

        self.integral += error * self.dt

        if ratio > (self.setpoint + 0.000001) and self.integral < 0:
            self.integral = self.integral * 0.9  #  0.94 # 0.6 # 0.5
        elif ratio < (self.setpoint - 0.000001) and self.integral > 0:
            self.integral = self.integral * 0.9 # 0.5

        if self.integral > self.integral_limit:
            self.integral = self.integral_limit
        elif self.integral < -self.integral_limit:
            self.integral = -self.integral_limit

        output = self.setpoint - self.kp * error - self.kd * derivative - self.ki * self.integral

        self.previous_error = error

        self.kp = self.kp_backup

        print 'Ratio: ', ratio, ', PID: ', output
        return output

    def set_proportional(self, kp):
        self.kp = kp

    def set_derivative(self, kd):
        self.kd = kd

    def get_derivative(self):
        return self.kd

    def set_integral(self, ki):
        self.ki = ki
