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
clusterName = 'TianheII'
name = ''
jobsPerSlot = 4

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*$')

#variables
tmp_fileLists = '''

C12H24_092_1003_1_opt_B3L
C12H24_092_1008_1_opt_B3L
C12H24_092_1009_1_opt_B3L
C12H24_092_1010_1_opt_B3L
C12H24_092_1011_1_opt_B3L
C12H24_092_2001_1_opt_B3L

C14H28_093_1000_1_opt_B3L
C14H28_093_1001_1_opt_B3L
C14H28_093_1002_1_opt_B3L
C14H28_093_1003_1_opt_B3L
C14H28_093_1004_1_opt_B3L
C14H28_093_1005_1_opt_B3L








'''
tmp_fileLists=tmp_fileLists.strip()
tmp_fileLists=tmp_fileLists.split()

#flags

# temporary variables
tmp_m = []
tmp_num = 0
slot_num = 1

pwd = os.getcwd()


fw2 = file('submitFleet.sh', 'w')
if clusterName == 'Tianhe' or clusterName == 'Tianhe2' or clusterName == 'TianheII':
	fw2.write('''#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

''')
else:
	fw2.write('''#!/bin/csh
#
''')

if clusterName == 'Tianhe' or clusterName == 'Tianhe2':
	fw2.write('''numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done

''')

if clusterName == 'TianheII':
	fw2.write('''numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done

''')


for tmp_file in tmp_fileLists:
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			if tmp_num == 0:
				fw = file('slot_' + '%04d'%slot_num + '.sh', 'w')
				fw.write('#!/bin/bash\n\n')
			if clusterName == 'TianheII':
				fw.write('sh ' + tmp_file + '/' + tmp_file + '''.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
''')
			else:			
				fw.write('sh ' + tmp_file + '/' + tmp_file + '.job\n')
			tmp_num += 1
			if tmp_num >= jobsPerSlot:
				tmp_num = 0
				slot_num += 1
				if clusterName == 'TianheII':
					fw.write('wait\n')
				fw.close()
				os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
if clusterName == 'TianheII' and tmp_num != 0:
	fw.write('wait\n')
fw.close()
os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

tmp_fileList = os.listdir('.')
for tmp_file in tmp_fileList:
	if re.search('slot_.*sh', tmp_file):
		if clusterName == 'Tianhe' or clusterName == 'Tianhe2':
			fw2.write('echo \'submit to Tianhe:\'\necho \'' + tmp_file + '\'\nyhbatch -pTH_NET -c 12 ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
''')
		elif clusterName == 'TianheII':
			fw2.write('echo \'submit to TianheII:\'\necho \'' + tmp_file + '\'\nyhbatch -N 1 ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done
''')
		else:
			fw2.write('sh submit12.sh ' + tmp_file + '\nsleep 5\n')

fw2.close()
os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw2.name + ' > log_dos2unix.txt 2>&1')

print 'Tianhe submission script generated successfully!'

# THE END




