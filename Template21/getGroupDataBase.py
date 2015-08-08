# this is used to generate database for group additivity method
from xlwt import *
import os
import re

import textExtractor
import chem

###########################################
# extract geometry and energy form log file
###########################################
# get commands from .name file
__energy__ = 'b3lyp'
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[3].strip(' \n')
		if tmp_line == 'cbs':
			__energy__ = 'cbs'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs freq and energy are used in this calculation\n-------------------------------------\n'
		elif re.match('b3lyp', (tmp_line.strip()).lower()) != None:
			__energy__ = 'b3lyp'
			print '\n-------------------------------------\nb3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'cbsb3lyp':
			__energy__ = 'cbsb3lyp'
			print '\n-------------------------------------\ncbs verified and b3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'
		fr.close()	


#definition of goal parameters
name = []
multi = []
geom = []
RSN = [] 					#external symmetry number
formula = []
atomsNum = []
energy = []				#CBS-QB3 (0 K)

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
speciesNum = 0		#	this is the total number of species in the database

#definition of flags
cbs_done = -1
multi_done = -1
freqCom_done = -1
standard_done = -1
coordinate_done = -1
RSN_done = -1
freqSum_done = -1
energy_done = -1

#definition of temporary variables
tmp_m = []		#match result 
tmp_num = 0
tmp_hessian = ''

#extract info
pwd = os.getcwd()
tmp_fileLists = os.listdir(os.path.join(pwd, 'freq'))

for tmp_file in tmp_fileLists:
	freqFile = file(os.path.join('freq', tmp_file), 'r')

	#reset all variables		
	multi_done = -1
	freqCom_done = -1
	standard_done = -1
	coordinate_done = -1
	RSN_done = -1
	freqSum_done = -1
	energy_done = -1

	# only if __energy__ == 'cbs', then check whether the freq file is cbs file 
	# if __energy__ == 'cbs':
	if 'cbs' in __energy__:	
		cbs_done = -1
	else:
		cbs_done = 1

	tmp_lines = freqFile.readlines()
	for (lineNum, tmp_line) in enumerate(tmp_lines):
		if cbs_done != 1:
			if lineNum == len(tmp_lines)-1:
				print 'Error! ' + tmp_file + 'not cbs freq file'
			tmp_m = pattern_cbs.match(tmp_line)
			if tmp_m:
				cbs_done = 1
		elif multi_done != 1:
			tmp_m = pattern_multi.match(tmp_line)
			if tmp_m:
				multi.append(int(tmp_m.group(1)))
				multi_done = 1
		elif freqCom_done != 1:
			if lineNum < len(tmp_lines)-1:
				tmp_line = tmp_lines[lineNum].strip() + tmp_lines[lineNum+1].strip()
				tmp_m = pattern_freqCom.match(tmp_line)
				if tmp_m:
					freqCom_done = 1
		elif standard_done != 1:
			tmp_m = pattern_standard.match(tmp_line)
			if tmp_m:
				tmp_num = lineNum + 5
				standard_done = 1
		elif coordinate_done != 1:
			tmp_m = pattern_endline.match(tmp_line)
			if tmp_m:
				if lineNum > tmp_num:
					geom.append(tmp_lines[tmp_num: lineNum])
					coordinate_done = 1
		elif RSN_done != 1:
			tmp_m=pattern_RSN.match(tmp_line)
			if tmp_m:	
				RSN.append(int(tmp_m.group(1)))
				RSN_done = 1
		elif freqSum_done != 1:
			if freqSum_done < 0:
				tmp_m = pattern_freqSum.match(tmp_line)
				if tmp_m:
					freqSum_done = 0
					tmp_num = lineNum
			elif tmp_line != '\n':
				continue
			else:
				tmp_hessian = textExtractor.hessianExtractor(tmp_lines[tmp_num:lineNum])
				if len(tmp_hessian) != ((3*len(geom[-1]))*(3*len(geom[-1])+1)/2):
					print 'Error! The size of hessian matrix does not equal to 3*N!'
				freqSum_done = 1
				break							
	freqFile.close()

	if 'cbs' in __energy__:	
		cbs_done = -1
	else:
		cbs_done = 1

	energyFile = file(os.path.join('energy', tmp_file),'r')
	for tmp_line in energyFile.readlines():
		if cbs_done != 1:
			if tmp_line == tmp_lines[-1]:
				print 'Error! ' + tmp_file + 'not cbs freq file'
			tmp_m = pattern_cbs.match(tmp_line)
			if tmp_m:
				cbs_done = 1
		elif energy_done != 1:
			tmp_m = pattern_energy.match(tmp_line)
			if tmp_m:
				energy.append(float(tmp_m.group(1)))
				energy_done = 1
	energyFile.close()

	tmp_mole = chem.molecule()
	tmp_mole.getLogGeom(geom[-1])
	tmp_mole.calcFormula()
	formula.append(tmp_mole.formula)
	atomsNum.append(tmp_mole.getAtomsNum())

	name.append(tmp_file[0:-4])
	speciesNum += 1


###########################################
# write info to excel
###########################################
wb = Workbook()
sh = wb.add_sheet('speciesInfo')
sh.cell_overwrite_ok = True

tmp_row = 0
tmp_col = 0

sh.write(tmp_row, tmp_col, 'Name Abbreviation')
sh.write(tmp_row, tmp_col+1, 'Name')
sh.write(tmp_row, tmp_col+2, 'Formula')
sh.write(tmp_row, tmp_col+3, 'Atoms Number')
sh.write(tmp_row, tmp_col+4, 'Energy')
sh.write(tmp_row, tmp_col+5, 'Multiplicity')
sh.write(tmp_row, tmp_col+6, 'External Symmetry Number')
sh.write(tmp_row, tmp_col+7, 'Geometry')

tmp_row = 1
tmp_col = 0
for i in xrange(speciesNum):
	sh.write(tmp_row, tmp_col, name[i])
	sh.write(tmp_row, tmp_col+1, name[i])
	sh.write(tmp_row, tmp_col+2, formula[i])
	sh.write(tmp_row, tmp_col+3, atomsNum[i])
	sh.write(tmp_row, tmp_col+4, energy[i])
	sh.write(tmp_row, tmp_col+5, multi[i])
	sh.write(tmp_row, tmp_col+6, RSN[i])
	sh.write(tmp_row, tmp_col+7, textExtractor.geometryExtractor(geom[i]).replace('\t','    '))
	tmp_row += 1

wb.save('database.xls')

