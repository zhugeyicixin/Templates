# this code is used to traverse all jobs folder in current directory

from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil


#input
# clusterName can be 'cce' or 'TianheII' or 'Tianhe' or 'Tianhe2'
clusterName = 'TianheII'
name = ''
jobsPerSlot = 2

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*$')

#variables
tmp_jobList = []

#flags

# temporary variables
tmp_m = []
tmp_num = 0
slot_num = 1

pwd = os.getcwd()
tmp_files = os.listdir(pwd)
for tmp_file in tmp_files:
	if os.path.isfile(tmp_file):
		continue
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			tmp_jobList.append(tmp_file)	


fw2 = file('submitFleet.sh', 'w')
if clusterName == 'Tianhe' or clusterName == 'Tianhe2' or clusterName == 'TianheII':
	fw2.write('''#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

''')
else:
	fw2.write('''#!/bin/bash
#
''')

if clusterName == 'Tianhe' or clusterName == 'Tianhe2':
	fw2.write('''numJobs=`yhq |grep TH_SR | wc -l` 
while ((numJobs>18))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_SR | wc -l`  
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

for tmp_file in tmp_jobList:
	if re.search(name,tmp_file):
		tmp_m = pattern_name.match(tmp_file)
		if tmp_m:
			if tmp_num == 0:
				fw = file('slot_' + '%04d'%slot_num + '.sh', 'w')
				if clusterName == 'Tianhe' or clusterName == 'Tianhe2' or clusterName == 'TianheII':
					fw.write('#!/bin/bash\n\n')
				else:
					fw.write('''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
''')
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
			fw2.write('echo \'submit to Tianhe:\'\necho \'' + tmp_file + '\'\nyhbatch -pTH_SR -c 12 ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep TH_SR | wc -l` 
while ((numJobs>18))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_SR | wc -l`  
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
			fw2.write('qsub -pe smp 24 ' + tmp_file + '\nsleep 5\n')
			# fw2.write('qsub -pe orte 12 ' + tmp_file + '\nsleep 5\n')

fw2.close()
os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw2.name + ' > log_dos2unix.txt 2>&1')

print 'Tianhe submission script generated successfully!'

# THE END




