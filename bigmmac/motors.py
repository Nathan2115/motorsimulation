"""`motors.py` contains motor classes used by the BigMMAC simulation suite. Each motor class contains methods for applying voltage to
lumped parameter physics models as well as for anaylzing performance and plotting state change in time. `PMDC` is the class for permanent magnet
DC machines."""

import matplotlib.pyplot as plt
import pandas
import plotly.express as px
from plotly.offline import plot
import numpy as np

class PMDC:
    """The PMDC class is the parent class for permanent magnet DC electric machines in the 
    Big Brain Motor Modeling, Analysis, and Control (BigMMAC) simulation suite.
    This class contains the defining physics and numerical integration. """
    
    def __init__(self, motorParams):
        """The constructor for the PMDC class takes a list of machine parameters as its argument and initializes instance variables 
        including machine parameters, dynamic states and their derivatives, machine performance (torque, power), and 
        storage lists for plotting"""

        ## Parameters
        self.kr = motorParams['kr']    # Torque/Back EMF constant (N/A or V/rad/s)
        self.Ra = motorParams['Ra']    # Armature resistance (Ohm)
        self.La = motorParams['La']    # Armature inductance (H)
        self.Jr = motorParams['Jr']    # Motor inertia (kg*m^2)
        self.B = motorParams['B']      # Motor damping coefficient (N*s/m)
        self.Tl = motorParams['Tl']    # Load torque (N)
        self.Tf = motorParams['Tf']    # Dry friction torque (N)

        ## States and Derivatives
        self.wr = 0                    # Motor speed (rad/s)
        self.dwr_dt = 0                # Motor acceleration (m/s^2)
        self.ia = 0                    # Armature current (A)
        self.dia_dt = 0                # Armature current derivative (A/s)

        ## Performance
        self.Tau = 0                 # Motor torque (N-m)
        self.Pelec = 0               # Electrical Power (W)
        self.Pmech = 0               # Mechanical Power (W)

        ## Plot storage
        self.time = 0
        self.times = [0]

        self.ias = [0]
        self.wrs = [0]
        self.wrs_rpm = [0]
        
        self.Taus = [0]
        self.Pelecs = [0]
        self.Pmechs = [0]
    
    def physics(self, va, ia, wr):
        """ `physics` is a helper function that stores the physics of the PMDC machine in a state space representation,
        and can be called to compute machine dynamics at any time. This helper function gets used by the `applyVoltage` method
        in numerical integration"""

        ## Governing ODEs
        dia_dt = (1/self.La) * va + (-self.Ra/self.La) * ia + (-self.kr/self.La) * wr
        if ia == 0: 
            dwr_dt = 0
        else:
            dwr_dt = (self.kr/self.Jr) * ia + (-self.B/self.Jr) * wr + (-1/self.Jr) * (self.Tl + self.Tf)

        ## Packaged System
        xdot = dia_dt, dwr_dt
        return xdot

    def applyVoltage(self, va, dt):
        """The `applyVoltage` method is the main simulation within PMDC class. Practical machines are driven by voltage commands 
        and output performance (i.e. torque and power). Similarly, this method takes a voltage at a timestep, integrates (single step RK4) 
        and stores the machine dynamics, and computes and stores machine performance. This method assumes that voltage is constant at every
        simulation timestep"""
        
        ## Runge-Kutta Order 4 integration of physics
        k1_ia, k1_wr = self.physics(va, self.ia, self.wr)
        k2_ia, k2_wr = self.physics(va, self.ia + dt/2*k1_ia, self.wr + dt/2*k1_wr)
        k3_ia, k3_wr = self.physics(va, self.ia + dt/2*k2_ia, self.wr + dt/2*k2_wr)
        k4_ia, k4_wr = self.physics(va, self.ia + dt*k3_ia, self.wr + dt*k3_wr)
        self.ia = self.ia + dt/6*(k1_ia + 2*k2_ia + 2*k3_ia + k4_ia)
        self.wr = self.wr + dt/6*(k1_wr + 2*k2_wr + 2*k3_wr + k4_wr)
        
        ## Calculate performance
        self.Tau = self.kr * self.ia
        self.Pelec = va * self.ia
        self.Pmech = (self.Tau - self.Tf) * self.wr
        self.time += dt

        ## Store data for plotting
        self.times.append(self.time)
        self.ias.append(self.ia)
        self.wrs.append(self.wr)
        self.wrs_rpm.append(self.wr * (1/(2*np.pi))*60)
        self.Taus.append(self.Tau)
        self.Pelecs.append(self.Pelec)
        self.Pmechs.append(self.Pmechs)

    def analyze(self, desiredout):
        """`analyze` is a method that generates plots and print outputs for states and performance variables. It takes
        a single string as its argument. Use `currentplot` for current plot, similarly `speedplot` or `torqueplot`. `pelec`
        or `pmech` print steady-state power."""

        if desiredout == 'currentplot':
            plt.plot(self.times, self.ias)
            plt.title('Armature Current vs. Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Current (A)')
            plt.grid(True)
            plt.show()
            
        elif desiredout == 'currentplotly':
            fig = px.scatter(x=self.times, y=self.ias)
            fig.update_layout(
                title='Armatur Current vs. Time',
                xaxis_title='Time (s)',
                yaxis_title='Current (A)'
            )

            plot(fig, filename='currentplot.html', auto_open=True)

        elif desiredout == 'speedplot':
            plt.plot(self.times, self.wrs_rpm)
            plt.title('Rotor Speed vs. Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Rotor Speed (RPM)')
            plt.grid(True)
            plt.show()
            
        elif desiredout == 'torqueplot':
            plt.plot(self.times, self.Taus)
            plt.title('Torque vs. Time')
            plt.xlabel('Time (s)')
            plt.ylabel('Torque (N-m)')
            plt.grid(True)
            plt.show()
        
        elif desiredout == 'pelec':
            print("\n")
            print("Electrical Power = ", round(self.Pelec,2), "W")
            print("\n")

        elif desiredout == 'pmech':
            print("\n")
            print("Mechanical Power = ", round(self.Pmech,2),"W")
            print("\n")