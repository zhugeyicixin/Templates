import numpy as np
import scipy as sp
from scipy import interpolate

import phaseSpaceIntegral

# input area
target_T = 298.15
target_dict = {
'C/C/H3-C/C3/H':1.64267889914,
'C/C/H3-C/C2/H2':1.65575079163,
'C/C/H3-C/C/H3':1.72192579763,
'C/C/H3-C/C4':1.47941120136,
'C/C4-C/C4':1.53596305371,
'C/C3/H-C/C3/H':0.680626772989,
'C/C2/H2-C/C2/H2':0.936735134149,
'C/C3/H-C/C4':0.877959036282,
'C/C2/H2-C/C3/H':0.842140035991,
'C/C2/H2-C/C4':0.911315420043,
}
# target_integrals = [1, 2, 3]

# calculate key-value table
# unit: cm^-1
# V(x)=V/2-V/2*cos(n*x)
# n=1
integral_list = []
V_list = range(100,2000,5) + range(2000,5000,25)
for tmp_V in V_list:
	V = tmp_V
	PG_coeff_V = V*np.array([0.5, -0.5, 0.0, 0.0])
	tmp_integral = phaseSpaceIntegral.fourierPotentialInt(coeff_V=PG_coeff_V,temperature=target_T, numSegment=300, zeroShift=False)
	integral_list.append(tmp_integral)
	# print V, tmp_integral

# # integral_list = np.array(integral_list)
# for i in xrange(len(integral_list)-1):
# 	print V_list[i], np.log(integral_list[i]/integral_list[i+1])

# B-Spline interpolation to get new V for values of certain integrals
tck = interpolate.splrep(integral_list[::-1], V_list[::-1])
# V_new = interpolate.splev(target_integrals, tck)
for tmp_rot in target_dict.keys():
	V_new = interpolate.splev(target_dict[tmp_rot], tck)
	print tmp_rot, V_new

# test_coeff_V = np.array([535.0612726, 1.517096498, -3.054160898, -538.05935, 0.0, -5.136394671, -2.387745805, 7.00944267])
# tmp_integral = phaseSpaceIntegral.fourierPotentialInt(coeff_V=test_coeff_V,temperature=target_T, numSegment=300)
# print tmp_integral
# V_new = interpolate.splev(tmp_integral, tck)
# print V_new

