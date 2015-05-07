# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os

###################
#extract data
###################

#definition of goal parameters
energy = 0.0				#CBS-QB3 (0 K)

#definetion of comparing pattern
pattern_method = re.compile('^.*#.*cbs-qb3.*$')
pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')

# flags
method_done = 0

# tmporary varibles
tmp_row = 0

#build a new workbook
wb_new = Workbook()
sh=wb_new.add_sheet('energy')

#extract info

# os.chdir('tmpCBSFiles')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.log',tmp_file):
		fr=file(tmp_file,'r')
		print tmp_file
		method_done = 0
		for tmp_line in fr.readlines():
			if not method_done == 1:
				tmp_m = pattern_method.match(tmp_line)
				if tmp_m:
					method_done = 1
			else:
				tmp_m = pattern_energy.match(tmp_line)
				if tmp_m:
					energy = float(tmp_m.group(1))
					sh.write(tmp_row,0,tmp_file[0:-4])
					sh.write(tmp_row,1,energy)
					tmp_row += 1
					break


wb_new.save('tmpB3CBSB7Energy.xls')
print 'energy data extracted successfully!'


# THE END


