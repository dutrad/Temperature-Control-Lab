import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def hiv(x,t,k1,k2,k3,k4,k5,k6):
    H = x[0]
    I = x[1]
    V = x[2]

    dH = k1 - k2*H - k3*H*V
    dI = k3*H*V - k4*I
    dV = -k3*H*V - k5*V + k6*I

    return [dH,dI,dV]

#Initial condition
H0 = 1e6
I0 = 0.0
V0 = 100.0

#Constants
k1 = 1e5
k2 = 0.1
k3 = 2e-7
k4 = 0.5
k5 = 100
k6 = 100.0

#solve
t = np.linspace(0,25,1000)
z = odeint(hiv, [H0,I0,V0], t, args = (k1,k2,k3,k4,k5,k6,))

h = z[:,0]
i = z[:,1]
v = z[:,2]

#plot results
plt.semilogy(t,h,'r-', linewidth=2,label='Healthy Cells')
plt.semilogy(t,i,'b--', linewidth=2,label='Infected Cells')
plt.semilogy(t,v,'g:', linewidth=2,label='Virus')
plt.xlabel('time')
plt.ylabel('#')
plt.legend()
plt.show()

#Multiple values of k5
N = 50
k5 = np.linspace(1,N,N)

H = np.zeros(N)
I = np.zeros(N)
V = np.zeros(N)

for i in range(0,len(k5)):
    z = odeint(hiv, [H0,I0,V0], t, args = (k1,k2,k3,k4,k5[i],k6,))
    H[i] = z[-1,0]
    I[i] = z[-1,1]
    V[i] = z[-1,2]

plt.subplot(3,1,1)
plt.semilogy(k5,H,'r-', linewidth=2)
plt.xlabel('k5')
plt.ylabel('Final Value')
plt.title('Healthy Cells')

plt.subplot(3,1,2)
plt.semilogy(k5,I,'b-', linewidth=2)
plt.xlabel('k5')
plt.ylabel('Final Value')
plt.title('Infected Cells')

plt.subplot(3,1,3)
plt.semilogy(k5,V,'g-', linewidth=2)
plt.xlabel('k5')
plt.ylabel('Final Value')
plt.title('Virus')
plt.show()
