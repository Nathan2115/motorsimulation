"""`motorsimulators.py` contains the simulation classes used by the BigMMAC simulation suite. The `ConnectXYZ` classes provides an intuitive way of
integrating motor and inverter models with controller prototypes and has a method for running a discrete time simulation.
DC machines."""

import numpy as np

class ConnectPMDC:
    """ `ConnectPMDC` creates a connected system of PMDC motor, full bridge inverter, and controller. `Connect` provides the `simulate()` method for system
    simulation, and also provides the `idealSwitchGen` helper function to generate PWM signals."""
    def __init__(self, motor, inverter, control):
        self.inverter = inverter
        self.motor = motor
        self.control = control

    def idealSwitchGen(self, timer, duty, ndt, dt, fsw):
        """The `idealSwitchGen() helper function is used to simulate PWM switching in the `FullBridgeIdeal` type inverter. The `timer` is analagous to a hardware timer that would be used
        on a microcontroller implementation. `duty` sets the duty cycle for the PWM. `ndt` is the number of `dt` elements that can fit within a PWM period, given switching frequency `fsw`.
        This helper outputs switch state (high or low) for a single switch for every `dt` in simulation, and modifies `dt` at the switch time from high to low to ensure duty cycles 
        are accurate."""

        switchstate = 0

        ## Determine between which timer counts the switch from high to low occurs for a given duty cycle
        pwm_switch_case = np.trunc(duty * ndt) 

        ## Determine if PWM should be be switched from high to low, output correspondong switch state
        #  Start high, remain high as long as switch case hasn't been reached
        if timer < pwm_switch_case and duty != 0:
            dt_out = dt
            switchstate = 1
            timer += 1

        #  Once switch case has been reached, calculate the dt offset required to accurately hit duty cycle
        elif timer == pwm_switch_case and duty != 0:
            dt_mod = (duty / fsw) - (timer * dt)
            dt_out = dt_mod
            switchstate = 1
            timer += 1

        #  Calculate the dt offset complimentary to the switchcase dt offset to ensure that the switch happens within exactly 2 dt cycles and duty cycle is maintained accurately 
        elif timer == (pwm_switch_case + 1) and duty != 0:
            dt_mod = (duty / fsw) - ((timer - 1) * dt)
            dt_out = (2 * dt) - dt_mod
            switchstate = 0
            timer += 1
        
        # After switching to low, return to original dt and maintain low switch state
        elif timer > pwm_switch_case and duty != 0:
            dt_out = dt
            switchstate = 0
            timer += 1

        # If duty cycle is zero, keep switch state low
        else:
            dt_out = dt
            switchstate = 0
            timer += 1
        return  timer, dt_out, switchstate
        

    def simulate(self, dt, t_end):
        """'simulate' applies control commands from the controller to the drive, applies drive voltage to motor, then solves the motor physics and 
         updates the controller at every timestep 'dt' for simulation duration t = 0 to t = t_end."""
        
        self.simstep = 0
        self.dt = dt
        self.t_end = t_end
        self.sim_end = self.t_end/self.dt

        ## Simple inverter is useful for steady state dynamics on longer simulation time scales
        if self.inverter.type() == 'FullBridgeSimple':
            while self.simstep < self.sim_end:

                # Compute control output
                self.da, self.db = self.control #eventually make self.control(motorstates)

                # Simulate inverter output
                self.vcmd = self.inverter.on(self.da, self.db) 

                # Appy inverter output to motor and solve physics
                self.motor.applyVoltage(self.vcmd, self.dt)

                self.simstep += 1

        ## Ideal inverter neglects switching losses but captures PWM transient waveforms, so is better for transient simulations
        elif self.inverter.type() == 'FullBridgeIdeal':
            self.timer = 0
            self.ndt = np.trunc((1/self.inverter.fsw()) / self.dt)
            while self.simstep < self.sim_end:

                # Compute control output
                self.da, self.db = self.control #eventually make self.control(motorstates)

                # If current simulation step is within a given PWM period, compute switch states for all inverter switches
                
                if self.timer < self.ndt:
                    if self.da > self.db: # Positive Voltage/Rotation
                        self.timer, self.dt_out, self.ahi = self.idealSwitchGen(self.timer, self.da, self.ndt, self.dt, self.inverter.fsw())
                        self.alo = 0
                        self.bhi = 0
                        self.blo = 1
                        
                    elif self.da < self.db: # Negative voltage/rotation
                        self.timer, self.dt_out, self.bhi = self.idealSwitchGen(self.timer, self.db, self.ndt, self.dt, self.inverter.fsw())
                        self.blo = 0
                        self.ahi = 0
                        self.alo = 1
                    else:
                        self.ahi = 0
                        self.bhi = 0
                        self.alo = 0
                        self.blo = 0
                        self.dt_out = self.dt
                
                # If current simulation step is NOT within a given PWM period, start a new PWM period and compute switch states for all inverter switches
                else:
                    self.timer = 0
                    if self.da > self.db: # Positive Voltage/Rotation
                        self.timer, self.dt_out, self.ahi = self.idealSwitchGen(self.timer, self.da, self.ndt, self.dt, self.inverter.fsw())
                        self.alo = 0
                        self.bhi = 0
                        self.blo = 1
                        
                    elif self.da < self.db: # Negative voltage/rotation
                        self.timer, self.dt_out, self.bhi = self.idealSwitchGen(self.timer, self.db, self.ndt, self.dt, self.inverter.fsw())
                        self.blo = 0
                        self.ahi = 0
                        self.alo = 1
                    else:
                        self.ahi = 0
                        self.bhi = 0
                        self.alo = 0
                        self.blo = 0
                        self.dt_out = self.dt

                # Simulate inverter output given inverter switch states
                self.vcmd = self.inverter.on(self.ahi, self.alo, self.bhi, self.blo, self.dt_out)

                # Appy inverter output to motor and solve physics
                self.motor.applyVoltage(self.vcmd, self.dt_out)

                self.simstep += 1
        else:
            print("\n")
            print("Unrecognized Inverter Type in Simulation")
            print("\n")
