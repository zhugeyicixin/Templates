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
pattern_folder = re.compile('^[^L].*$')
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

if os.path.exists(pwd_home + '/LogFileError'):
	shutil.rmtree('LogFileError')
os.mkdir('LogFileError')

tmp_folderLists = os.listdir(pwd)
for tmp_folder in tmp_folderLists:
	if os.path.isfile(tmp_folder):
		continue
	tmp_m = pattern_folder.match(tmp_folder)
	if tmp_m:
		# print tmp_folder
		os.chdir(tmp_folder)
		pwd = os.getcwd()
		tmp_fileLists = os.listdir(pwd)
		logExist = False
		for tmp_file in tmp_fileLists:
			succcess = 0
			if re.search('.log',tmp_file):
				logExist = True
				fr = file(tmp_file)
				tmp_lines = fr.readlines()
				tmp_m = pattern_end.match(tmp_lines[-1])
				if tmp_m:
					succcess = 1
					# print tmp_file + '\tsucccess'
					shutil.copyfile(tmp_file, pwd_home + '/LogFileCollection/' + tmp_file)
				else:
					print tmp_file + '\terror'
					error_file_num += 1
					shutil.copyfile(tmp_file, pwd_home + '/LogFileError/' + tmp_file)

		if logExist == False:
			print tmp_folder + '\tlog file does not exist!'
			shutil.copyfile(tmp_folder+'.gjf', pwd_home + '/LogfileError/' + tmp_folder+'.gjf')
			error_file_num += 1
		os.chdir('../')

print '\n log files extracted successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!'

# THE END


