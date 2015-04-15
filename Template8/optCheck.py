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
import matplotlib.pyplot as plt

#input
# frozen_num1 = 27
# frozen_num2 = 29
# name = 'C9H19O2_2_26'



# symbol indicating the position
# pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
# pattern_optimized = re.compile('^.*Optimized Parameters.*$')
# pattern_standard = re.compile('^.*Standard orientation:.*$') 
# pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')

pattern_name = re.compile('^.*RO2_1_210.*$')
pattern_step = re.compile('^.*Step number *([0-9]+) out of a maximum of.*$')
pattern_scf = 	re.compile('^.*SCF Done.*E\(UB3LYP\) = *(-?[0-9]+\.[0-9]+).*$')
pattern_change = re.compile('^.*Predicted change in Energy=(-?[0-9]+\.[0-9]+)D(-?[0-9]+).*$')
#flags
# multi_done = 0
# optimized_done = 0
# Standard_done = 0
# skip_line = 0
# coordinate_done = 0

#variables
stepNum = []
energy = []
energyChange = []

# temporary variables
tmp_energy = 0
tmp_m = []

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	stepNum = []
	energy = []
	energyChange = []

	multi_done = 0
	optimized_done = 0
	Standard_done = 0
	skip_line = 0
	coordinate_done = 0

	if re.search('.log',tmp_file):
		tmp_m = pattern_name.match(tmp_file[0:-4])
		if tmp_m:
			if os.path.isfile(tmp_file[0:-4] +'_optCheck.xls'):
				os.remove(tmp_file[0:-4] +'_optCheck.xls')

			fr = file(tmp_file,'r')
			for tmp_line in fr.readlines():
				tmp_m = pattern_scf.match(tmp_line)
				if tmp_m:
					tmp_energy = float(tmp_m.group(1))
					continue
				tmp_m = pattern_step.match(tmp_line)
				if tmp_m:
					stepNum.append(int(tmp_m.group(1)))
					energy.append(tmp_energy)
					continue
				tmp_m = pattern_change.match(tmp_line)
				if tmp_m:
					energyChange.append(float(tmp_m.group(1))*10**int(tmp_m.group(2)))
			fr.close()		

			wb_new=Workbook()
			sh=wb_new.add_sheet('optHistory')
			sh.write(0,0,'stepNum')
			sh.write(0,1,'energy')
			sh.write(0,2,'changeInEnergy')

			for i in range(0,len(stepNum)):
				sh.write(i+1,0,stepNum[i])
				sh.write(i+1,1,energy[i])
				sh.write(i+1,2,energyChange[i])
			wb_new.save(tmp_file[0:-4] + '_optCheck.xls')
			
			plt.figure(figsize=(8,4))
			plt.plot(stepNum,energy)
			plt.show()

print 'opt check runs successfully!'

# THE END


