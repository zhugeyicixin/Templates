import numpy as np
import fourier
import phys

phys1 = phys.phys()

# calculate potential integral in phase space
# coeff_V is the fitted fourier coefficients of potential curve
# numSegment is the number of small intervals divided from 2*pi
# if zeroShift is True, then shift the whole potential curve above x axis, i.e. the zero energy corresponding to the point with the lowest energy
# if zeroShift is false, then use the original potential curve determined by coeff_V 
def fourierPotentialInt(coeff_V, temperature=298.15, numSegment=100, zeroShift=True):
	theta = np.array(range(0, numSegment+1))*2*np.pi/numSegment
	dtheta = theta[1]
	
	potential = fourier.func_fourier(theta, *coeff_V)
	potential = phys1.cmm1ToJoul(potential)
	if zeroShift:
		potential -= np.min(potential)
	y = np.exp(-potential/phys1.k/temperature)
	integralResult = (np.sum(y) - (y[1] + y[-1])/2.0) * dtheta

	return integralResult

def fourierPotentialInertiaInt(coeff_V, coeff_I, temperature=298.15, numSegment=100):
	theta = np.array(range(0, numSegment+1))*2*np.pi/numSegment
	dtheta = theta[1]
	
	potential = fourier.func_fourier(theta, *coeff_V)
	potential = phys1.cmm1ToJoul(potential)
	inertia = fourier.func_cosFourier(theta, *coeff_I)
	y = np.exp(-potential/phys1.k/temperature)*np.sqrt(inertia)
	integralResult = (np.sum(y) - (y[1] + y[-1])/2.0) * dtheta

	return integralResult	