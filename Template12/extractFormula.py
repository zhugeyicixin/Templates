# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
import numpy as np
from xlrd import *
from xlwt import *
from xlutils.copy import copy
import re
import os

import textExtractor
import chem

__energy__ = 'cbs'

###################
#get reactions to calculate
###################
name = ''
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[3].strip(' \n')
		if tmp_line == 'cbs':
			__energy__ = 'cbs'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'b3lyp':
			__energy__ = 'b3lyp'
			print '\n-------------------------------------\nb3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'cbsb3lyp':
			__energy__ = 'cbsb3lyp'
			print '\n-------------------------------------\ncbs verified and b3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'
		fr.close()	

wb=open_workbook('template.xls')
sh=wb.sheet_by_name('Reactions')

#definition of goal parameters
reacs_name = []					#reactants name list
TSs_name = []					#TSs name list
prods_name = []					#productions name list

reacs_abbr = []					#reactants Name Abbreviate list
TSs_abbr = []					#TSs Name Abbreviate list
prods_abbr = []					#productions Name Abbreviate list

reacs_form = []					#reactants formula list
TSs_form = []					#TSs formula list
prods_form = []					#productions formula list
thermoFactor_dict = {}

#definition of temporary variables
tmp_row = 2
tmp_col = 0
tmp_name = []
tmp_abbr = []
tmp_form = []
num_rows = sh.nrows
num_cols = sh.ncols
num_reac = 1
num_TS = 1
num_prod = 1

for tmp_row in range(2,num_rows):
	if int(sh.cell_value(tmp_row,0)) != 0:
		num_reac = int(int(sh.cell_value(tmp_row,0))/10)
		num_prod = int(sh.cell_value(tmp_row,0))%10
		tmp_name = []
		tmp_abbr = []
		tmp_form = []
		for i in range(num_reac + num_TS + num_prod):
			tmp_name.append(sh.cell_value(tmp_row,2+i*4))
			tmp_abbr.append(sh.cell_value(tmp_row,3+i*4))
			tmp_form.append(sh.cell_value(tmp_row,4+i*4))
			if i == (num_reac -1):
				reacs_name.append(tmp_name)
				reacs_abbr.append(tmp_abbr)
				reacs_form.append(tmp_form)
				tmp_name = []
				tmp_abbr = []
				tmp_form = []
			elif i == (num_reac + num_TS -1):
				TSs_name.append(tmp_name)
				TSs_abbr.append(tmp_abbr)
				TSs_form.append(tmp_form)
				tmp_name = []
				tmp_abbr = []
				tmp_form = []
			elif i == (num_reac + num_TS + num_prod-1):
				prods_name.append(tmp_name)
				prods_abbr.append(tmp_abbr)
				prods_form.append(tmp_form)
				tmp_name = []
				tmp_abbr = []
				tmp_form = []

print reacs_name
print TSs_name
print prods_name
print 'get reactions successfully!'

total = len(TSs_name) 			#total number of reactions

###################
#extract data
###################

#definition of goal parameters
formulaDict = {}
multi = 0
geom = ''
freq=[]						#frequencies
RSN = 0 					#external symmetry number
opticalNum = 0				#optical isomer number
rots = []					#rotational constants
hessian = []
energy = 0.0				#CBS-QB3 (0 K)

#definetion of comparing pattern
pattern_cbs = re.compile('^.*#.*[Cc][Bb][Ss]-[Qq][Bb]3.*$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_freqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
# note that Input orientation should be used in MESMER rather than standard orientation when hessian used
pattern_standard = re.compile('^.*Input orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_freq = re.compile('^.*Frequencies -- *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)?$')
pattern_RSN = re.compile('^.*Rotational symmetry number *([0-9]+).*$')
pattern_rots = re.compile('^.*Rotational constants \(GHZ\): *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+)$')
pattern2_rots = re.compile('^.*Rotational constant \(GHZ\): *(-?[0-9]+\.[0-9]+)$')
pattern_freqSum = re.compile('^.*\\\\Freq\\\\.*$')
if __energy__ == 'cbs':
	pattern_energy = re.compile('^.*CBS-QB3 \(0 K\)= *(-?[0-9]+\.[0-9]+).*$')
else:
	pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')

#definition of counter
count = 0					#count the num of line maybe tell() could be useful you could have a try if needed

#definition of flags
cbs_done = -1
multi_done = -1
freqCom_done = -1
standard_done = -1
coordinate_done = -1
freq_done = -1
RSN_done = -1
rots_done = -1
freqSum_done = -1
energy_done = -1

#definition of temporary variables
tmp_m = []		#match result 
tmp_name = ''	#the temporary name of the specie now
tmp_row = 3
tmp_blankline = ['blank']
tmp_index = 0
tmp_class = 1 	#1 for reactants 2 for products 3 for TSs
tmp_energies = []
tmp2_energies = []
tmp_barrier = 0.0
tmp_reverse_barrier = 0.0
tmp_num = 0
tmp_line = ''
tmp_mole = chem.molecule()
#sh=wb.sheet_by_index(1)
#sh.put_cell(1,1,2,2,0)			#

allSpecies_name = reacs_name + tmp_blankline + prods_name + tmp_blankline + TSs_name
allSpecies_abbr = reacs_abbr + tmp_blankline + prods_abbr + tmp_blankline + TSs_abbr
allSpecies_form = reacs_form + tmp_blankline + prods_form + tmp_blankline + TSs_form

#extract info
for i in range(len(allSpecies_name)):
	tmp_name = allSpecies_name[i]
	tmp2_energies = []

	if tmp_name == 'blank':
		tmp_class += 1
		tmp2_energies.append(0)
		tmp_energies.append(tmp2_energies)
		tmp_row += 1
		continue
	for j in range(len(tmp_name)):
		tmp2_name = tmp_name[j]
		freqFile=file('freq/'+ tmp2_name + '.log','r')

		#reset all variables
		multi = 0
		freq=[]						
		RSN = 0
		opticalNum = 0 					
		rots = []					
		hessian = []	
		energy = 0.0
			
		multi_done = -1
		freqCom_done = -1
		standard_done = -1
		coordinate_done = -1
		freq_done = -1
		RSN_done = -1
		rots_done = -1
		freqSum_done = -1
		energy_done = -1

		tmp_all_lines = freqFile.readlines()
		for (lineNum, line) in enumerate(tmp_all_lines):
			if freqCom_done != 1:
				if lineNum < len(tmp_all_lines) - 1:
					tmp_line = tmp_all_lines[lineNum].strip() + tmp_all_lines[lineNum+1].strip()
					tmp_m = pattern_freqCom.match(tmp_line)
					if tmp_m:
						freqCom_done = 1
			elif standard_done != 1:
				tmp_m = pattern_standard.match(line)
				if tmp_m:
					tmp_num = lineNum + 5
					standard_done = 1
			elif coordinate_done != 1:
				tmp_m = pattern_endline.match(line)
				if tmp_m:
					if lineNum > tmp_num:
						geom = textExtractor.geometryExtractor(tmp_all_lines[tmp_num: lineNum])
						geom = geom.replace('\t','    ')
						geom = geom.strip()
						geom = geom.split('\n')
						coordinate_done = 1			
		freqFile.close()
		if tmp2_name not in formulaDict.keys():
			tmp_mole.getGjfGeom(geom)
			tmp_mole.calcFormula()
			formulaDict[tmp2_name] = tmp_mole.formula
			if tmp_mole.formula != allSpecies_form[i][j]:
				print 'Error! Formula inconsistent for ' + tmp2_name

print formulaDict
	
print 'Formula extracted successfully!\n'


# THE END


