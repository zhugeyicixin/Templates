# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
import numpy as np
from xlrd import *
from xlwt import *
from xlutils.copy import copy
import re
import os

import textExtractor

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

#definition of temporary variables
tmp_row = 2
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
multi = 0
geom = ''
freq=[]						#frequencies
RSN = 0 					#external symmetry number
rots = []					#rotational constants
hessian = []
energy = 0.0				#CBS-QB3 (0 K)

#definetion of comparing pattern
pattern_cbs = re.compile('^.*#.*[Cc][Bb][Ss]-[Qq][Bb]3.*$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_freqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
pattern_standard = re.compile('^.*Standard orientation:.*$') 
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
#sh=wb.sheet_by_index(1)
#sh.put_cell(1,1,2,2,0)			#

#build a new workbook
sheets = [s.name for s in wb.sheets()]
wb_new = copy(wb)
sh=wb_new.get_sheet(sheets.index('SpeciesInfo'))				#if overwrite to use cell_overwrite_ok=True
sh2=wb_new.get_sheet(sheets.index('SpeciesGeom'))
sh3=wb_new.get_sheet(sheets.index('SpeciesHessian'))

sh.write(1,0,total)

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

		# only if __energy__ == 'cbs', then check whether the freq file is cbs file 
		# if __energy__ == 'cbs':
		if 'cbs' in __energy__:	
			cbs_done = -1
		else:
			cbs_done = 1

		tmp_all_lines = freqFile.readlines()
		for (lineNum, line) in enumerate(tmp_all_lines):
			if cbs_done != 1:
				if line == tmp_all_lines[-1]:
					print 'error: ' + tmp2_name + 'not cbs freq file'
				tmp_m = pattern_cbs.match(line)
				if tmp_m:
					cbs_done = 1
			elif multi_done != 1:
				tmp_m = pattern_multi.match(line)
				if tmp_m:
					multi = tmp_m.group(1)
					multi_done = 1
			elif freqCom_done != 1:
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
			elif freq_done != 1:
				tmp_m = pattern_freq.match(line)
				if tmp_m:
					freq.extend(tmp_m.groups())
					freq_done = 0
				if freq_done == 0:
					if re.search('Thermochemistry',line):
						while None in freq:
							freq.remove(None)
						freq_done = 1
			elif RSN_done != 1:
				tmp_m=pattern_RSN.match(line)
				if tmp_m:	
					RSN = tmp_m.group(1)
					RSN_done = 1
			elif rots_done != 1:
				tmp_m = pattern_rots.match(line)
				if tmp_m:
					rots.extend(tmp_m.groups())
					rots_done = 1
				else:
					tmp_m=pattern2_rots.match(line)
					if tmp_m:
						rots.extend(tmp_m.groups())
						rots.append(rots[0])
						rots.append(rots[0])
						rots[0] = '0.0'
						rots_done = 1
			elif freqSum_done != 1:
				if freqSum_done < 0:
					tmp_m = pattern_freqSum.match(line)
					if tmp_m:
						freqSum_done = 0
						tmp_num = lineNum
				elif line != '\n':
					continue
				else:
					hessian = textExtractor.hessianExtractor(tmp_all_lines[tmp_num:lineNum])
					if len(hessian) != ((3*len(geom))*(3*len(geom)+1)/2):
						print 'Error! The size of hessian matrix does not equal to 3*N!'
					freqSum_done = 1
					break							
		freqFile.close()

		energyFile = file('energy/'+ tmp2_name + '.log','r')
		for line in energyFile.readlines():
			if energy_done != 1:
				tmp_m = pattern_energy.match(line)
				if tmp_m:
					energy = tmp_m.group(1)
					energy_done = 1
		energyFile.close

		#write info
		tmp_index = i - (total+1)*(tmp_class-1)					#tmp_index is the NO. of reaction
		sh.write(tmp_row,0,10 * len(reacs_name[tmp_index]) + len(prods_name[tmp_index]))
		sh.write(tmp_row,1,allSpecies_abbr[i][j])
		sh.write(tmp_row,2,allSpecies_name[i][j])
		sh.write(tmp_row,3,float(energy))
		sh.write(tmp_row,10,allSpecies_form[i][j])
		print tmp2_name
		sh.write(tmp_row,11,float(rots[0]))
		sh.write(tmp_row,12,float(rots[1]))
		sh.write(tmp_row,13,float(rots[2]))
		sh.write(tmp_row,14,np.sqrt(float(rots[1])*float(rots[2])))
		sh.write(tmp_row,15,int(RSN))
		sh.write(tmp_row,16,int(multi))
		sh.write(tmp_row,17,allSpecies_name[i][j])
		
		tmp2_energies.append(float(energy))

		if tmp_class == 1:
			sh.write(tmp_row,4,'R')
			sh.write(tmp_row,7,0.0)
			sh.write(tmp_row,8,0.0)
		elif tmp_class ==2:
			sh.write(tmp_row,4,'P')
			sh.write(tmp_row,7,0.0)
			sh.write(tmp_row,8,0.0)
		elif float(freq[0]) < 0:
			sh.write(tmp_row,4,'T')
			tmp_barrier = float(energy) - sum(tmp_energies[i - (total+1) * 2])
			sh.write(tmp_row,5,tmp_barrier)
			tmp_reverse_barrier = float(energy) - sum(tmp_energies[i - (total+1)])
			sh.write(tmp_row,6, tmp_reverse_barrier)
			sh.write(tmp_row,7,627.51*tmp_barrier)
			sh.write(tmp_row,8,627.51*tmp_reverse_barrier)
			sh.write(tmp_row,18,-float(freq[0]))
			freq.pop(0)
		else:
			# sh.write(tmp_row,4,'Error')
			sh.write(tmp_row,4,'T')
			tmp_barrier = float(energy) - sum(tmp_energies[i - (total+1) * 2])
			sh.write(tmp_row,5,tmp_barrier)
			tmp_reverse_barrier = float(energy) - sum(tmp_energies[i - (total+1)])
			sh.write(tmp_row,6, tmp_reverse_barrier)
			sh.write(tmp_row,7,627.51*tmp_barrier)
			sh.write(tmp_row,8,627.51*tmp_reverse_barrier)

		sh.write(tmp_row,19,len(freq))
		for k in range(len(freq)):
			if float(freq[k]) > 0:
				sh.write(tmp_row,21+k,float(freq[k]))
			else:
				sh.write(tmp_row,21+k,'error ' + str(freq[k]))

		sh2.write(0, tmp_row-2, allSpecies_abbr[i][j])
		sh2.write(1, tmp_row-2, allSpecies_name[i][j])
		sh2.write(2, tmp_row-2, len(geom))
		for (index, x) in enumerate(geom):
			sh2.write(index+3, tmp_row-2, x)

		sh3.write(0, tmp_row-2, allSpecies_abbr[i][j])
		sh3.write(1, tmp_row-2, allSpecies_name[i][j])
		sh3.write(2, tmp_row-2, len(hessian))
		for (index, x) in enumerate(hessian):
			sh3.write(index+3, tmp_row-2, x)

		tmp_row += 1

	tmp_energies.append(tmp2_energies)

wb_new.save(name + '.xls')
print 'data extracted successfully!\n'


# THE END


