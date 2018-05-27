import tclab
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.integrate import odeint



# save txt file
def save_txt(t,u1,u2,y1,y2,sp1,sp2):
    data = np.vstack((t,u1,u2,y1,y2,sp1,sp2))  # vertical stack
    data = data.T                 # transpose data
    top = 'Time (sec), Heater 1 (%), Heater 2 (%), ' \
        + 'Temperature 1 (degC), Temperature 2 (degC), ' \
        + 'Set Point 1 (degC), Set Point 2 (degC)'
    np.savetxt('data.txt',data,delimiter=',',header=top,comments='')

def model_balance(x,t,Q):
    T0      = 273.15 + 23   #Kelvin
    Tinf    = 273.15 + 23   #Kelvin
    alpha   = 0.01
    cp      = 500           #Heat capacity (J/Kg*K)
    A       = 1.5e-3        #Area (m^2)
    m       = 0.4e-2        #Mass (Kg)
    U       = 10            #Heat Transfer Coefficient (W/m^2*K)
    eps     = 0.9           #Emissivity
    sig     = 5.6e-8        #Stefan Boltzmann Constant (W/m^2*K^4)

    #Temperature
    T = x[0]

    dTdt = (U*A*(Tinf-T) + eps*sig*A*(Tinf**4 - T**4) + alpha*Q)/(m*cp)
    return dTdt

# FOPDT model
Kp = 0.5      # degC/%
tauP = 120.0  # seconds
thetaP = 15   # seconds (integer)
Tss = 23      # degC (ambient temperature)
Qss = 0       # % heater
K = 273.15    #Celsius to Kelvin

#Definitions
run_time = 9   #Minutes
t_sample = 1    #Sample time (s)
n = int(60*run_time/t_sample)
t = np.zeros(n)

#TCLab
a = tclab.TCLab()
print(a.version)

## Turn on LED
print("Led on")
a.LED(50)

#Temperatures
T1      =   np.ones(n) * a.T1
Tsp1    =   np.ones(n) * 23.0

T2      =   np.ones(n) * a.T2
Tsp2    =   np.ones(n) * 23.0

# Predictions
Tp = np.ones(n) * a.T2
e_eb = np.zeros(n)
Tpl = np.ones(n) * a.T2
e_fopdt = np.zeros(n)

#Steps (0-100%)
Q1 = np.zeros(n)
Q2 = np.zeros(n)

Q2[8:int(n/3)] = 50
Q2[int(n/3):int(2*n/3)] = 100
Q2[int(2*n/3):] = 70

print('Running Main Loop. Ctrl-C to end.')
print('  Time   Q1     Q2    T1     T2')
print('{:6.1f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}'.format(t[0], \
                                                       Q1[0], \
                                                       Q2[0], \
                                                       T1[0], \
                                                       T2[0]))

#Plot
# Create plot
plt.figure(figsize=(10,7))
plt.ion()
plt.show()

# Main Loop
start_time = time.time()
prev_time = start_time
sleep_max = 1
try:
    for i in range(1,n):
        #Sleep
        sleep = sleep_max - (time.time() - prev_time)
        time.sleep(sleep)

        #Record time
        now = time.time()
        dt = now - prev_time
        prev_time = now
        t[i] = now - start_time

        #Read temperatures in Celsius
        T1[i] = a.T1
        T2[i] = a.T2

        #Energy balance with one step
        Tnext = odeint(model_balance, Tp[i-1] + K, [0,dt],args=(Q2[i-1],))
        Tp[i] = Tnext[1] - K
        e_eb[i] = e_eb[i-1] + abs(Tp[i]-T2[i])/n

        #One step FOTD
        z = np.exp(-dt/tauP)
        Tpl[i] = (Tpl[i-1]-Tss) * z \
                 + (Q2[max(0,i-int(thetaP)-1)]-Qss)*(1-z)*Kp \
                 + Tss
        e_fopdt[i] = e_fopdt[i-1] + abs(Tpl[i]-T2[i])/n

        #Update Heaters
        a.Q1(Q1[i])
        a.Q2(Q2[i])

        # Print line of data
        print('{:6.1f} {:6.2f} {:6.2f} {:6.2f} {:6.2f}'.format(t[i], \
                                                               Q1[i], \
                                                               Q2[i], \
                                                               T1[i], \
                                                               T2[i]))

        #Plots
        plt.clf()
        ax=plt.subplot(3,1,1)
        ax.grid()
        plt.plot(t[0:i], T1[0:i], 'ro', label=r'$T_1$ Measured')
        plt.plot(t[0:i], T2[0:i], 'bo', label=r'$T_2$ Measured')
        plt.plot(t[0:i], Tp[0:i], 'g', label=r'$T_2$ Energy balance')
        plt.plot(t[0:i], Tpl[0:i],'k-', label=r'$T_2$ FOTD')
        plt.ylabel('Temperature (degC)')
        plt.legend(loc=2)

        ax=plt.subplot(3,1,2)
        ax.grid()
        plt.plot(t[0:i], e_eb[0:i], 'g', label='Error energy balance')
        plt.plot(t[0:i], e_fopdt[0:i], 'k-', label='Error FOTD')
        plt.ylabel('Cumulative Error')
        plt.legend(loc='best')

        ax=plt.subplot(3,1,3)
        ax.grid()
        plt.plot(t[0:i], Q1[0:i], 'r-', label=r'$Q_1$')
        plt.plot(t[0:i], Q2[0:i], 'b:', label=r'$Q_2$')
        plt.ylabel('Heaters')
        plt.xlabel('Time (s)')
        plt.legend(loc='best')

        plt.draw()
        plt.pause(0.05)

    # Turn off heaters
    a.Q1(0)
    a.Q2(0)
    # Save text file
    save_txt(t[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    # Save figure
    plt.savefig('test_Models.png')

# Allow user to end loop with Ctrl-C
except KeyboardInterrupt:
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Shutting down')
    a.close()
    save_txt(t[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    plt.savefig('test_Models.png')

# Make sure serial connection still closes when there's an error
except:
    # Disconnect from Arduino
    a.Q1(0)
    a.Q2(0)
    print('Error: Shutting down')
    a.close()
    save_txt(t[0:i],Q1[0:i],Q2[0:i],T1[0:i],T2[0:i],Tsp1[0:i],Tsp2[0:i])
    plt.savefig('test_Models.png')
    raise
