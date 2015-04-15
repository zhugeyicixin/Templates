import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt
import sys

# if set __printError__ = True, then the root mean square RMS of devidation list(fit_y)-list(y) would be printed
__printError__ = False

# the max_order in fourier() expand
MAX_ORDER = 15
COS_MAX_ORDER = 18

# a simple fourier case in 6 order
def func_fourier6(x, a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6):
    return a0+a1*np.cos(x)+b1*np.sin(x)+a2*np.cos(2*(x))+b2*np.sin(2*(x))+a3*np.cos(3*(x))+b3*np.sin(3*(x))+a4*np.cos(4*(x))+b4*np.sin(4*(x))+a5*np.cos(5*(x))+b5*np.sin(5*(x))+a6*np.cos(6*(x))+b6*np.sin(6*(x))

# a simple cos fourier case in 6 order
def func_cosFourier6(x, c, a0, a1, a2, a3, a4, a5, a6):
    # return a0+a1*np.cos(x+c)+a2*np.cos(2*(x+c))+a3*np.cos(3*(x+c))+a4*np.cos(4*(x+c))+a5*np.cos(5*(x+c))+a6*np.cos(6*(x+c))
    return a0+a1*np.cos(x+c)+a2*np.cos(2*(x+c))+a3*np.cos(3*(x+c))+a4*np.cos(4*(x+c))+a5*np.cos(5*(x+c))+a6*np.cos(6*(x+c))

# a completed fourier case
def func_fourier(x, *a):
    # pay attention that the fourier coefficients coeff is a list of [a[0],a[1],...,b[0],b[1],...], namely list(a)+list(b)
    y = a[0]
    l=len(a)/2
    for i in range(1,l):
    # for i in range(1,6):
        y = y + a[i]*np.cos(i*x) + a[i+l]*np.sin(i*x)
    return y

# a cos fourier case
# pay attention that the phase angle c is the same
def func_cosFourier(x, *a):
    # a[0] is the phase c
    # a[1] is a0
    c = a[0]
    y = a[1]
    for i in range(2, len(a)):
        y = y + a[i]*np.cos((i-1) * (x+c))
    return y

# get the precise fourier expanded expression coefficients
# but further fourier fitting is recommanded for integral inaccuracy and truncation error 
def fourier(x, y, n = -1, threshold = 1e-6):
    # obtain the trancated fourier coefficients of f(x)
    # pay attention that f(x)=a0+sum(ai*cos(i*x)+bi*sin(i*x)), a0 is the same as a0/2 in original fourier formula!
    # when n < 0, the threshold is used in trancation
    # when n > 0, the threshold is ignored and n is the trancation length
    a = [0]
    b = [0]
    if n < 0:
        n = MAX_ORDER + 1
        # 100 items are used to control the time
    a[0] = sum(y[0:36])/18/2
    deviation = a[0] - y
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    for i in range(1,n+1):
        tmp_cos = np.cos(i*x[0:36])
        tmp_a = sum(y[0:36]*tmp_cos[0:36])/18
        a.append(tmp_a)

        tmp_sin = np.sin(i*x[0:36])
        tmp_b = sum(y[0:36]*tmp_sin[0:36])/18
        b.append(tmp_b)

        deviation = a[i]*np.cos(i*x) + b[i]*np.sin(i*x) + deviation
        RMS = np.sqrt(np.average(np.power(deviation,2)))
        if n > MAX_ORDER:
            if RMS < threshold:
                break
            if i > MAX_ORDER:
                print 'Pay attention! Threshold used in fourier(), but ' + str(MAX_ORDER+1) + ' items has been reached! Forced to exit!'
    
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
	    print 'RMS\t' + str(RMS)
    return a, b, deviation

# fit simple fourier in 6 order
def fit_fourier6(x, y):
    opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier6, x, y, maxfev=1000)
    a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6 = opt_parms
    fit_y=func_fourier6(x, a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6)
    deviation = fit_y - y
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
	    print 'RMS\t' + str(RMS)
    return a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6, deviation

# fit fourier in controllable order
def fit_fourier(x, y, init_guess=None, n = 6):
    # n is the trancated length
    # if init_guess is not defined, then n is used. Otherwise, n is ignored. Then the trancated length is the same as the init_guess 
    if init_guess == None:
        a=[1]*(n+1)
        b=[1]*(n+1)
        opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier, x, y, p0 = a+b, maxfev=1000)
    else:
        opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier, x, y, p0 = init_guess, maxfev=1000)

    deviation = func_fourier(x,*opt_parms) - y
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
	    print 'RMS\t' + str(RMS)
    return opt_parms, deviation

# fit fourier in controllable order
def fit_fourier_noGuess(x, y, n = -1, threshold = 1e-6):
    # obtain the trancated fourier coefficients of f(x)
    # pay attention that f(x)=a0+sum(ai*cos(i*x)+bi*sin(i*x)), a0 is the same as a0/2 in original fourier formula!
    # when n < 0, the threshold is used in trancation
    # when n > 0, the threshold is ignored and n is the trancation length
	coeff_a, coeff_b, deviation = fourier(x,y,n,threshold)
	coeff, deviation = fit_fourier(x,y,coeff_a+coeff_b)
	RMS = np.sqrt(np.average(np.power(deviation,2)))
	if __printError__ == True:
		print 'RMS\t' + str(RMS)
	return coeff, deviation

# fit cos fourier in controllable order
def fit_cosFourier(x, y, init_guess=None, n = 6):
    # n is the trancated length
    # if init_guess is not defined, then n is used. Otherwise, n is ignored. Then the trancated length is the same as the init_guess 
    if init_guess == None:
        a=[1] + [1]*(n+1)
        try:
            opt_parms, parm_cov = sp.optimize.curve_fit(func_cosFourier, x, y, p0 = a, maxfev=1000)
        except RuntimeError:
            print 'Error - fit_cisFourier does not converge with 1000 steps'
            opt_parms = a
        except:
            print 'Unexpected error! ' + str(sys.exc_info()[0])
        # opt_parms, parm_cov = sp.optimize.curve_fit(func_cosFourier6, x, y, p0 = a, maxfev=1000)
        # opt_parms, parm_cov = sp.optimize.curve_fit(func_cosFourier6, x, y, maxfev=1000)
    else:
        try:
            opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier, x, y, p0 = init_guess, maxfev=1000)
        except RuntimeError:
            print 'Error - fit_cisFourier does not converge with 1000 steps'
            opt_parms = init_guess

    deviation = func_cosFourier(x,*opt_parms) - y
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
        print 'RMS\t' + str(RMS)
    return opt_parms, deviation

# fit fourier in controllable order
def fit_cosFourier_noGuess(x, y, n = -1, threshold = 1e-6):
    # obtain the trancated fourier coefficients of f(x)
    # pay attention that f(x)=a0+sum(ai*cos(i*x)+bi*sin(i*x)), a0 is the same as a0/2 in original fourier formula!
    # when n < 0, the threshold is used in trancation
    # when n > 0, the threshold is ignored and n is the trancation length
    
    # currently a initial guess like this would be better
    # coeff_a, coeff_b, deviation = fourier(x,y,n,threshold)
    
    # default initial guess used currently
    # plt.figure()
    # plt.plot(x, y,'*')
    # plt.show()

    step = 2
    if n > 0:
        coeff, deviation = fit_cosFourier(x, y, n=n)
    else:
        for tmp_n in range(4, COS_MAX_ORDER + 2 + step, step):    
            coeff, deviation = fit_cosFourier(x, y, n=tmp_n)
            RMS = np.sqrt(np.average(np.power(deviation,2)))
            if RMS < threshold:
                break
        if RMS > threshold:
            print('Pay attention! Threshold used in fit_cosFourier_noGuess(), but ' + str(COS_MAX_ORDER) + ' items has been reached! Forced to exit!')
    if __printError__ == True:
        print 'RMS\t' + str(RMS)
    return coeff, deviation


