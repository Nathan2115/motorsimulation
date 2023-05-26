"""`inverters.py` contains inverter classes used by the BigMMAC simulation suite. Each inverter class contains the `on` method for turning on to
convert switch commands or duty cycles commands into voltage outputs."""

import numpy as np
import matplotlib.pyplot as plt

class FullBridgeIdeal:
    """`FullBridgeIdeal` includes switching dynamics for accurate transient analysis, and scales switch commands by bus voltage. This class
    also provides an `analyze` method to view PWM plots and inverter outputs."""
    def __init__(self, vbus, fsw):
        
        self.vbus = vbus
        self.vout = 0
        self.fswitch = fsw
        self.time = 0

        self.ahis = [0]
        self.alos = [0]
        self.bhis = [0]
        self.blos = [0]
        self.times = [0]
        self.vouts = [0]
        
    def type(self):
        """The `type` method returns the type inverter that this class represents."""
        return 'FullBridgeIdeal'
    
    def fsw(self):
        """The `fsw` method in `FullBridgeIdeal` returns the switching frequency of the inverter."""
        return self.fswitch
    
    def on(self, ahi, alo, bhi, blo, dt): 
        """The `on` method scales switch commands by bus voltage."""
        self.ahi = ahi
        self.alo = alo
        self.bhi = bhi
        self.blo = blo
        self.time += dt

        self.ahis.append(ahi)
        self.alos.append(alo)
        self.bhis.append(bhi)
        self.blos.append(blo)
        self.times.append(self.time)
        if self.ahi > self.bhi:
            self.vout = self.ahi * self.vbus
        elif self.ahi < self.bhi:
            self.vout = self.bhi * self.vbus * -1
        else:
            self.vout = self.ahi + self.bhi
        self.vouts.append(self.vout)
        return self.vout
        
    def analyze(self, desiredout):
        """Ue argument 'switchplot' to look at the PWM signals on each inverter switch or 'voutplot' to look at the inverter output voltage plot."""
        if desiredout == 'switchplot':
            
            fig, axs = plt.subplots(4)

            axs[0].grid(True)
            axs[1].grid(True)
            axs[2].grid(True)
            axs[3].grid(True)

            axs[0].plot(self.times, self.ahis)
            axs[0].set_title('Phase A | High Side Switch')

            axs[1].plot(self.times, self.alos)
            axs[1].set_title('Phase A | Low Side Switch')

            axs[2].plot(self.times, self.bhis)
            axs[2].set_title('Phase B | High Side Switch')

            axs[3].plot(self.times, self.blos)
            axs[3].set_title('Phase B | Low Side Switch')

            axs[0].set_ylim([0,1])
            axs[1].set_ylim([0,1])
            axs[2].set_ylim([0,1])
            axs[3].set_ylim([0,1])

            axs[0].set_ylabel('Switch State')
            axs[1].set_ylabel('Switch State')
            axs[2].set_ylabel('Switch State')
            axs[3].set_ylabel('Switch State')

            axs[3].set_xlabel('Time (s)')

            plt.subplots_adjust(hspace=2)
            plt.show()
        
        if desiredout == 'voutplot':
            plt.plot(self.times, self.vouts)
            plt.title('Inverter Output Voltage')
            plt.xlabel('Time (s)')
            plt.ylabel('Voltage')
            plt.grid(True)
            plt.show()

        
    
class FullBridgeSimple:
    """`FullBridgeSimple` abstracts away switching dynamics for faster simulation times, outputting average value voltage."""
    def __init__(self, vbus):
        self.vbus = vbus
        self.vout = 0
        self.vbus = vbus

    def type(self):
        """The `type` method returns the type inverter that this class represents."""
        return 'FullBridgeSimple'
    
    def on(self, da, db):
        """ The `on` method in `FullBridgeSimple` computes average value voltage from duty cycle and bus voltage arguments."""
        self.da = da
        self.db = db
        if da > db:
            self.vout = da*self.vbus
        elif da < db:
            self.vout = -1*db*self.vbus
        else:
            self.vout = 0
        return self.vout