# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil


pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')

error_file_num = 0
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue

	print tmp_file
	if os.path.exists(os.path.join(tmp_file, tmp_file+'.log')):
		fr = file(os.path.join(tmp_file, tmp_file+'.log'), 'r')
		tmp_lines = fr.readlines()
		tmp_m = pattern_end.match(tmp_lines[-1])
		if tmp_m:
			pass
		else:
			print 'Error! ' + tmp_file + ' did not end normally!'
			error_file_num += 1				
	else:
		print 'Error! Log file not found!', tmp_file
		error_file_num += 1		

print 'error_file_num: ', error_file_num

# THE END




