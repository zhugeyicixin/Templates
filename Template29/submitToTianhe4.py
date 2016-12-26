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
clusterName = 'Tianhe'
name = '.gjf'
jobsPerSlot = 6

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*$')

#variables
tmp_fileLists = '''

s000004.log
s000008.log
s000009.log
s000017.log
s000024.log
s000026.log
s000030.log
s000032.log
s000035.log
s000036.log
s000037.log
s000038.log
s000039.log
s000042.log
s000048.log
s000051.log
s000052.gjf
s000053.gjf
s000054.gjf
s000055.gjf
s000056.gjf
s000057.gjf
s000058.gjf
s000059.gjf
s000060.gjf
s000061.log
s000079.log
s000080.log
s000081.log
s000082.log
s000084.log
s000085.log
s000086.log
s000088.log
s000092.log
s000093.log
s000094.log
s000106.log
s000125.log
s000126.log
s000127.log
s000129.log
s000132.log




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
	fw2.write('''numJobs=`yhq |grep pTH_SR | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep pTH_SR | wc -l`  
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
			fileName = tmp_file[0:-4]
			if tmp_num == 0:
				fw = file('slot_' + '%04d'%slot_num + '.sh', 'w')
				fw.write('#!/bin/bash\n\n')
			if clusterName == 'TianheII':
				fw.write('sh ' + fileName + '/' + fileName + '''.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
''')
			else:			
				fw.write('sh ' + fileName + '/' + fileName + '.job\n')
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
numJobs=`yhq |grep pTH_SR | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep pTH_SR | wc -l`  
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




