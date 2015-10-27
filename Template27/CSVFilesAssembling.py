# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil


increment = 10

pattern_file = re.compile('^DMH.*csv$')

#flags
header_done = 0
normal_check = 1

#counters
warn_file_num = 0
error_file_num = 0

pwd = os.getcwd()
pwd_home = pwd

if os.path.exists('DMH_650K_10atm_phi1_all.csv'):
	os.remove('DMH_650K_10atm_phi1_all.csv')

tmp_fileLists = os.listdir(pwd)
fw = file('DMH_650K_10atm_phi1_all.csv', 'w')
for tmp_file in tmp_fileLists:
	tmp_m = pattern_file.match(tmp_file)
	if tmp_m:
		print tmp_file
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		if header_done != 1:
			fw.writelines(tmp_lines[0:2])
			header_done = 1
		if len(tmp_lines) == 2 + increment:
			fw.writelines(tmp_lines[2:])
		else:
			print 'Warning!', tmp_file
			warn_file_num += 1
			fw.writelines(tmp_lines[2:])

print '\n csv files were assembled successfully!'
print 'warn_file_num:\t' + str(warn_file_num)
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful csv files!'

fw.close()
# THE END


