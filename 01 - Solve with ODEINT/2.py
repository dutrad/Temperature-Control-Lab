import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#return dy/dt
def model(y,t):
    if(t<10):
        u = 0.0
    else:
        u = 2.0

    dydt = (-y + u)/5
    return dydt

#initial condition
y0 = 1;

#time
t = np.linspace(0,40)

#solve
y = odeint(model, y0, t)

#plot results
plt.plot(t,y,'r-', linewidth=2)
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()
