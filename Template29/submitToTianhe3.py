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
C9H18_155_05_5_opt_B3LD3
C9H18_155_08_5_opt_B3LD3
C9H18_196_04_5_opt_B3LD3
C9H18_273_00_5_opt_B3LD3
C9H18_273_03_5_opt_B3LD3
C9H18_273_05_5_opt_B3LD3
C9H18_273_08_5_opt_B3LD3








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




