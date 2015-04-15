# this is a math lib file
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import scipy

# interpolate one or two numbers into a list using second order Taylor series
# interpolationNum is the dict of {position: number of numbers to be inserted} 
def interpolation(listA, interpolationNum):
	tmp_index = 0
	listB = []
	for tmp_key in sorted(interpolationNum.keys()):
		listB = listB + listA[tmp_index: tmp_key]
		tmp_index = tmp_key
		if not len(listA) > (tmp_key + interpolationNum[tmp_key]):
			print 'Error! The listA	is not long enough for interpolation!'
		if interpolationNum[tmp_key] == 1:
			listB.append((4*(listA[tmp_key]+listA[tmp_key-1])-(listA[tmp_key+1]+listA[tmp_key-2]))/6)
		elif interpolationNum[tmp_key] == 2:
			listB.append(listA[tmp_key]/2 - listA[tmp_key+1]/5 + listA[tmp_key-1] - listA[tmp_key-2]*3/10)
			listB.append(listA[tmp_key] - listA[tmp_key+1]*3/10 + listA[tmp_key-1]/2 - listA[tmp_key-2]/5)
		else:
			print 'Error! Missing number in the list is more then 2!'
	listB += listA[tmp_index:]
	return listB

# interpolation using spline()
def interpolation2(partDict, points):
	positive_1 = 0
	positive_2 = 0
	nege_start = 0

	listA = range(1,points+1)
	list_key = sorted(partDict.keys())
	list_value = [partDict[x] for x in list_key]
	# B-spline interpolation
	tck = interpolate.splrep(list_key, list_value)
	listB = interpolate.splev(listA, tck)
	if listB[0] < 0:
		print 'Error! The 0th number in the interpolated list of lamm output is negative!'
	for i in range(0,points):
		if listB[i] > 0:
			if nege_start == 1:
				positive_2 = i
				f_linear = interpolate.interp1d([listA[positive_1], listA[positive_2]], [listB[positive_1], listB[positive_2]])
				listB[positive_1+1: positive_2] = f_linear(listA[positive_1+1: positive_2])
				nege_start = 0
		else:
			if nege_start != 1:
				positive_1 = i - 1
			nege_start = 1
	return listB

