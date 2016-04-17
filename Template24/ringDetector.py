# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil

import chem


# constants
pattern_logFile = re.compile('^(C[0-9]*H[0-9]*_*[0-9]*).*\.log$')
pattern_fileConf = re.compile('^(C[0-9]*H[0-9]*_[0-9]*_[0-9]+)_[0-9]+_.*$')
pattern_gjfFile = re.compile('^(C[0-9]*H[0-9]*_*[0-9]*_r[0-9]+_[CO0-9]+).*\.gjf$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$') 
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_input = re.compile('^.*Input orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
# pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_energy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')

# variables
energyDict = {}
molecules = []
multi = 1
ringMoles = []
ringConfs = []

#flags
logExist = 0
multi_done = 0
optimized_done = 0
standard_done = 0
coordinate_done = 0

# temporary variables
tmp_energy = 0.0

#counters
error_file_num = 0

# extract energies
os.chdir('_f2_lowestEnergy')
tmp_folderLists = os.listdir('.')
for tmp_folder in tmp_folderLists:
	logExist = 0
	tmp_energy = 0.0
	if os.path.isfile(tmp_folder):
		tmp_m = pattern_logFile.match(tmp_folder)
		if tmp_m:
			tmp_name = tmp_m.group(1)
			if tmp_name not in energyDict.keys():
				energyDict[tmp_name] = {} 
			fr = file(os.path.join(tmp_folder), 'r')
			tmp_lines = fr.readlines()
			tmp2_m = pattern_end.match(tmp_lines[-1])
			if not tmp2_m:
				print 'Error! ' + tmp_folder + ' not ends normally!'
				error_file_num += 1
			else:
				for tmp_line in tmp_lines:
					tmp3_m = pattern_energy.match(tmp_line)
					if tmp3_m:
						tmp_energy = float(tmp3_m.group(1))
				energyDict[tmp_name][tmp_folder[0:-4]] = tmp_energy
			fr.close()
	else:
		tmp_fileList = os.listdir(tmp_folder)
		# print tmp_folder
		for tmp_file in tmp_fileList:
			tmp_m = pattern_logFile.match(tmp_file)
			if tmp_m:
				logExist = 1
				tmp_name = tmp_m.group(1)
				if tmp_name not in energyDict.keys():
					energyDict[tmp_name] = {} 
				fr = file(os.path.join(tmp_folder, tmp_file), 'r')
				tmp_lines = fr.readlines()
				tmp2_m = pattern_end.match(tmp_lines[-1])
				if not tmp2_m:
					print 'Error! ' + tmp_file + ' not ends normally!'
					error_file_num += 1
				else:
					for tmp_line in tmp_lines:
						tmp3_m = pattern_energy.match(tmp_line)
						if tmp3_m:
							tmp_energy = float(tmp3_m.group(1))
					energyDict[tmp_name][tmp_file[0:-4]] = tmp_energy
				fr.close()
		if logExist != 1:
			print 'Error! The name of folder is not invalid! ' + tmp_folder	
			error_file_num += 1	

# extract geom from log files
molecules = sorted(energyDict.keys())
tmp_molecule = chem.molecule()
for tmp_mole in molecules:
	tmp_dict = energyDict[tmp_mole]
	sortedDict = sorted(tmp_dict.items(), key=lambda d:d[1])
	if len(sortedDict) > 0:
		tmp_file = sortedDict[0]
		fr = file(os.path.join(tmp_file[0], tmp_file[0]+'.log'))

		multi_done = 0
		optimized_done = 0
		standard_done = 0
		coordinate_done = 0

		tmp_lines = fr.readlines()
		for (lineNum, tmp_line) in enumerate(tmp_lines):
			if multi_done != 1:
				tmp_m = pattern_multi.match(tmp_line)
				if tmp_m:
					multi = int(tmp_m.group(1))
					multi_done = 1
			elif optimized_done != 1:
				tmp_m = pattern_optimized.match(tmp_line)
				if tmp_m:
					optimized_done = 1
			elif standard_done != 1:
				tmp_m = pattern_standard.match(tmp_line)
				if tmp_m: 
					tmp_num = lineNum + 5
					standard_done = 1
			elif coordinate_done != 1:
				tmp_m = pattern_endline.match(tmp_line)
				if tmp_m:
					if lineNum > tmp_num:
						# tmp_geom = textExtractor.geometryExtractor(tmp_lines[tmp_num: lineNum])
						tmp_geom = tmp_lines[tmp_num: lineNum]
						coordinate_done = 1

		tmp_molecule.getLogGeom(tmp_geom)
		tmp_molecule.setLabel(tmp_mole)
		tmp_molecule.fulfillBonds()
		if tmp_molecule.existRings():
			ringMoles.append(tmp_molecule.label)
			for tmp_str in tmp_dict.keys():
				print tmp_str
				ringConfs.append(tmp_str)

os.chdir('../')

print '\nRing detection completed successfully!'
print 'There are ' + str(len(ringMoles)) + ' molecules and ' + str(len(ringConfs)) + ' corresponding conformers containing rings in total.' 

# THE END


