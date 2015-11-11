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
			print 'sh submitTH.sh ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			'''


print 'Tianhe submission script generated successfully!'

# THE END




