import motors 
import inverters
import motorsimulators
import motormath
import motorparams
import commands
import numpy as np
import time
import matplotlib.pyplot as plt
plt.style.use('rose-pine')

start_time = time.time()

####### System Parameters ###################################################################
vbus = 12
dt = 1e-6
fsw = 20000
current_pi_bw = 50

####### System Initialization ###############################################################
cim = motors.PMDC(motorparams.cim)
hbridge = inverters.FullBridgeIdeal(vbus,fsw)
input = commands.Step(5)

####### Controller Design ###################################################################
class currentController:
    def __init__(self, params):
        self.kp, self.ki = motormath.params2igains(params['Ra'], params['La'], current_pi_bw)
        self.error = 0
        self.error_integral = 0
        self.previous_error = 0

    def control(self, vbus, dt):
        ia = cim.states['ia']
        ref = input.get()
        dt = dt
        vbus = vbus

        self.error = ref - ia
        self.error_integral += self.error * dt

        v_p_i = (self.kp * self.error) + (self.ki * self.error_integral)
        duty = v_p_i/vbus

        if duty > 1:
            duty = 1
        elif duty < -1:
            duty = -1

        if duty < 0:
            da = 0
            db = duty
        elif duty > 0:
            da = duty
            db = 0

        return da, db

controller = currentController(motorparams.cim)

####### SIMULATION ######################################################################
system = motorsimulators.ConnectPMDC(cim, hbridge, controller)

system.simulate(dt,0.01)

print("--- %s seconds ---" % (time.time() - start_time))

###### Analysis #########################################################################
cim.analyze('allplots')
#hbridge.analyze('switchplot')
