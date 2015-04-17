import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt
import sys
from scipy import optimize

import phys

# if set __printError__ = True, then the root mean square RMS of devidation list(fit_y)-list(y) would be printed
__printError__ = False

# the max_order in fourier() expand
MAX_ORDER = 15
COS_MAX_ORDER = 18

phys1 = phys.phys()

# the arrhenius formula, a[0] is A, a[1] is n, a[2] is Ea
# unit: Ea [cal/mol], A [s**-1 or cm**-3/mol/s], k [s**-1 or cm**-3/mol/s] 
def func_arrhenius(T, *a):
    return a[0]*T**a[1]*np.exp(-phys1.calToJoul(a[2])/phys1.R/T)

def func_arrheniuslog(T, *a):
    return np.log(a[0])+a[1]*np.log(T)-phys1.calToJoul(a[2])/phys1.R/T

def func_arrheniuslogTm1(Tm1, *a):
    return np.log(a[0])-a[1]*np.log(Tm1)-phys1.calToJoul(a[2])*Tm1/phys1.R    

# the 3-parameter arrhenius formula
# unit: Ea [cal/mol], A [s**-1 or cm**-3/mol/s], k [s**-1 or cm**-3/mol/s] 
def func_arrhenius3(T, A, n, Ea):
    return A*T**n*np.exp(-phys1.calToJoul(Ea)/phys1.R/T)

def func_arrhenius3log(T, A, n, Ea):
    return np.log(A)+n*np.log(T)-phys1.calToJoul(Ea)/phys1.R/T

def resi_arrhenius(a, k, T):
    return k - func_arrhenius(T, *a)

def resi_arrheniuslog(a, ln_k, T):
    return ln_k - func_arrheniuslog(T, *a)

def resi_arrheniuslogTm1(a, ln_k, Tm1):
    return ln_k - func_arrheniuslogTm1(Tm1, *a)    

# fit arrhenius
def fit_arrhenius(T, k, init_guess=None):
    if init_guess == None:
        a = [1,1,1]
        # leastsq could be tried in the future
        try:
            opt_parms, parm_cov = sp.optimize.curve_fit(func_arrheniuslog, T, np.log(k), p0 = a, maxfev=1000)
            # opt_parms, parm_cov = sp.optimize.curve_fit(func_arrhenius3, T, k, maxfev=1000)
            # opt_parms, parm_cov = sp.optimize.curve_fit(func_arrhenius3log, T, np.log(k), maxfev=1000)
        except RuntimeError:
            print 'Error - fit_arrhenius does not converge with 1000 steps'
            opt_parms = a
        except:
            print 'Unexpected error!' + str(sys.exc_info()[0])
            opt_parms = a
    else:
        try:
            # opt_parms, parm_cov = sp.optimize.curve_fit(func_arrhenius, T, k, p0 = init_guess, maxfev=1000)
            opt_parms1, parm_cov = sp.optimize.curve_fit(func_arrheniuslog, T, np.log(k), p0 = init_guess, maxfev=1000)
            # opt_parms, parm_cov = sp.optimize.curve_fit(func_arrheniuslogTm1, 1.0/T, np.log(k), p0 = init_guess, maxfev=1000)            
        except RuntimeError:
            # print 'Error - fit_arrhenius does not converge with 1000 steps'
            opt_parms1 = init_guess
        except:
            print 'Unexpected error!' + str(sys.exc_info()[0])
            opt_parms1 = init_guess

        # opt_parms = optimize.leastsq(resi_arrhenius, init_guess, args=(k, T))
        opt_parms2 = optimize.leastsq(resi_arrheniuslog, init_guess, args=(np.log(k), T))
        # opt_parms = optimize.leastsq(resi_arrheniuslogTm1, init_guess, args=(np.log(k), 1.0/T))
        opt_parms2 = opt_parms2[0]

        deviation1 = func_arrhenius(T,*opt_parms1) - k
        rela_deviation1 = deviation1/k
        rela_RMS1 = np.sqrt(np.average(np.power(rela_deviation1,2)))
        deviation2 = func_arrhenius(T,*opt_parms2) - k
        rela_deviation2 = deviation2/k
        rela_RMS2 = np.sqrt(np.average(np.power(rela_deviation2,2)))
        if rela_RMS1 < rela_RMS2:
            opt_parms = opt_parms1
            # print 'curve_fit win', rela_RMS1, rela_RMS2
        else:
            opt_parms = opt_parms2
            # print 'leastsq win', rela_RMS1, rela_RMS2

    deviation = func_arrhenius(T,*opt_parms) - k
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
        print 'RMS\t' + str(RMS)
    return opt_parms, deviation

# fit arrhenius without guess
def fit_arrhenius_noGuess(T, k, threshold = 1e-6):
    ln_k = np.log(k)
    Tm1 = 1.0/T
    tmp_Ea, tmp_A = np.polyfit(Tm1, ln_k, 1)
    tmp_Ea = -tmp_Ea * phys1.R / phys1.calToJoul(1)
    tmp_A = np.exp(tmp_A)

    a = [tmp_A, 0.0, tmp_Ea]
    coeff, deviation = fit_arrhenius(T, k, a)
    # coeff, deviation = fit_arrhenius(T, k)    

    # plt.plot(1000.0/T, np.log(k), 'r*', 1000.0/T, np.log(func_arrhenius(T,*a)),'b')
    # plt.show()
    # print k

    rela_deviation = deviation/k
    rela_RMS = np.sqrt(np.average(np.power(rela_deviation,2)))
    if rela_RMS > threshold:
        print 'Warning! The relative RMS ' + str(rela_RMS) + ' is larger then the threshold ' + str(threshold) + '!'
    RMS = np.sqrt(np.average(np.power(deviation,2)))
    if __printError__ == True:
        print 'RMS\t' + str(RMS)
        print 'relative RMS\t' + str(rela_RMS)
    return coeff, deviation, rela_RMS




