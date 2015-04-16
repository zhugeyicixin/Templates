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


#input
directory = 'rotation6'
charmap={'rotation1': directory,',gdiis': ''}
name = 'TS'

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*_[34]_.*_1_scan.*$')

#variables

#flags

# temporary variables
tmp_m = []

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			print tmp_file
			fw = file(tmp_file + '/' + tmp_file + '.job','r+')
			lines = fw.readlines()
			# print lines
			lines[10] = re.sub(r'rotation1',lambda x: charmap[x.group(0)], lines[10])
			fw.seek(0)
			fw.truncate()
			# fw.writelines(lines)
			fw.write(
# Tsinghua100 cluster
'''#BSUB -J ''' + tmp_file + '''
#BSUB -q hpc_linux
#BSUB -R "select[mem>30000]"
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -o /work2/hexin_work/26DMH/rotation/''' + directory + '/' + tmp_file + '''/output.%J
#BSUB -e /work2/hexin_work/26DMH/rotation/''' + directory + '/' + tmp_file + '''/error.%J

export g09root=/home/hexin/gaussian
export GAUSS_SCRDIR=/scratch
source $g09root/g09/bsd/g09.profile

cd /work2/hexin_work/26DMH/rotation/''' + directory + '/' + tmp_file + '''
$g09root/g09/g09 ''' + tmp_file + '''.gjf ''' + tmp_file + '''.log
$g09root/g09/formchk ''' + tmp_file + '''.chk
		

''')

# cce cluster
# '''#!/bin/csh
# #
# #$ -cwd
# #$ -j y
# #$ -S /bin/csh
# #
# setenv GAUSS_SCRDIR /state/partition1
# setenv g09root /share/apps
# source $g09root/g09/bsd/g09.login

# cd /home/hetanjin/DMH/rotation/''' + directory + '/' + tmp_file + '''
# /share/apps/g09/g09 ''' + tmp_file + '''.gjf
# /share/apps/g09/formchk ''' + tmp_file + '''.chk


# ''')

			fw.close()
			os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

			fw = file(tmp_file + '/' + tmp_file + '.gjf','r+')
			lines = fw.readlines()
			# print lines
			lines[3] = re.sub(r',gdiis',lambda x: charmap[x.group(0)], lines[3])
			fw.seek(0)
			fw.truncate()
			fw.writelines(lines)
			fw.close()
			os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)



print 'hindered rotation scripts generated successfully!'

# THE END




