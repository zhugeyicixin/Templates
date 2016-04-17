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
pattern_folder = re.compile('^.*M06D3$')
# pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')

#flags
# cbs_success = 0

#counters
error_file_num = 0

pwd = os.getcwd()
pwd_home = pwd

if os.path.exists(pwd_home + '/LogFileCollection'):
	shutil.rmtree('LogFileCollection')
os.mkdir('LogFileCollection')

tmp_folderLists = os.listdir(pwd)
for tmp_folder in tmp_folderLists:
	tmp_m = pattern_folder.match(tmp_folder)
	if tmp_m:
		print tmp_folder
		os.chdir(tmp_folder)
		pwd = os.getcwd()
		tmp_fileLists = os.listdir(pwd)
		for tmp_file in tmp_fileLists:
			succcess = 0
			if re.search('.log',tmp_file):
				fr = file(tmp_file)
				tmp_lines = fr.readlines()
				tmp_m = pattern_end.match(tmp_lines[-1])
				if tmp_m:
					succcess = 1
					print tmp_file + '\tsucccess'
				else:
					print tmp_file + '\terror'
					error_file_num += 1

				shutil.copyfile(tmp_file, pwd_home + '/LogFileCollection/' + tmp_file)
		os.chdir('../')

print '\n log files extracted successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!'

# THE END


