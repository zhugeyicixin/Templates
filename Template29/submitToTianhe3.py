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
tmp_fileLists = '''
C10H20_111_4_opt_M06
C10H20_166_4_opt_M06
C10H20_171_4_opt_M06
C10H20_179_4_opt_M06
C10H20_17_4_opt_M06
C10H20_190_4_opt_M06
C10H20_192_4_opt_M06
C10H20_195_4_opt_M06
C10H20_233_4_opt_M06
C10H20_251_4_opt_M06
C10H20_296_4_opt_M06
C10H20_305_4_opt_M06
C10H20_30_4_opt_M06
C10H20_322_4_opt_M06
C10H20_333_4_opt_M06
C10H20_394_4_opt_M06
C10H20_39_4_opt_M06
C10H20_411_4_opt_M06
C10H20_430_4_opt_M06
C10H20_43_4_opt_M06
C10H20_443_4_opt_M06
C10H20_483_4_opt_M06
C10H20_486_4_opt_M06
C10H20_50_4_opt_M06
C10H20_52_4_opt_M06
C10H20_58_4_opt_M06
C10H20_62_4_opt_M06
C10H20_74_4_opt_M06
C10H20_75_4_opt_M06
C10H20_9_4_opt_M06
C9H18_324_4_opt_M06
C9H18_420_4_opt_M06
C9H18_447_4_opt_M06
C9H18_497_4_opt_M06
C9H18_499_4_opt_M06
C9H18_506_4_opt_M06
C9H18_518_4_opt_M06
C9H18_519_4_opt_M06
C9H18_526_4_opt_M06
C9H18_540_4_opt_M06







'''
tmp_fileLists=tmp_fileLists.strip()
tmp_fileLists=tmp_fileLists.split()

#flags

# temporary variables
tmp_m = []


pwd = os.getcwd()


fw = file('testTH1.sh','w')
fw.write('''#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

''')
for tmp_file in tmp_fileLists:
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			fw.write('sh submitTH.sh ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>16))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			
''')

fw.close()
os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

print 'Tianhe submission script generated successfully!'

# THE END




