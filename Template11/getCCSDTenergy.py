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
pattern_T1 = re.compile('^.*T1 Diagnostic *= *([-\.0-9]+).*$')
pattern_energy = re.compile('^.*CCSD\(T\)= *(-?[0-9]+\.[0-9]+)D\+(-?[0-9]+).*$')

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
		T1Diag = 0.0
		energy = 0.0
		for tmp_line in fr.readlines():
			tmp_m = pattern_T1.match(tmp_line)
			if tmp_m:
				T1Diag = float(tmp_m.group(1))
			tmp_m = pattern_energy.match(tmp_line)
			if tmp_m:
				energy = float(tmp_m.group(1))*10**int(tmp_m.group(2))
				sh.write(tmp_row,0,tmp_file[0:-4])
				sh.write(tmp_row,1,T1Diag)
				sh.write(tmp_row,2,energy)
				tmp_row += 1


wb_new.save('tmpCCSDTEnergy.xls')
print 'energy data extracted successfully!'


# THE END


