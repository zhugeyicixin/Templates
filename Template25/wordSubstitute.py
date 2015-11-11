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
			# lines[0] = '%mem=16GB\n'
			# lines[1] = '%nprocshared=12\n'
			# lines[2] = '#p B3LYP/6-31G(d) opt=(gdiis,tight) int=ultrafine freq \n'
			fw.writelines(lines)
			fw.close()
			os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

			if os.path.exists(tmp_file + '/' + tmp_file+'.fchk'):
				os.remove(tmp_file + '/' + tmp_file+'.fchk')
			if os.path.exists(tmp_file + '/' + tmp_file+'.log'):
				os.remove(tmp_file + '/' + tmp_file+'.log')
			if os.path.exists(tmp_file + '/' + tmp_file+'.chk'):
				os.remove(tmp_file + '/' + tmp_file+'.chk')


# if os.path.exists(os.getcwd()+'/mesmerInput'):
	# shutil.rmtree(os.getcwd()+'/mesmerInput')

print 'hindered rotation scripts generated successfully!'

# THE END




