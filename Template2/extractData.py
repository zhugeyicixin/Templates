# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re

###################
#get reactions to calculate
###################

wb=open_workbook('template.xls')
sh=wb.sheet_by_index(0)

#definition of goal parameters
reacs_name = []					#reactants name list
TSs_name = []					#TSs name list
prods_name = []					#productions name list

reacs_abbr = []					#reactants Name Abbreviat list
TSs_abbr = []					#TSs Name Abbreviat list
prods_abbr = []					#productions Name Abbreviat list

reacs_form = []					#reactants formula list
TSs_form = []					#TSs formula list
prods_form = []					#productions formula list

#definition of temporary variables
tmp_row = 2
num_rows = sh.nrows
num_cols = sh.ncols

for tmp_row in range(2,num_rows):
	reacs_name.append(sh.cell_value(tmp_row,2))
	reacs_abbr.append(sh.cell_value(tmp_row,3))
	reacs_form.append(sh.cell_value(tmp_row,4))

	TSs_name.append(sh.cell_value(tmp_row,6))
	TSs_abbr.append(sh.cell_value(tmp_row,7))
	TSs_form.append(sh.cell_value(tmp_row,8))

	prods_name.append(sh.cell_value(tmp_row,10))
	prods_abbr.append(sh.cell_value(tmp_row,11))
	prods_form.append(sh.cell_value(tmp_row,12))

print reacs_name
print TSs_name
print prods_name
print 'get reactions successfully!'

total = num_rows - 2 			#total number of reactions

###################
#extract data
###################

#definition of goal parameters
freq=[]						#frequencies
RSN = 0 					#external symmetry number
rots = []					#rotational constants
energy = 0.0				#CBS-QB3 (0 K)

#definetion of comparing pattern
pattern_freq = re.compile('^.*Frequencies -- *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)?$')
pattern_RSN = re.compile('^.*Rotational symmetry number *([0-9]+).*$')
pattern_rots = re.compile('^.*Rotational constants \(GHZ\): *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+)$')
pattern_energy = re.compile('^.*CBS-QB3 \(0 K\)= *(-?[0-9]+\.[0-9]+).*$')

#definition of counter
count = 0					#count the num of line maybe tell() could be useful you could have a try if needed

#definition of flags
freq_done = -1
RSN_done = -1
rots_done = -1
energy_done = -1


#definition of temporary variables
tmp_m = []		#match result 
tmp_name = ''	#the temporary name of the specie now
tmp_row = 3
tmp_blankline = ['blank']
tmp_index = 0
tmp_class = 1 	#1 for reactants 2 for products 3 for TSs
tmp_energies = []
tmp_barrier = 0.0
tmp_reverse_barrier = 0.0
#sh=wb.sheet_by_index(1)
#sh.put_cell(1,1,2,2,0)			#

#build a new workbook
wb_new = copy(wb)
sh=wb_new.get_sheet(1)				#if overwrite to use cell_overwrite_ok=True
sh.write(1,0,total)

allSpecies_name = reacs_name + tmp_blankline + prods_name + tmp_blankline + TSs_name
allSpecies_abbr = reacs_abbr + tmp_blankline + prods_abbr + tmp_blankline + TSs_abbr
allSpecies_form = reacs_form + tmp_blankline + prods_form + tmp_blankline + TSs_form

#extract info
for tmp_name in allSpecies_name:
	if tmp_name == 'blank':
		tmp_class += 1
		tmp_row += 1
		continue
	freqFile=file('freq/'+ tmp_name + '.log','r')

	#reset all variables
	freq=[]						
	RSN = 0 					
	rots = []					
	energy = 0.0				

	freq_done = -1
	RSN_done = -1
	rots_done = -1
	energy_done = -1

	for line in freqFile.readlines():
		if freq_done != 1:
			tmp_m = pattern_freq.match(line)
			if tmp_m:
				freq.extend(tmp_m.groups())
				freq_done = 0
			if freq_done == 0:
				if re.search('Thermochemistry',line):
					while None in freq:
						freq.remove(None)
					freq_done = 1
		else:
			if RSN_done != 1:
				tmp_m=pattern_RSN.match(line)
				if tmp_m:	
					RSN = tmp_m.group(1)
					RSN_done = 1
			else:
				tmp_m=pattern_rots.match(line)
				if tmp_m:
					rots.extend(tmp_m.groups())
					rots_done = 1
	freqFile.close()

	energyFile = file('energy/'+ tmp_name + '.log','r')
	for line in energyFile.readlines():
		if energy_done != 1:
			tmp_m = pattern_energy.match(line)
			if tmp_m:
				energy = tmp_m.group(1)
				energy_done = 1
	energyFile.close

	#write info
	tmp_index = tmp_row -3
	sh.write(tmp_row,0,1)
	sh.write(tmp_row,1,allSpecies_abbr[tmp_index])
	sh.write(tmp_row,2,allSpecies_name[tmp_index])
	sh.write(tmp_row,3,float(energy))
	sh.write(tmp_row,10,allSpecies_form[tmp_index])
	sh.write(tmp_row,11,float(rots[0]))
	sh.write(tmp_row,12,float(rots[1]))
	sh.write(tmp_row,13,float(rots[2]))
	sh.write(tmp_row,14,sqrt(float(rots[1])*float(rots[2])))
	sh.write(tmp_row,15,int(RSN))
	sh.write(tmp_row,16,allSpecies_name[tmp_index])
	
	tmp_energies.append(float(energy))

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
		tmp_barrier = float(energy) - tmp_energies[tmp_index - total * 2 - 2]
		sh.write(tmp_row,5,tmp_barrier)
		tmp_reverse_barrier = float(energy) - tmp_energies[tmp_index - total - 2]
		sh.write(tmp_row,6, tmp_reverse_barrier)
		sh.write(tmp_row,7,627.51*tmp_barrier)
		sh.write(tmp_row,8,627.51*tmp_reverse_barrier)
		sh.write(tmp_row,17,-float(freq[0]))
		freq.pop(0)
	else:
		sh.write(tmp_row,4,'Error')

	sh.write(tmp_row,18,len(freq))
	for i in range(len(freq)):
		sh.write(tmp_row,20+i,float(freq[i]))

	tmp_row += 1

wb_new.save('rate.xls')
print 'data extracted successfully!'


# THE END


