# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os
import shutil


#input
files='''
C10H22_10_9_11_1_scan_M06.log	
C10H22_11_7_9_1_scan_M06.log	
C10H22_11_9_11_1_scan_M06.log	
C10H22_12_11_13_1_scan_M06.log	
C10H22_12_11_29_1_scan_M06.log	
C10H22_12_13_16_1_scan_M06.log	
C10H22_12_1_5_1_scan_M06.log	
C10H22_12_5_22_1_scan_M06.log	
C10H22_12_5_6_1_scan_M06.log	
C10H22_12_6_7_1_scan_M06.log	
C10H22_12_7_9_1_scan_M06.log	
C10H22_12_9_11_1_scan_M06.log	
C10H22_24_7_8_1_scan_M06.log	
C10H22_29_8_9_1_scan_M06.log	
C10H22_31_9_10_1_scan_M06.log	
C10H22_32_8_9_1_scan_M06.log	
C10H22_49_1_5_1_scan_M06.log	
C10H22_51_7_9_1_scan_M06.log	
C10H22_51_9_11_1_scan_M06.log	
C10H22_51_9_22_1_scan_M06.log	
C10H22_52_12_14_1_scan_M06.log	
C10H22_52_12_22_1_scan_M06.log	
C10H22_52_1_5_1_scan_M06.log	
C10H22_52_26_29_1_scan_M06.log	
C10H22_52_5_18_1_scan_M06.log	
C10H22_52_5_7_1_scan_M06.log	
C10H22_52_7_26_1_scan_M06.log	
C10H22_52_7_9_1_scan_M06.log	
C10H22_52_9_12_1_scan_M06.log	
C10H22_53_11_14_1_scan_M06.log	
C10H22_53_1_5_1_scan_M06.log	
C10H22_53_26_29_1_scan_M06.log	
C10H22_53_5_8_1_scan_M06.log	
C10H22_53_8_18_1_scan_M06.log	
C10H22_53_8_26_1_scan_M06.log	
C10H22_53_8_9_1_scan_M06.log	
C10H22_53_9_11_1_scan_M06.log	
C10H22_53_9_22_1_scan_M06.log	
C10H22_54_12_14_1_scan_M06.log	
C10H22_54_12_29_1_scan_M06.log	
C10H22_54_1_5_1_scan_M06.log	
C10H22_54_22_25_1_scan_M06.log	
C10H22_54_5_8_1_scan_M06.log	
C10H22_54_8_18_1_scan_M06.log	
C10H22_54_8_22_1_scan_M06.log	
C10H22_54_8_9_1_scan_M06.log	
C10H22_54_9_12_1_scan_M06.log	
C10H22_55_10_11_1_scan_M06.log	
C10H22_55_10_25_1_scan_M06.log	
C10H22_55_10_29_1_scan_M06.log	
C10H22_55_11_14_1_scan_M06.log	
C10H22_55_18_21_1_scan_M06.log	
C10H22_55_1_5_1_scan_M06.log	
C10H22_57_8_18_1_scan_M06.log	
C10H22_59_6_7_1_scan_M06.log	
C10H22_6_11_13_1_scan_M06.log	
C10H22_6_13_16_1_scan_M06.log	
C10H22_6_16_19_1_scan_M06.log	
C10H22_6_1_5_1_scan_M06.log	
C10H22_6_25_28_1_scan_M06.log	
C10H22_6_5_7_1_scan_M06.log	
C10H22_6_7_25_1_scan_M06.log	
C10H22_6_7_9_1_scan_M06.log	
C10H22_6_9_11_1_scan_M06.log	
C10H22_63_5_6_1_scan_M06.log	
C10H22_64_5_17_1_scan_M06.log	
C10H22_66_7_8_1_scan_M06.log	
C10H22_68_8_17_1_scan_M06.log	
C10H22_70_1_5_1_scan_M06.log	
C10H22_75_1_5_1_scan_M06.log	
C10H22_75_5_13_1_scan_M06.log	
C10H22_75_5_29_1_scan_M06.log	
C10H22_75_5_6_1_scan_M06.log	
C10H22_75_6_17_1_scan_M06.log	
C10H22_75_6_25_1_scan_M06.log	
C10H22_75_6_7_1_scan_M06.log	
C10H22_75_7_21_1_scan_M06.log	
C10H22_75_7_9_1_scan_M06.log	
C10H22_8_10_12_1_scan_M06.log	
C10H22_8_12_15_1_scan_M06.log	
C10H22_8_15_18_1_scan_M06.log	
C10H22_9_6_7_1_scan_M06.log	
C10H22_9_7_9_1_scan_M06.log	
C10H22_9_9_11_1_scan_M06.log	
C2H6_1_1_5_1_scan_M06.log	
C3H8_1_1_5_1_scan_M06.log	
C3H8_1_5_8_1_scan_M06.log	
C4H10_1_1_5_1_scan_M06.log	
C4H10_1_5_8_1_scan_M06.log	
C4H10_1_8_11_1_scan_M06.log	
C4H10_2_1_5_1_scan_M06.log	
C4H10_2_5_11_1_scan_M06.log	
C4H10_2_5_7_1_scan_M06.log	
C5H12_1_11_14_1_scan_M06.log	
C5H12_1_1_5_1_scan_M06.log	
C5H12_1_5_8_1_scan_M06.log	
C5H12_1_8_11_1_scan_M06.log	
C5H12_2_1_5_1_scan_M06.log	
C5H12_2_5_14_1_scan_M06.log	
C5H12_2_5_7_1_scan_M06.log	
C5H12_2_7_10_1_scan_M06.log	
C5H12_3_1_5_1_scan_M06.log	
C5H12_3_5_10_1_scan_M06.log	
C5H12_3_5_14_1_scan_M06.log	
C5H12_3_5_6_1_scan_M06.log	
C8H18_12_5_15_1_scan_M06.log	
C8H18_4_13_16_1_scan_M06.log	
C9H20_13_12_15_1_scan_M06.log	
C9H20_25_5_8_1_scan_M06.log	
C9H20_8_10_13_1_scan_M06.log	






'''


files=files.split()
for (index, tmp_file) in enumerate(files):
	files[index] = tmp_file[0:-4]+''
print len(files)


if os.path.exists('toBeSubmit'):
	shutil.rmtree('toBeSubmit')
os.mkdir('toBeSubmit')

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	tmp2_fileLists = os.listdir(os.path.join(pwd, tmp_file))
	for tmp2_file in tmp2_fileLists:
		if os.path.isfile(os.path.join(pwd, tmp_file, tmp2_file)):
			continue
		if tmp2_file in files:
			print tmp_file, tmp2_file
			if not os.path.exists(os.path.join('toBeSubmit', tmp_file)):
				os.mkdir(os.path.join('toBeSubmit', tmp_file))
			shutil.copytree(os.path.join(pwd, tmp_file, tmp2_file), os.path.join('toBeSubmit', tmp_file, tmp2_file))

print 'hindered rotation scripts generated successfully!'

# THE END




