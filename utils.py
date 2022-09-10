import numpy as np
import datetime
import matplotlib.pyplot as plt


###########################################################################
def get_times(data):
    time = data[:, :5]
    time1 = time2 = np.zeros(time.shape[0])
    delta= np.zeros(time.shape[0]-1)
    times = np.zeros(time.shape[0])
    times[0] = 0
    for i in range(time.shape[0]-1):
        time1 = datetime.datetime(
            year = time[i, 0],
            month = time[i, 1], 
            day = time[i, 2], 
            hour = time[i, 3], 
            minute = time[i, 4])
        time2 = datetime.datetime(
            year = time[i+1, 0],
            month = time[i+1, 1], 
            day = time[i+1, 2], 
            hour = time[i+1, 3], 
            minute = time[i+1, 4])
        delta = time2 - time1
        times[i+1] = times[i] + delta.total_seconds()/60
        #times[i+1] = times[i] + delta.days
    times = times/(24*60)    #in days
    return np.array(times)


############################################################################
def get_oppositions(data):
    opps = data[:, 5:9]
    opp_longitudes = opps[:, 0]*30 + opps[:, 1] + opps[:, 2]/60 + opps[:, 3]/3600      #in degrees

    return np.array(opp_longitudes)


############################################################################
def equant_pos(z, s, times):
    epos = z + s * times
    prim_range = np.floor(epos/360)
    epos = epos - prim_range*360

    return np.array(epos)


#############################################################################
def plot_longitudes(r, s, c, e1, e2, z, times, oppositions):

    longitudes = equant_pos(z, s, times)
   
    plt.figure(dpi=120)
    plt.xlim(-17, 17)
    plt.ylim(-17, 17)
    plt.gca().set_aspect('equal', adjustable='box')

    c = np.radians(c)
    theta = np.linspace( 0 , 2 * np.pi , 150 )
    x = r * np.cos(theta) + np.cos(c)
    y = r * np.sin(theta) + np.sin(c)
    plt.plot(x,y, linewidth=0.7) 


    x1 = np.arange(e1*np.cos(e2*np.pi/180), 15, 0.1)
    x2 = np.arange(-15, e1*np.cos(e2*np.pi/180) + 0.1, 0.1)

    for i in range(len(longitudes)):
        if longitudes[i] < 90 or longitudes[i] > 270:
            #y = mx + rsin(theta) - mrcos(theta)  formula
            y = np.tan(longitudes[i]*np.pi/180)*x1 + e1*np.sin(e2*np.pi/180) - np.tan(longitudes[i]*np.pi/180)*e1*np.cos(e2*np.pi/180)
            plt.plot(x1,y, '--', linewidth=0.7)
        else:
            y = np.tan(longitudes[i]*np.pi/180)*x2 + e1*np.sin(e2*np.pi/180) - np.tan(longitudes[i]*np.pi/180)*e1*np.cos(e2*np.pi/180)
            plt.plot(x2,y, '--', linewidth=0.7) 

            
    x1 = np.arange(0, 15, 0.1)
    x2 = np.arange(-15, 0.1, 0.1)

    for i in range(len(oppositions)):
        if oppositions[i] < 90 or oppositions[i] > 270:
            y = np.tan(oppositions[i]*np.pi/180)*x1
            plt.plot(x1, y, linewidth=0.7)
        else:
            y = np.tan(oppositions[i]*np.pi/180)*x2
            plt.plot(x2,y,linewidth=0.7)

    plt.plot(np.cos(c), np.sin(c), 'k', marker = '.', markersize=1)
    plt.plot(0, 0,'k', marker = '.', markersize=1)
    plt.plot(e1*np.cos(np.radians(e2)), e1*np.sin(np.radians(e2)), 'k',marker = '.', markersize=1)
    plt.grid()
       
    x = np.linspace(5, 15, 20)
    y1 = np.linspace(-25, -25, 20)
    y2 = np.linspace(-20, -20, 20)
    plt.plot(x, y1, 'k--', linewidth=0.5, label = 'Equant Longitudes')
    plt.plot(x, y2, 'k', linewidth=0.5, label = 'Oppositions Longitudes')
    plt.legend(loc ="lower right", prop={'size': 5})
    plt.show()
      