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
        self.integral_limit = 0.01

    def update(self, encoder_A, encoder_B):
        encoder_A = encoder_A - self.offset_A
        encoder_B = encoder_B - self.offset_B
	
	smallest = min(encoder_A, encoder_B)
	encoder_A += 5000 - smallest
	encoder_B += 5000 - smallest
	
	print 'Encoder A: ', encoder_A, ' , Encoder B: ', encoder_B

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

class PID2:

    def __init__(self, kp, kd, ki, offset_A, offset_B, end_offset_A, end_offset_B, max_power=255):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.end_A = end_offset_A - offset_A
        self.end_B = end_offset_B - offset_B
        self.max_power = max_power

        self.end_difference = self.end_A - self.end_B
        self.difference_per_value_A = 1.0*self.end_difference/self.end_A

        self.offset_A = offset_A
        self.offset_B = offset_B

        self.previous_error = 0
        self.integral = 0
        self.passed_time = 0

    def update(self, encoder_A, encoder_B, dt):
        self.passed_time += dt
        value_A = encoder_A - self.offset_A
        value_B = encoder_B - self.offset_B

        current_difference = value_A - value_B
        error = current_difference - self.difference_per_value_A * value_A

        derivative = (error - self.previous_error) / dt
        self.integral += error * dt

        power_compensation = (self.max_power / 255.0) * \
                             (self.kp * error + self.kd * derivative + self.ki * self.integral)
        self.previous_error = error
        return power_compensation  # mogelijks is dit het negatieve van dit
        pass
