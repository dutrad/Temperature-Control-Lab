import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#return dy/dt
def model(z,t,u):
    dxdt = (-z[0] + u)/2.0
    dydt = (-z[1] + z[0])/5.0
    return [dxdt,dydt]

#initial condition
z0 = [0,0]

#time
N = 150
t = np.linspace(0,15,N)
u = np.zeros(N)
u[51:] = 2.0

x = np.zeros(N)
y = np.zeros(N)

#solve
for i in range(1,N):
    tspan = [t[i-1], t[i]]
    z = odeint(model, z0, t, args=(u[i],))
    z0 = z[1]
    x[i] = z0[0]
    y[i] = z0[1]

#plot results
plt.plot(t,u,'g:', linewidth=2,label='u')
plt.plot(t,x,'r-', linewidth=2,label='x')
plt.plot(t,y,'b--', linewidth=2,label='y')
plt.xlabel('time')
plt.ylabel('z(t)')
plt.legend()
plt.show()
