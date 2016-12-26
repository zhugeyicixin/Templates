# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil
import random

#input
directory = 'rotation3'
charmap={'rotation1': directory,',gdiis': '', '%chk=': '%chk=/scratch/','%chk=/scratch/':'%chk='}
name = ''
path='/WORK/tsinghua_xqyou_1/hetanjin/PODEn/_002_confSearch/'
useRandomSelect = True

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*$')

#variables

#flags

# temporary variables
tmp_m = []

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			print tmp_file
			tmp2_fileLists = os.listdir(tmp_file)
			possibility = 1.0
			if useRandomSelect == True:
				if len(tmp2_fileLists) <= 5000:
					possibility = 1.0
				elif len(tmp2_fileLists) <= 10000:
					possibility = 0.5
				elif len(tmp2_fileLists) <= 20000:
					possibility = 0.25
				else:
					possibility = 0.1

			for tmp2_file in tmp2_fileLists:
				if os.path.isdir(tmp2_file):
					continue
				if re.match('^.*com$', tmp2_file) and random.random() <= possibility:
					fr = file(tmp_file+'/'+tmp2_file, 'r')
					tmp_lines = fr.readlines()
					fr.close()
					tmp_lines.pop(2)

					newName = '' + tmp2_file[0:-4]
					if os.path.exists(tmp_file+'/'+newName):
						shutil.rmtree(tmp_file+'/'+newName)
					os.mkdir(tmp_file+'/'+newName)
					
					fw = file(tmp_file+'/'+newName+'/'+newName+'.gjf', 'w')
					fw.writelines(tmp_lines)
					fw.close()
					os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

					fw = file(tmp_file+'/'+newName+'/'+newName + '.job','w')
					fw.write('''#!/bin/bash

cd ''' + path + tmp_file + '/' + newName + '''
g09 ''' + newName + '''.gjf

					''')
					fw.close()
					os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

print 'Gaussian jobs generated successfully!'

# THE END




