import class1
import class2
import class3
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
import re
import os

# print 'hellp'


wb_new=Workbook()

# class1_data
testdata=class1.class_data()
sh=wb_new.add_sheet('class1_data')
sh.write(0,0,'parts')
for i in range(0,len(testdata['parts'])):
	sh.write(i+2,0,testdata['parts'][i][0])
	sh.write(i+2,1,testdata['parts'][i][1])
sh.write(0,3,'downscale')
sh.write(1,3,'phases')
for i in range(0,len(testdata['downscale']['phases'])):
	sh.write(i+2,3,testdata['downscale']['phases'][i])
sh.write(1,4,'p_max_values')
for i in range(0,len(testdata['downscale']['p_max_values'])):
	sh.write(i+2,4,testdata['downscale']['p_max_values'][i])
sh.write(1,5,'factor_coeffs')
# for i in range(0,len(testdata['downscale']['factor_coeffs'])):
sh.write(2,5,testdata['downscale']['factor_coeffs'][0])
sh.write(2,6,testdata['downscale']['factor_coeffs'][1])
sh.write(2,7,testdata['downscale']['factor_coeffs'][2])
# sh.write(1,8,'v_max_split')
# sh.write(2,8,testdata['downscale']['v_max_split'])
sh.write(1,10,'cycle')
for i in range(0,len(testdata['cycle'])):
	sh.write(i+2,10,testdata['cycle'][i])

# class2_data
testdata=class2.class_data()
sh=wb_new.add_sheet('class2_data')
sh.write(0,0,'parts')
for i in range(0,len(testdata['parts'])):
	sh.write(i+2,0,testdata['parts'][i][0])
	sh.write(i+2,1,testdata['parts'][i][1])
sh.write(0,3,'downscale')
sh.write(1,3,'phases')
for i in range(0,len(testdata['downscale']['phases'])):
	sh.write(i+2,3,testdata['downscale']['phases'][i])
sh.write(1,4,'p_max_values')
for i in range(0,len(testdata['downscale']['p_max_values'])):
	sh.write(i+2,4,testdata['downscale']['p_max_values'][i])
sh.write(1,5,'factor_coeffs')
for i in range(0,len(testdata['downscale']['factor_coeffs'])):
	if testdata['downscale']['factor_coeffs'][i]==None:
		sh.write(i+2,5,'None')
		continue
	sh.write(i+2,5,testdata['downscale']['factor_coeffs'][i][0])
	sh.write(i+2,6,testdata['downscale']['factor_coeffs'][i][1])
	sh.write(i+2,7,testdata['downscale']['factor_coeffs'][i][2])
sh.write(1,8,'v_max_split')
sh.write(2,8,testdata['downscale']['v_max_split'])
sh.write(1,10,'cycle')
for i in range(0,len(testdata['cycle'])):
	sh.write(i+2,10,testdata['cycle'][i])

# class3_data_a
testdata=class3.class_data_a()
sh=wb_new.add_sheet('class3_data_a')
sh.write(0,0,'parts')
for i in range(0,len(testdata['parts'])):
	sh.write(i+2,0,testdata['parts'][i][0])
	sh.write(i+2,1,testdata['parts'][i][1])
sh.write(0,3,'downscale')
sh.write(1,3,'phases')
for i in range(0,len(testdata['downscale']['phases'])):
	sh.write(i+2,3,testdata['downscale']['phases'][i])
sh.write(1,4,'p_max_values')
for i in range(0,len(testdata['downscale']['p_max_values'])):
	sh.write(i+2,4,testdata['downscale']['p_max_values'][i])
sh.write(1,5,'factor_coeffs')
for i in range(0,len(testdata['downscale']['factor_coeffs'])):
	sh.write(i+2,5,testdata['downscale']['factor_coeffs'][i][0])
	sh.write(i+2,6,testdata['downscale']['factor_coeffs'][i][1])
	sh.write(i+2,7,testdata['downscale']['factor_coeffs'][i][2])
sh.write(1,8,'v_max_split')
sh.write(2,8,testdata['downscale']['v_max_split'])
sh.write(1,10,'cycle')
for i in range(0,len(testdata['cycle'])):
	sh.write(i+2,10,testdata['cycle'][i])

# class3_data_b
testdata=class3.class_data_b()
sh=wb_new.add_sheet('class3_data_b')
sh.write(0,0,'parts')
for i in range(0,len(testdata['parts'])):
	sh.write(i+2,0,testdata['parts'][i][0])
	sh.write(i+2,1,testdata['parts'][i][1])
sh.write(0,3,'downscale')
sh.write(1,3,'phases')
for i in range(0,len(testdata['downscale']['phases'])):
	sh.write(i+2,3,testdata['downscale']['phases'][i])
sh.write(1,4,'p_max_values')
for i in range(0,len(testdata['downscale']['p_max_values'])):
	sh.write(i+2,4,testdata['downscale']['p_max_values'][i])
sh.write(1,5,'factor_coeffs')
for i in range(0,len(testdata['downscale']['factor_coeffs'])):
	sh.write(i+2,5,testdata['downscale']['factor_coeffs'][i][0])
	sh.write(i+2,6,testdata['downscale']['factor_coeffs'][i][1])
	sh.write(i+2,7,testdata['downscale']['factor_coeffs'][i][2])
sh.write(1,8,'v_max_split')
sh.write(2,8,testdata['downscale']['v_max_split'])
sh.write(1,10,'cycle')
for i in range(0,len(testdata['cycle'])):
	sh.write(i+2,10,testdata['cycle'][i])




wb_new.save('data_all.xls')
print 'data extracted successfully!'

# sh=wb.sheet_by_index(0)
