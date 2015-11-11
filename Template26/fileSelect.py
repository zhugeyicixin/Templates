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
C10H22_19_r014_C6_2_opt_B3L
C10H22_25_r020_C11_2_opt_B3L
C10H22_27_r015_C22_2_opt_B3L
C10H22_41_r002_C20_2_opt_B3L
C10H22_42_r007_C9_2_opt_B3L
C10H22_45_r020_C29_2_opt_B3L
C10H22_46_r019_C8_2_opt_B3L
C10H22_4_r003_C29_2_opt_B3L
C10H22_57_r005_C25_2_opt_B3L
C10H22_5_r007_C16_2_opt_B3L
C10H22_63_r007_C21_2_opt_B3L
C10H22_69_r006_C7_2_opt_B3L
C10H22_70_r021_C19_2_opt_B3L
C10H22_9_r020_C6_2_opt_B3L
C4H10_2_r007_C5_2_opt_B3L
C5H12_2_r001_C1_2_opt_B3L
C6H14_2_r013_C17_2_opt_B3L
C7H16_3_r012_C8_2_opt_B3L
C7H16_4_r006_C20_2_opt_B3L
C7H16_6_r001_C1_2_opt_B3L
C8H18_13_r002_C11_2_opt_B3L
C8H18_13_r007_C23_2_opt_B3L
C8H18_15_r006_C1_2_opt_B3L
C8H18_16_r012_C16_2_opt_B3L
C8H18_2_r014_C5_2_opt_B3L
C8H18_8_r010_C12_2_opt_B3L
C8H18_9_r004_C10_2_opt_B3L
C8H18_9_r010_C15_2_opt_B3L
C8H18_9_r012_C1_2_opt_B3L
C9H20_12_r007_C18_2_opt_B3L
C9H20_15_r013_C23_2_opt_B3L
C9H20_18_r015_C18_2_opt_B3L
C9H20_22_r019_C22_2_opt_B3L
C9H20_24_r018_C19_2_opt_B3L
C9H20_25_r016_C22_2_opt_B3L
C9H20_33_r016_C9_2_opt_B3L
C9H20_3_r005_C13_2_opt_B3L
C9H20_3_r016_C1_2_opt_B3L
C9H20_4_r001_C16_2_opt_B3L
C9H20_6_r017_C12_2_opt_B3L




'''


files=files.split()
for (index, tmp_file) in enumerate(files):
	files[index] = tmp_file[0:]+''
print len(files)


if os.path.exists('toBeSubmit'):
	shutil.rmtree('toBeSubmit')
os.mkdir('toBeSubmit')

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	if tmp_file in files:
		print tmp_file
		shutil.copytree(tmp_file,os.path.join('toBeSubmit', tmp_file))

print 'hindered rotation scripts generated successfully!'

# THE END




