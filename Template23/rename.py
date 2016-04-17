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



# pattern_folder = re.compile('^RO2_[0-9]+.*$')
pattern_file = re.compile('^.*_9_SP_M06D3.log$')

pwd = os.getcwd()

tmp_folderLists = os.listdir(pwd)
for (index,tmp_file) in enumerate(tmp_folderLists):
	tmp_m = pattern_file.match(tmp_file)
	if tmp_m:
		print tmp_file
		os.rename(tmp_file, tmp_file[0:-15]+'_7_SP_M06D3.log')

 
print '\n rename successfully!'
# THE END


