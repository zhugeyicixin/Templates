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
pattern_freq = re.compile('^.*Frequencies -- *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)?$')

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
			freq = []
			freq_done = -1
			for tmp_line in tmp_lines:
				if freq_done != 1:
					tmp2_m = pattern_freq.match(tmp_line)
					if tmp2_m:
						freq.extend(map(float,tmp2_m.groups()))
						freq_done = 0
					if freq_done == 0:
						if re.search('Thermochemistry', tmp_line):
							while None in freq:
								freq.remove(None)
							freq_done = 1
			for tmp_num in freq:
				if tmp_num<=0:
					print 'Error2! An imaginary frequency!' + tmp_file
					error_file_num += 1
					print freq
					break

		else:
			print 'Error1! ' + 'File did not end normally!' + tmp_file
			error_file_num += 1				
	else:
		print 'Error! Log file not found!', tmp_file
		error_file_num += 1		

print 'error_file_num: ', error_file_num

# THE END




