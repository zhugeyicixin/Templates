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
files='''
s0008.log
s0049.log
s0066.log
s0100.log
s0152.log
s0153.log
s0159.log
s0181.log
s0204.log
s0225.log
s0231.log
s0233.log
s0234.log




'''


files=files.split()
for (index, tmp_file) in enumerate(files):
	if re.match('^.*\.log$', tmp_file):
		files[index] = tmp_file[0:-4]+''
print len(files)


if os.path.exists('toBeSubmit'):
	shutil.rmtree('toBeSubmit')
os.mkdir('toBeSubmit')

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	if tmp_file in files:
		print tmp_file
		shutil.copytree(tmp_file,os.path.join('toBeSubmit', tmp_file))

print 'hindered rotation scripts generated successfully!'

# THE END




