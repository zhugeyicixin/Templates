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
# pattern_MP4 = re.compile('^.*#P Geom=AllCheck Guess=TCheck SCRF=Check MP4SDQ/CBSB4.*$')
# pattern_energy = re.compile('^.*QCISD\(T\)= *(-?[0-9]+\.[0-9]+)D\+(-?[0-9]+).*$')
pattern_optEnergy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
pattern_zpe = re.compile('^.*Zero-point correction= *(-?[0-9]+\.[0-9]+) *\(Hartree/Particle\) *.*$')
pattern_optZPE = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_optEnthalpy = re.compile('^.*Sum of electronic and thermal Enthalpies= *(-?[0-9]+\.[0-9]+).*$')
# pattern_energy = re.compile('^.*E2 =    -0.2898122586D+.*$')
pattern_optimized = re.compile('^.* Optimized Parameters.*$')



#flags
optimized_done = 0

# temporary variables
tmp_row = 0

#build a new workbook
wb_new = Workbook()
sh=wb_new.add_sheet('energy')
sh.write(tmp_row,0,'name')
sh.write(tmp_row,1,'optEnergy')
sh.write(tmp_row,2,'zpe')
sh.write(tmp_row,3,'optZPE')
sh.write(tmp_row,4,'optEnthalpy')
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
			tmp_m = pattern_optEnergy.match(tmp_line)
			if tmp_m:
				optEnergy = float(tmp_m.group(1))
			tmp_m = pattern_zpe.match(tmp_line)
			if tmp_m:
				zpe = float(tmp_m.group(1))
			tmp_m = pattern_optZPE.match(tmp_line)
			if tmp_m:
				optZPE = float(tmp_m.group(1))
			tmp_m = pattern_optEnthalpy.match(tmp_line)
			if tmp_m:
				optEnthalpy = float(tmp_m.group(1))
			# tmp_m = pattern_optimized.match(tmp_line)
			# if tmp_m:
				# optimized_done = 1
				sh.write(tmp_row,0,tmp_file[0:-4])
				sh.write(tmp_row,1,optEnergy)
				sh.write(tmp_row,2, zpe)
				sh.write(tmp_row,3,optZPE)
				sh.write(tmp_row,4,optEnthalpy)
				tmp_row += 1
				# break


wb_new.save('tmpUB3LYP_freqEnergy.xls')
print 'energy data extracted successfully!'


# THE END


