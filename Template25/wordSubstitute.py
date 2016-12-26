# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil


#input
directory = 'rotation3'
charmap={'rotation1': directory,',gdiis': '', '%chk=': '%chk=/scratch/','%chk=/scratch/':'%chk='}
name = ''
path='/WORK/tsinghua_xqyou_1/hetanjin/PODEn/_001_opt/'

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
			fw = file(tmp_file + '/' + tmp_file + '.gjf','r+')
			lines = fw.readlines()
			# print lines
			# lines[2] = re.sub(r'%chk=',lambda x: charmap[x.group(0)], lines[2])
			fw.seek(0)
			fw.truncate()
			lines[0] = '%mem=15GB\n'
			lines[1] = '%nprocshared=12\n'
			lines[2] = '#p opt=(calcfc,ts) freq b3lyp/6-31g(d) empiricaldispersion=gd3bj \n'
			# lines[2] = '#p PM6 opt=gdiis  \n'
			#p PM6 opt  
			# if re.match('^.*chk=.*$', lines[2]):  
				# lines.pop(2)
			# lines[2] = '#p M062X/def2TZVPP opt=(ts,calcfc,tight) freq int=ultrafine     \n'
			# lines.insert(2, '#p B3LYP/6-311++G(d,p) opt=(gdiis,tight) int=ultrafine EmpiricalDispersion=GD3BJ     \n')

			fw.writelines(lines)
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

# 			fw = file(tmp_file + '/' + tmp_file + '.job','w')
# 			fw.write('''#!/bin/bash

# export GAUSS_SCRDIR=/vol-th/home/you/scratch
# export g09root=/vol-th/home/you/softwares/gaussian/g09D01

# source $g09root/g09/bsd/g09.profile

# cd ''' + path + tmp_file + '''
# $g09root/g09/g09 ''' + tmp_file + '''.gjf

# 				''')
# 			fw.close()
# 			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			fw = file(tmp_file + '/' + tmp_file + '.job','w')
			fw.write('''#!/bin/bash

cd ''' + path + tmp_file + '''
g09 ''' + tmp_file + '''.gjf

				''')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

# 			fw = file(tmp_file + '/' + tmp_file + '.job','w')
# 			fw.write('''#!/bin/bash

# export GAUSS_SCRDIR=/state/partition1
# export g09root=/home/hetanjin/apps/g09D01
# source $g09root/g09/bsd/g09.profile

# cd ''' + path + tmp_file + '''
# $g09root/g09/g09 ''' + tmp_file + '''.gjf

# 				''')
# 			fw.close()
# 			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')



			if os.path.exists(tmp_file + '/' + tmp_file+'.fchk'):
				os.remove(tmp_file + '/' + tmp_file+'.fchk')
			if os.path.exists(tmp_file + '/' + tmp_file+'.log'):
				os.remove(tmp_file + '/' + tmp_file+'.log')
			if os.path.exists(tmp_file + '/' + tmp_file+'.chk'):
				os.remove(tmp_file + '/' + tmp_file+'.chk')
			if os.path.exists(tmp_file + '/' + tmp_file+'.com'):
				os.remove(tmp_file + '/' + tmp_file+'.com')

# if os.path.exists(os.getcwd()+'/mesmerInput'):
	# shutil.rmtree(os.getcwd()+'/mesmerInput')

print 'hindered rotation scripts generated successfully!'

# THE END




