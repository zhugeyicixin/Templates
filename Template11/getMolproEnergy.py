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
uhfEnergy = 0.0				
casEnergy = 0.0
rs2Energy = 0.0

#definetion of comparing pattern
pattern_uhf = re.compile('^.*!UHF STATE 1.1 Energy *(-?[0-9]+\.[0-9]+).*$')
pattern_cas = re.compile('^.*!MCSCF STATE 1.1 Energy *(-?[0-9]+\.[0-9]+).*$')
pattern_rs2 = re.compile('^.*!RSPT2 STATE 1.1 Energy *(-?[0-9]+\.[0-9]+).*$')

# flags
addrow = 0

tmp_row = 0

#build a new workbook
wb_new = Workbook()
sh=wb_new.add_sheet('energy')

#extract info

# os.chdir('tmpCBSFiles')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.xml',tmp_file):
		fr=file(tmp_file,'r')
		print tmp_file
		addrow = 0
		for tmp_line in fr.readlines():
			tmp_m = pattern_uhf.match(tmp_line)
			if tmp_m:
				uhfEnergy = float(tmp_m.group(1))
				# sh.write(tmp_row,0,tmp_file[0:-4])
				sh.write(tmp_row,1,uhfEnergy)
				addrow = 1
			tmp_m = pattern_cas.match(tmp_line)
			if tmp_m:
				casEnergy = float(tmp_m.group(1))
				# sh.write(tmp_row,0,tmp_file[0:-4])
				sh.write(tmp_row,2,casEnergy)
				addrow = 1
			tmp_m = pattern_rs2.match(tmp_line)
			if tmp_m:
				rs2Energy = float(tmp_m.group(1))
				sh.write(tmp_row,3,rs2Energy)
				addrow = 1
				break
		if addrow == 1:
			sh.write(tmp_row,0,tmp_file[0:-4])
			tmp_row += 1
				


wb_new.save('tmpMolproEnergy.xls')
print 'energy data extracted successfully!'


# THE END


