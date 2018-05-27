import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#return dy/dt
def model(z,t):
    dxdt = 3 * np.exp(-t)
    dydt = 3 - z[1]
    return [dxdt,dydt]

#initial condition
z0 = [0,0]

#time
t = np.linspace(0,10)

#solve
z = odeint(model, z0, t)

x = z[:,0]
y = z[:,1]

#plot results
plt.plot(t,x,'r-', linewidth=2,label='x')
plt.plot(t,y,'b--', linewidth=2,label='y')
plt.xlabel('time')
plt.ylabel('z(t)')
plt.legend()
plt.show()
