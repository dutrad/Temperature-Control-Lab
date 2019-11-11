import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#return dy/dt
def model(y,t,a,b):
    dydt = a*y + b
    return dydt

#initial condition
y0 = 0;

#time
t = np.linspace(0,5)

#solve
y = odeint(model, y0, t, args=(-1,1,))

#plot results
plt.plot(t,y,'r-', linewidth=2)
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()
