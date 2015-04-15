import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize

from fourier import *

def main():
    x = np.array([-3.06884618787763,    -2.8943132626782,   -2.71978033747877,  -2.54524741227933,  -2.3707144870799,   -2.19618156188047,  -2.02164863668103,  -1.8471157114816,   -1.67258278628217,  -1.49804986108274,  -1.3235169358833,   -1.14898401068387,  -0.974451085484436, -0.799918160285004, -0.62538523508557,  -0.450852309886138, -0.276319384686705, -0.101786459487272, 0.0727464657121614, 0.247279390911594,  0.421812316111027,  0.59634524131046,   0.770878166509893,  0.945411091709326,  1.11994401690876,   1.29447694210819,   1.46900986730763,   1.64354279250706,   1.81807571770649,   1.99260864290592,   2.16714156810536,   2.34167449330479,   2.51620741850422,   2.69074034370366,   2.86527326890309,   3.03980619410252,   3.21433911930195])
    V = np.array([0,    16.3196946382522,   54.7887690588831,   97.2639139443635,   127.877771839499,   131.447526708245,   102.810257345438,   48.8421039208769,   0.619796350598335,  5.31391975283622,   103.611559227108,   286.535763353109,   475.069300115108,   619.516748197376,   725.656216233968,   795.701544828712,   823.652078069746,   799.894168719649,   723.767198070883,   601.453108139336,   446.385941073298,   273.431152589619,   99.1516152322292,   -55.3065097257494,  -154.958746619522,  -168.20557693392,   -109.112032443284,  -10.7906897366046,  95.7016935124993,   177.190648861229,   218.120911806821,   217.721467979252,   181.550512403249,   123.066887907683,   61.2911439612507,   15.882940120995,    0.0103153139352798])

   
    a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6, deviation = fit_fourier6(x, V)
    fit_V1 = func_fourier6(x,a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6)
    
    coeff_a, coeff_b, deviation = fourier(x,V,n=-1,threshold=np.std(V)/4e1)
    print coeff_a,coeff_b
    fit_V2 = func_fourier(x, *(coeff_a+coeff_b))

    coeff, deviation = fit_fourier_noGuess(x,V,n=6)
    print  coeff
    # coeff, deviation = fit_fourier(x,V)
    fit_V3 = func_fourier(x,*coeff)

    fig = plt.figure()
    # ax1 = fig.add_subplot(3,1,1)
    # ax2 = fig.add_subplot(3,1,2)
    # ax3 = fig.add_subplot(3,1,3)

    # ax1.plot(x,V,x,fit_V1)
    # ax2.plot(x,V,x,fit_V2)
    # ax3.plot(x,V,x,fit_V3)

    ax = fig.add_subplot(3,1,1)
    ax.plot(x,V,x,fit_V1)
    ax = fig.add_subplot(3,1,2)
    ax.plot(x,V,x,fit_V2)

    # plt.plot(x,V)
    # fit_y = model_func(x, a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6, phi)
    # plot(ax1, x, y, V, fit_y, (A0, K0, C0), (A, K, C0))
    # ax1.set_title('Non-linear Fit')

    # Linear Fit (Note that we have to provide the y-offset ("C") value!!
    # A, K = fit_exp_linear(x, y, C0)
    # fit_y = model_func(x, A, K, C0)
    # plot(ax2, x, y, V, fit_y, (A0, K0, C0), (A, K, 0))
    # ax2.set_title('Linear Fit')
    # print a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6
    plt.show()

def plot(ax, x, y, V, fit_y, orig_parms, fit_parms):
    A0, K0, C0 = orig_parms
    A, K, C = fit_parms

    ax.plot(x, y, 'k--', 
      label='Actual Function:\n $y = %0.2f e^{%0.2f x} + %0.2f$' % (A0, K0, C0))
    ax.plot(x, fit_y, 'b-',
      label='Fitted Function:\n $y = %0.2f e^{%0.2f x} + %0.2f$' % (A, K, C))
    ax.plot(x, V, 'ro')
    ax.legend(bbox_to_anchor=(1.05, 1.1), fancybox=True, shadow=True)

# def func_fourier6(x, a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6):
#     return a0+a1*np.cos(x)+b1*np.sin(x)+a2*np.cos(2*(x))+b2*np.sin(2*(x))+a3*np.cos(3*(x))+b3*np.sin(3*(x))+a4*np.cos(4*(x))+b4*np.sin(4*(x))+a5*np.cos(5*(x))+b5*np.sin(5*(x))+a6*np.cos(6*(x))+b6*np.sin(6*(x))

# def fit_fourier6(x, y):
#     opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier6, x, y, maxfev=1000)
#     a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6 = opt_parms
#     fit_y=func_fourier6(x, a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6)
#     deviation = np.sqrt(np.average(np.power(y-fit_y,2)))
#     print 'deviation0\t' + str(deviation)
#     return a0, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, b5, b6

# def fit_fourier(x, y, init_guess=None, n = 6):
#     # n is the trancated length
#     # if init_guess is not defined, then n is used. Otherwise, n is ignored. Then the trancated length is the same as the init_guess 
#     if init_guess == None:
#         a=[1]*(n+1)
#         b=[1]*(n+1)
#         opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier, x, y, p0 = [a+b], maxfev=1000)
#     else:
#         opt_parms, parm_cov = sp.optimize.curve_fit(func_fourier, x, y, p0 = init_guess, maxfev=1000)

#     deviation = np.sqrt(np.average(np.power(y-func_fourier(x,*opt_parms),2)))
#     print 'deviation2\t' + str(deviation) 
#     return opt_parms, deviation

# # def func_fourier(x, a, b):
# def func_fourier(x, *a):
#     # pay attention that the fourier coefficients coeff is a list of [a[0],a[1],...,b[0],b[1],...], namely list(a)+list(b)
#     y = a[0]
#     l=len(a)/2
#     for i in range(1,l):
#     # for i in range(1,6):
#         y = y + a[i]*np.cos(i*x) + a[i+l]*np.sin(i*x)
#     return y

#     y = a[0]
#     print len(a)
#     for i in range(1,len(a)):
#     # for i in range(1,6):
#         y = y + a[i]*np.cos(i*x) + b[i]*np.sin(i*x)
#     return y

# def fourier(x, y, n = -1, threshold=1e2):
#     # obtain the trancated fourier coefficients of f(x)
#     # pay attention that f(x)=a0+sum(ai*cos(i*x)+bi*sin(i*x)), a0 is the same as a0/2 in original fourier formula!
#     # when n < 0, the threshold is used in trancation
#     # when n > 0, the threshold is ignored and n is the trancation length
#     a = [0]
#     b = [0]
#     if n < 0:
#         n = 100
#         # 100 items are used to control the time
#     a[0] = sum(y[0:36])/18/2
#     deviation = y - a[0]
#     for i in range(1,n+1):
#         tmp_cos = np.cos(i*x[0:36])
#         tmp_a = sum(y[0:36]*tmp_cos[0:36])/18
#         a.append(tmp_a)

#         tmp_sin = np.sin(i*x[0:36])
#         tmp_b = sum(y[0:36]*tmp_sin[0:36])/18
#         b.append(tmp_b)

#         deviation = deviation - a[i]*np.cos(i*x) - b[i]*np.sin(i*x)
#         if n > 99:
#             if np.sqrt(np.average(np.power(deviation,2))) < threshold:
#                 break
#             if i > 99:
#                 print 'Pay attention! Threshold used in fourier(), but 100 items has been reached! Forced to exit!'
#     deviation = np.sqrt(np.average(np.power(deviation,2)))
#     print 'deviation1\t' + str(deviation)
#     return a, b, deviation


if __name__ == '__main__':
    main()
