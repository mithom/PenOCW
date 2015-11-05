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
    def __init__(self, kp, kd, setpoint, offset_A, offset_B, dt):
        self.kp = kp
        # self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt

        self.offset_A = offset_A
        self.offset_B = offset_B

        self.previous_error = 0
        # self.integral = 0

    def update(self, encoder_A, encoder_B):
        encoder_A = encoder_A  - self.offset_A
        encoder_B = encoder_B  - self.offset_B
        if encoder_B != 0:
	    ratio = encoder_A / float(encoder_B)
	else:
	    ratio = 1
        error = ratio - self.setpoint

        derivative = (error - self.previous_error) / self.dt
        output = 1 - self.kp * error - self.kd * derivative  # + self.ki*self.integral

        self.previous_error = error
        # self.integral += error
        # print "pid output:" + str(output)
        return output
