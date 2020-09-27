class PIDcontroller:
    def __init__(self,kp,ki,kd):
        self.timestep = 2
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.i_error = 0
        self.p_error = 0
        self.d_error = 0
        self.last_error = 0

    def update(self, state, setpoint):
        error = setpoint - state
        self.p_error = error
        self.i_error += (error * self.timestep)
        self.d_error = (self.last_error - self.p_error) / self.timestep

        return (self.p_error * self.kp) + (self.d_error * self.kd) + (self.i_error * self.ki)


