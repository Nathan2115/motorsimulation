import motors
import inverters
import motorsimulators
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('rose-pine')

####### Motor Parameters #########################################################
cim_params = {
    'kr': 0.0185,       # Torque/back-EMF constant (N-m/A) or (V-s/rad)
    'Ra': 0.091,        # Armature resistance (ohm)
    'La': 59e-6,        # Armature inductance (H)
    'Jr': 0.000075,     # Motor inertia (kg-m^2)
    'B': 9e-5,          # Motor damping coefficient (N-m-s/rad)
    'Tl': 0,            # Load torque
    'Tf': 0.05          # Dry friction torque
}

####### Controller Design ########################################################
def controller():
    return 0.01, 0

####### System Parameters ########################################################
vbus = 12
dt = 1e-6
fsw = 20000

####### SIMULATION ###############################################################
cim = motors.PMDC(cim_params)
hbridge = inverters.FullBridgeIdeal(vbus,fsw)

system = motorsimulators.ConnectPMDC(cim, hbridge, controller())

system.simulate(dt,0.001)

cim.analyze('currentplot')
#hbridge.analyze('switchplot')
