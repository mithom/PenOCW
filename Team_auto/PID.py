__author__ = 'Gilles'


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
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt

        self.offset_A = offset_A
        self.offset_B = offset_B

        self.previous_error = 0
        self.integral = 0
        self.integral_limit = 2

    def update(self, encoder_A, encoder_B):
        encoder_A = encoder_A - self.offset_A
        encoder_B = encoder_B - self.offset_B
        if encoder_B != 0:
            ratio = encoder_A / float(encoder_B)
        else:
            ratio = self.setpoint

        error = self.setpoint - ratio

        encoder_A = encoder_A - self.offset_A
        encoder_B = encoder_B - self.offset_B

        error = ratio - self.setpoint

        derivative = (error - self.previous_error) / self.dt

        self.integral += error * self.dt
        # if self.integral > self.integral_limit:
        #   self.integral = self.integral_limit
        #   print '///////////// MAX INTEGRAL'
        # elif self.integral < -self.integral_limit:
        #   self.integral = -self.integral_limit
        #   print '///////////// MAX INTEGRAL'

        # if ratio > 1.5:
        #   self.integral = 0

        output = self.setpoint - self.kp * error - self.kd * derivative - self.ki * self.integral

        self.previous_error = error

        return output

    def set_proportional(self, kp):
        self.kp = kp

    def set_derivative(self, kd):
        self.kd = kd

    def get_derivative(self):
        return self.kd

    def set_integral(self, ki):
        self.ki = ki
