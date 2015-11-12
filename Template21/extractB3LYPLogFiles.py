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



# pattern_folder = re.compile('^RO2_[0-9]+.*$')
pattern_folder = re.compile('^.*opt_631gd$')
# pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')

#flags
# cbs_success = 0
logFile = -1

#counters
error_file_num = 0
errorFiles = []

pwd = os.getcwd()
pwd_home = pwd



tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	succcess = 0
	if re.search('.log',tmp_file):
		logFile = 1
		fr = file(tmp_file,'r')
		tmp_lines = fr.readlines()
		fr.close()
		tmp_m = re.match('.*am1.*',tmp_lines[85].lower())
		if tmp_m:
			print 'am1 used! ' + tmp_file
		tmp_m = pattern_end.match(tmp_lines[-1])
		if tmp_m:
			succcess = 1
			# print tmp_file + '\tsucccess'
			# shutil.copyfile(tmp_file, pwd_home + '/LogFileCollection_1_631gd/' + tmp_file)
		else:
			print tmp_file + '\terror'
			errorFiles.append(tmp_file)
			os.remove(tmp_file)
			error_file_num += 1
	


# for tmp_folder in errorFiles:
# 	if os.path.exists(tmp_folder + '/' + tmp_folder + '.log'):
# 		os.remove(pwd_home + '/' + tmp_folder + '/' + tmp_folder + '.log')
# 	if os.path.exists(tmp_folder + '/' + tmp_folder + '.chk'):
# 		os.remove(pwd_home + '/' + tmp_folder + '/' + tmp_folder + '.chk')
# 	if os.path.exists(tmp_folder + '/' + tmp_folder + '.fchk'):
# 		os.remove(pwd_home + '/' + tmp_folder + '/' + tmp_folder + '.fchk')		

 
print '\n log files extracted successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!'

# THE END


