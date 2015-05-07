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
pattern_MP2 = re.compile('^.*#P Geom=AllCheck Guess=TCheck SCRF=Check MP2/CBSB3 CBSExtrap.*$')
pattern_energy = re.compile('^.*EUMP2 = *(-?[0-9]+\.[0-9]+)D\+(-?[0-9]+).*$')

tmp_row = 0

#build a new workbook
wb_new = Workbook()
sh=wb_new.add_sheet('energy')

#flags
MP2_done = 0
energy_done = 0

#extract info

# os.chdir('tmpCBSFiles')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	MP2_done = 0
	energy_done = 0
	if re.search('.log',tmp_file):
		fr=file(tmp_file,'r')
		for tmp_line in fr.readlines():
			if MP2_done != 1:
				tmp_m = pattern_MP2.match(tmp_line)
				if tmp_m:
					energy_done = 0
					MP2_done = 1
			elif energy_done != 1:
				tmp_m = pattern_energy.match(tmp_line)
				if tmp_m:
					energy = float(tmp_m.group(1))*10**int(tmp_m.group(2))
					sh.write(tmp_row,0,tmp_file[0:-4])
					sh.write(tmp_row,1,energy)
					tmp_row += 1
					MP2_done = 0
					energy_done = 1


wb_new.save('tmpMP2Energy.xls')
print 'energy data extracted successfully!'


# THE END


