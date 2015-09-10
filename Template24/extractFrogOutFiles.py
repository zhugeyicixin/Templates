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
pattern_folder = re.compile('^.*_confSearch$')
# pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_end = re.compile('^.*.*$')

#flags
# cbs_success = 0
mol2Exist = 0

#counters
error_file_num = 0

pwd = os.getcwd()
pwd_home = pwd

if os.path.exists(pwd_home + '/FrogOutput'):
	shutil.rmtree('FrogOutput')
os.mkdir('FrogOutput')

tmp_folderLists = os.listdir(pwd)
for tmp_folder in tmp_folderLists:
	tmp_m = pattern_folder.match(tmp_folder)
	if tmp_m:
		# print tmp_folder
		os.chdir(tmp_folder)
		pwd = os.getcwd()
		tmp_fileLists = os.listdir(pwd)
		mol2Exist = 0
		for tmp_file in tmp_fileLists:
			succcess = 0
			if re.search('_minimized\.mol2',tmp_file):
				mol2Exist = 1
				fr = file(tmp_file)
				tmp_lines = fr.readlines()
				tmp_m = pattern_end.match(tmp_lines[-1])
				if tmp_m:
					succcess = 1
					# print tmp_file + '\tsucccess'
				else:
					print tmp_file + '\terror'
					error_file_num += 1
				shutil.copyfile(tmp_file, pwd_home + '/FrogOutput/' + tmp_file)
		if mol2Exist != 1:
			error_file_num += 1
			print tmp_folder + '\terror'
		os.chdir('../')

print '\n log files extracted successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!'

# THE END


