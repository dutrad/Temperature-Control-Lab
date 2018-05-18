import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#return dy/dt
def model(y,t,k):
    dydt = -k * y
    return dydt

#initial condition
y0 = 5;

#time
t = np.linspace(0,20,50)

#solve
y1 = odeint(model, y0, t, args=(0.1,))
y2 = odeint(model, y0, t, args=(0.2,))
y3 = odeint(model, y0, t, args=(0.5,))

#plot results
plt.plot(t,y1,'r-', linewidth=2, label='k=0.1')
plt.plot(t,y2,'b--', linewidth=2, label='k=0.2')
plt.plot(t,y3,'g:', linewidth=2, label='k=0.5')
plt.xlabel('time')
plt.ylabel('y(t)')
plt.legend()
plt.show()
