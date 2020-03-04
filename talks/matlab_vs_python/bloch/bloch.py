#%% Imports
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt

#%% Define bloch and B_eff functions
def bloch_ode(t,M,T1,T2):
    B = B_eff(t)
    return np.array([M[1]*B[2] - M[2]*B[1] - M[0]/T2,
                     M[2]*B[0] - M[0]*B[2] - M[1]/T2,
                     M[0]*B[1] - M[1]*B[0] - (M[2]-1)/T1])

def B_eff(t):
    if t < 0.25:
        return np.array([0, 0, 0])
    elif t < 1.25:
        return np.array([1.8*np.sinc(t-0.75), 0, 0])
    elif t < 1.50:
        return np.array([0, 0, 0])
    elif t < 3.00:
        return np.array([0, 0, 2*np.pi])
    else:
        return np.array([0, 0, 0])

#%% Integrate ODE
t = np.array([0])
M = np.array([[0, 0, 1]])
dt= 0.005
r = ode(bloch_ode)\
   .set_integrator('dopri5')\
   .set_initial_value(M[0],t[0])\
   .set_f_params(1500, 50)
while r.successful() and r.t < 5:
    t = np.append(t,r.t+dt)
    M = np.append(M, np.array([r.integrate(t[-1])]),axis=0)

#%% Plot Results
plt.plot(t,M[:,0])
plt.plot(t,M[:,1])
plt.plot(t,M[:,2])