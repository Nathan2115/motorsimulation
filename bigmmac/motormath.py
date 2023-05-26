
import numpy as np

def ab2dq(a, b):
    """The traditional Clarke: (a,b,c) --> (d,q,0), this Modified Clarke (a,b) --> (d,q) works for ungrounded wye and delta 3-phase configs"""
    d = (2/3) * a - (1/3) * b - (1/3) * (-a - b)
    q = (np.sqrt(3)/3) * (b - (-a - b))
    return np.array([d, q])

def rot2elec(rotor, n_p):
    """ Transform from physical rotor angle/speed to electrical angle/speed, returns value in Radians or Rad/s. `n_p` is number of motor poles, 
    `rotor` should be rotor angle in Degrees rotor speed in Degrees/s"""
    elec = (n_p/2) * rotor
    elec = np.radians(elec)
    return(elec)

def dq2syn(d, q, theta_re):
    """Park transform: Stationary (d,q) --> synchronous (dsyn,qsyn). `theta_re` needs ot be radians"""
    dsyn = np.cos(theta_re) * d + np.sin(theta_re) * q
    qsyn = -1* np.sin(theta_re) * d + np.cos(theta_re) * q
    return np.array([dsyn, qsyn])

def syn2dq(dsyn, qsyn, theta_re):
    """Inverse Park transform: Synchronous (dsyn,qsyn) --> Stationary (d,q), `theta_re` needs ot be radians"""
    d = np.cos(theta_re) * dsyn - np.sin(theta_re) * qsyn
    q = np.sin(theta_re) * dsyn + np.cos(theta_re) * qsyn
    return np.array([d, q])

def rpm2rads(rpm):
    """RPM to rad/s"""
    rads = rpm * (1/60) * 2 * np.pi
    return rads

def rads2rpm(rads):
    """Rad/s to RPM"""
    rpm = rads* (1/(2 * np.pi)) * 60
    return rpm

def hz2rads(f):
    """Hz to rad/s"""
    return f*2*np.pi

def rads2hz(f):
    """Rad/s to Hz"""
    return f/(2*np.pi)