# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
from xlwt import *
import pyExcelerator
from xlutils.copy import copy
from re import *
import re
import os
import shutil


import phys
import fourier
import GaussView
import MomInert

# control the open or close of gauss, this is used for test
# generally it should be set as True
__Gauss__ = False	

#input
name = 'freq'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# softwares
gview1 = GaussView.gview()
mominert1 = MomInert.MomInert()

# constants

#variables

# energy in hatree

# dihedral in degree

#flags

# temporary variables
tmp_m = []
tmp_num = 0

pwd = os.getcwd()

if __Gauss__ == True:
	if os.path.exists(pwd + '/' + 'geomConnect'):

		shutil.rmtree('geomConnect')
	os.mkdir('geomConnect')

	gview1.openSoft()

	# traverse folders to get .gjf file with connectivity
	tmp_fileLists = os.listdir(pwd)
	for tmp_file in tmp_fileLists:
		if not os.path.isdir(pwd + '\\' + tmp_file):
			continue
		tmp_pwd = pwd + '\\' + tmp_file
		# print tmp_pwd

		# if target directory found
		if re.search(name,tmp_file):
			tmp_num = 0
			# traverse files
			tmp_fileLists2 = os.listdir(tmp_pwd)
			for tmp_file2 in tmp_fileLists2:
				tmp_m = pattern_name.match(tmp_file2[0:-4])	
				# if target file found
				if tmp_m:
					print tmp_file2
					tmp_num = tmp_num + 1
					
					gview1.openAndSave(tmp_pwd, tmp_file2)
					shutil.move(tmp_pwd +'/' + 'result_' + tmp_file2[0:-4] + '.gjf',pwd + '/geomConnect')
	gview1.closeSoft()

# get mominert input file
if os.path.exists(pwd + '/' + 'mominertInput'):
	shutil.rmtree('mominertInput')
os.mkdir('mominertInput')
if os.path.exists(pwd + '/' + 'mominertOutput'):
	shutil.rmtree('mominertOutput')
os.mkdir('mominertOutput')

tmp_pwd = pwd + '\\' + 'geomConnect'
tmp_num	= 0
tmp_fileLists2 = os.listdir(tmp_pwd)
for tmp_file2 in tmp_fileLists2:
	if not tmp_file2[-4:] == '.gjf':
		continue
	tmp_m = pattern_name.match(tmp_file2[0:-4])
	if tmp_m:
		print tmp_file2
		tmp_num = tmp_num + 1
		tmp_input = mominert1.gjfTodat(tmp_pwd, tmp_file2)
		shutil.move(tmp_pwd + '/' + tmp_input, pwd + '/' + 'mominertInput')

# run input and get mominert output file
os.chdir('mominertInput')
tmp_pwd = os.getcwd()
tmp_fileLists2 = os.listdir(tmp_pwd)
for tmp_file2 in tmp_fileLists2:
	if re.search('.out',tmp_file2):
		os.remove(tmp_file2)
	else:
		mominert1.run(fileName = tmp_file2)
os.chdir('..')
for tmp_file2 in tmp_fileLists2:
	shutil.move(tmp_pwd + '/' + tmp_file2[0:-4] + '.out', pwd + '/' + 'mominertOutput')

# extract mominert output into excel
wb_new = Workbook()
sh = wb_new.add_sheet('MomInert')
# sh.cell_overwrite_ok=True
sh.write(0, 0, 'name')
sh.write(0, 1, 'bond')
sh.write(0, 2, 'key word')
sh.write(0, 3, 'symmetry number')
sh.write(0, 4, 'phaseV')
sh.write(0, 5, 'coeff_I0')
sh.write(0, 7, 'coeff_B0')
tmp_pwd = pwd + '/' + 'mominertOutput'
tmp_fileLists2 = os.listdir(tmp_pwd)
tmp_num	= 0
tmp_row = 0
for tmp_file2 in tmp_fileLists2:
	if re.search('.out',tmp_file2):
		tmp_num += 1
		tmp_row += 1
		sh.write(tmp_row, 0, tmp_file2[0: -4])
		tmp_bonds, tmp_I0s, tmp_B0s = mominert1.extractOutput(tmp_pwd, tmp_file2)
		for (index, tmp_bond) in enumerate(tmp_bonds):
			sh.write(tmp_row, 1, str(tmp_bond[0]) + ' ' + str(tmp_bond[1]))
			sh.write(tmp_row, 2, 'Ihrd1')
			sh.write(tmp_row, 3, 1)
			sh.write(tmp_row, 4, '0.00')
			sh.write(tmp_row, 5, tmp_I0s[index])
			sh.write(tmp_row, 7, tmp_B0s[index])
			tmp_row += 1
if os.path.exists('MomInertOutput.xls'):
	os.remove('MomInertOutput.xls')
wb_new.save('MomInertOutput.xls')
print 'MomInert data extracted successfully!'

# THE END


