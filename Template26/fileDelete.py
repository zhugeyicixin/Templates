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
C9H18_515_6_opt_B3LD3
C9H18_513_6_opt_B3LD3


'''


files=files.split()
for (index, tmp_file) in enumerate(files):
	files[index] = tmp_file[0:]+''
print len(files)


pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue
	if tmp_file in files:
		print tmp_file
		shutil.rmtree(tmp_file)

print 'hindered rotation scripts generated successfully!'

# THE END




