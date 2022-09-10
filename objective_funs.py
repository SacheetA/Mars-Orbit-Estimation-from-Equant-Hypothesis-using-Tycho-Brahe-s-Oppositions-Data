import numpy as np
from utils import equant_pos
from scipy.optimize import minimize

############################################################################
def MarsEquantModel(c,r,e1,e2,z,s,times,oppositions):
    z = equant_pos(z, s, times)
    c = np.radians(c)
    e2 = np.radians(e2)
    z = np.radians(z)
    
    m = np.tan(z)
    A = 1 +  (m ** 2)
    B = -2 * (np.cos(c) + m * np.sin(c) + m * e1 * (m*np.cos(e2) - np.sin(e2)))
    C = (m*e1*np.cos(e2) - e1*np.sin(e2) + np.sin(c)) ** 2 + np.cos(c) ** 2 - r ** 2
    x1 = (-B + np.sqrt(B**2 - 4*A*C)) / (2*A)
    x2 = (-B - np.sqrt(B**2 - 4*A*C)) / (2*A)
    y1 = m * (x1 - e1 * np.cos(e2)) + e1*np.sin(e2)
    y2 = m * (x2 - e1 * np.cos(e2)) + e1*np.sin(e2)
    theta1 = np.arctan2(y1, x1)
    idx = (theta1) < 0
    theta1[idx] = theta1[idx] + 2*np.pi
    theta2 = np.arctan2(y2, x2)
    idx = (theta2) < 0
    theta2[idx] = theta2[idx] + 2*np.pi
    theta = np.zeros(len(z))

    
    for i in range(len(z)):
        if abs(theta1[i] - z[i]) < abs(theta2[i] - z[i]):
            theta[i] = theta1[i]
        else:
            theta[i] = theta2[i]
    errors = abs(np.degrees(theta) - oppositions)
    maxError = np.max(errors)

    return errors, maxError


#############################################################################  
def objective(params, r, s, times, oppositions):
     #params = [c,e1,e2,z]

    _, maxError = MarsEquantModel(params[0],r,params[1], params[2], params[3], s, times, oppositions)
    return maxError


#############################################################################  
def bestOrbitInnerParams(r,s,times,oppositions):
    params0 = [150, 1.2, 170, 60]
    bds = [(0,360), (1, 0.5*r), (0,360), (0,360)]
    result = minimize(objective, params0 ,args = (r, s, times, oppositions), method = 'Nelder-Mead', bounds = bds)
    c = result.x[0]
    e1 = result.x[1]
    e2 = result.x[2]
    z = result.x[3]
    maxError = result.fun
    errors, _ = MarsEquantModel(c,r,e1,e2,z,s,times,oppositions)
    
    return c,e1,e2,z,errors,maxError


#############################################################################  
def  bestR(s,times,oppositions):
    errors = []
    maxError = []
    radius = []
    c = []
    e1 = []
    e2 = []
    z = []

    for r in np.linspace(8,10,20):
        c_out,e1_out,e2_out,z_out,e,mE = bestOrbitInnerParams(r,s,times,oppositions)
        errors.append(e)
        maxError.append(mE)
        c.append(c_out)
        e1.append(e1_out)
        e2.append(e2_out)
        z.append(z_out)
        radius.append(r)

    #index of minimum value of max error
    idx = np.argmin(maxError)       

    #minimum values at the error
    min_maxerr = np.min(maxError)
    min_r = radius[idx]
    min_errors = errors[idx]
    min_c = c[idx]
    min_e1 = e1[idx]
    min_e2 = e2[idx]
    min_z = z[idx]

    return min_r, min_c, min_e1, min_e2, min_z, min_errors, min_maxerr


#############################################################################  
def bestS(r,times,oppositions):
    errors = []
    maxError = []
    angular_vel = []

    for s in np.linspace(0.5235,0.5245,120):
        _,_,_,_,e,mE = bestOrbitInnerParams(r,s,times,oppositions)
        errors.append(e)
        maxError.append(mE)
        angular_vel.append(s)

    idx = np.argmin(maxError)
    min_maxerr = np.min(maxError)
    min_s = angular_vel[idx]
    min_errors = errors[idx]

    return min_s, min_errors, min_maxerr


#############################################################################  
def bestMarsOrbitParams(times,oppositions):
    errors = []
    maxError = []
    r = []
    ang_vel = []
    c = []
    e1 = []
    e2 = []
    z = []
    i = 0
    print('\n\nIterations:')
    for s in np.linspace(0.5235,0.5245,120):
        r_out, c_out, e1_out, e2_out, z_out, errors_out, maxError_out = bestR(s,times,oppositions)
        r.append(r_out)
        c.append(c_out)
        e1.append(e1_out)
        e2.append(e2_out)
        z.append(z_out)
        errors.append(errors_out)
        maxError.append(maxError_out)
        ang_vel.append(s)
        i+= 1
        if i%10 == 0:
            print(i, 'iterations completed out of 120')

    print('\n\n')        

    idx = np.argmin(maxError)
    r_bestfit = r[idx]
    s_bestfit = ang_vel[idx]
    c_bestfit = c[idx]
    e1_bestfit = e1[idx]
    e2_bestfit = e2[idx]
    z_bestfit = z[idx]
    errors_bestfit = errors[idx]
    maxError_bestfit = maxError[idx]

    return r_bestfit, s_bestfit, c_bestfit, e1_bestfit, e2_bestfit, z_bestfit, errors_bestfit, maxError_bestfit 

