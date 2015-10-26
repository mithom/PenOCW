__author__ = 'Gilles'

#### PSEUDOCODE ####

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

#### PSEUDOCODE ####

class PID:
    def __init__(self,kp,ki,kd,setpoint,offset_A,offset_B):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.offset_A = offset_A
        self.offset_B = offset_B

        self.previous_error = 0
        self.integral = 0

    def update(self,encoder_A,encoder_B):
        difference = (encoder_A - self.offset_A) - (encoder_B - self.offset_B)
        error = self.setpoint + difference

        derivative = (error-self.previous_error)
        output = self.kp*error + self.ki*self.integral + self.kd*derivative

        self.previous_error = error
        self.integral += error

        return output
