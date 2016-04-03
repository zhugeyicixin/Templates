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
D3Energy = 0.0				#CBS-QB3 (0 K)
SCFEnergy = 0.0

#definetion of comparing pattern
# pattern_MP4 = re.compile('^.*#P Geom=AllCheck Guess=TCheck SCRF=Check MP4SDQ/CBSB4.*$')
# pattern_energy = re.compile('^.*QCISD\(T\)= *(-?[0-9]+\.[0-9]+)D\+(-?[0-9]+).*$')
# pattern_energy = re.compile('^.*E2 =    -0.2898122586D+.*$')
pattern_D3Energy = re.compile('^.*Grimme-D3 Dispersion energy= *(-?[0-9]+\.[0-9]+) *Hartrees.*$')
pattern_SCFEnergy = re.compile('^.*SCF Done:  E\([RU]M062X\) = *(-?[0-9]+\.[0-9]+) *A\.U\. after.*$')




#flags
optimized_done = 0

# temporary variables
tmp_row = 0

#build a new workbook
wb_new = Workbook()
sh=wb_new.add_sheet('energy')
sh.write(tmp_row,0,'name')
sh.write(tmp_row,1,'D3Energy')
sh.write(tmp_row,2,'SCF energy without D3')
sh.write(tmp_row,3,'SCF energy with D3')
tmp_row += 1

#extract info
# os.chdir('tmpCBSFiles')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.log',tmp_file):
		fr=file(tmp_file,'r')
		print tmp_file
		# optimized_done = 0
		for tmp_line in fr.readlines():
			tmp_m = pattern_D3Energy.match(tmp_line)
			if tmp_m:
				D3Energy = float(tmp_m.group(1))
			tmp_m = pattern_SCFEnergy.match(tmp_line)
			if tmp_m:
				SCFEnergy = float(tmp_m.group(1))
			# tmp_m = pattern_optimized.match(tmp_line)
			# if tmp_m:
				# optimized_done = 1
				# break

		sh.write(tmp_row,0,tmp_file[0:-4])
		sh.write(tmp_row,1,D3Energy)
		sh.write(tmp_row,2,SCFEnergy-D3Energy)
		sh.write(tmp_row,3,SCFEnergy)
		tmp_row += 1
		fr.close()


wb_new.save('tmpM06D3Energy.xls')
print 'energy data extracted successfully!'


# THE END


