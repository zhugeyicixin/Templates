# this is used to generate database for group additivity method
from xlwt import *
import os
import re
import xlsxwriter

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
		elif tmp_line == 'M062X/def2TZVP//B3LYP/6-31G(d)':
			__energy__ = 'M062X/def2TZVP//B3LYP/6-31G(d)'
			print '\n-------------------------------------\nM062X energy and b3lyp geom are used in this calculation\n-------------------------------------\n'	
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
optEnergy = []
optZPE = []
optEnthalpy = []
SPEnergy = []				#CBS-QB3 (0 K)

#definetion of comparing pattern
pattern_logFile = re.compile('^(C[0-9]*H[0-9OH]*_*[0-9]*_r[0-9]+_[CO0-9]+).*\.log|(C[0-9]*H[0-9OH]*_*[0-9]*).*\.log$')
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
# if __energy__ == 'cbs':
# 	pattern_energy = re.compile('^.*CBS-QB3 \(0 K\)= *(-?[0-9]+\.[0-9]+).*$')
# else:
# 	pattern_energy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')

pattern_optEnergy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
pattern_optZPE = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_optEnthalpy = re.compile('^.*Sum of electronic and thermal Enthalpies= *(-?[0-9]+\.[0-9]+).*$')
pattern_SPEnergy = re.compile('^.*SCF Done:  E\([RU]M062X\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
# pattern_SPEnergy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')

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
optEnergy_done = -1
optZPE_done = -1
optEnthalpy_done = -1
SPEnergy_done = -1

#definition of temporary variables
tmp_m = []		#match result 
tmp_num = 0
tmp_hessian = ''

#extract info
pwd = os.getcwd()
tmp_fileLists = os.listdir(os.path.join(pwd, 'freq'))

for tmp_file in tmp_fileLists:
	print tmp_file
	tmp_m = pattern_logFile.match(tmp_file)
	if tmp_m:
		if tmp_m.group(1) != None:
			tmp_name = tmp_m.group(1)
		else:
			tmp_name = tmp_m.group(2)
		freqFile = file(os.path.join('freq', tmp_file), 'r')

		#reset all variables		
		multi_done = -1
		freqCom_done = -1
		standard_done = -1
		coordinate_done = -1
		RSN_done = -1
		freqSum_done = -1
		optEnergy_done = -1
		optZPE_done = -1
		optEnthalpy_done = -1
		SPEnergy_done = -1

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
			elif optEnergy_done != 1:
				tmp_m = pattern_optEnergy.match(tmp_line)
				if tmp_m:
					optEnergy.append(float(tmp_m.group(1)))
					optEnergy_done = 1
			elif RSN_done != 1:
				tmp_m = pattern_RSN.match(tmp_line)
				if tmp_m:	
					RSN.append(int(tmp_m.group(1)))
					RSN_done = 1
			elif optZPE_done != 1:
				tmp_m = pattern_optZPE.match(tmp_line)
				if tmp_m:
					optZPE.append(float(tmp_m.group(1)))
					optZPE_done = 1
			elif optEnthalpy_done != 1:
				tmp_m = pattern_optEnthalpy.match(tmp_line)
				if tmp_m:
					optEnthalpy.append(float(tmp_m.group(1)))
					optEnthalpy_done = 1
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

		energyFile = file(os.path.join('energy', tmp_name+'_3_opt_M06.log'),'r')
		# energyFile = file(os.path.join('energy', tmp_file),'r')
		for tmp_line in energyFile.readlines():
			if cbs_done != 1:
				if tmp_line == tmp_lines[-1]:
					print 'Error! ' + tmp_file + 'not cbs freq file'
				tmp_m = pattern_cbs.match(tmp_line)
				if tmp_m:
					cbs_done = 1
			elif SPEnergy_done != 1:
				tmp_m = pattern_SPEnergy.match(tmp_line)
				if tmp_m:
					tmp_energy = float(tmp_m.group(1))
		SPEnergy.append(tmp_energy)
		SPEnergy_done = 1
		if SPEnergy_done != 1:
			print tmp_file
		energyFile.close()

		tmp_mole = chem.molecule()
		tmp_mole.getLogGeom(geom[-1])
		tmp_mole.calcFormula()
		formula.append(tmp_mole.formula)
		atomsNum.append(tmp_mole.getAtomsNum())

		name.append(tmp_name)
		speciesNum += 1

###########################################
# write info to excel
###########################################
wb = xlsxwriter.Workbook('database.xlsx')
sh = wb.add_worksheet('speciesInfo')

tmp_row = 0
tmp_col = 0

sh.write(tmp_row, tmp_col, 'Name Abbreviation')
sh.write(tmp_row, tmp_col+1, 'Name')
sh.write(tmp_row, tmp_col+2, 'Formula')
sh.write(tmp_row, tmp_col+3, 'Atoms Number')
sh.write(tmp_row, tmp_col+4, 'SCF Energy in freq')
sh.write(tmp_row, tmp_col+5, 'ZPE Energy in freq')
sh.write(tmp_row, tmp_col+6, 'Enthalpy in freq')
sh.write(tmp_row, tmp_col+7, 'SP Energy in energy')
sh.write(tmp_row, tmp_col+8, 'SP Energy (0 K) in energy corrected with freq scaling factor')
sh.write(tmp_row, tmp_col+9, 'SP Enthalpy (298.15 K) in energy corrected with freq scaling factor')
sh.write(tmp_row, tmp_col+10, 'Multiplicity')
sh.write(tmp_row, tmp_col+11, 'External Symmetry Number')
sh.write(tmp_row, tmp_col+12, 'Geometry')

tmp_row = 1
tmp_col = 0
for i in xrange(speciesNum):
	sh.write(tmp_row, tmp_col, name[i])
	sh.write(tmp_row, tmp_col+1, name[i])
	sh.write(tmp_row, tmp_col+2, formula[i])
	sh.write(tmp_row, tmp_col+3, atomsNum[i])
	sh.write(tmp_row, tmp_col+4, optEnergy[i])
	sh.write(tmp_row, tmp_col+5, optZPE[i])
	sh.write(tmp_row, tmp_col+6, optEnthalpy[i])
	sh.write(tmp_row, tmp_col+7, SPEnergy[i])
	# ZPE scaling factor from Truhlar used here
	sh.write(tmp_row, tmp_col+8, SPEnergy[i] + (optZPE[i]-optEnergy[i])*0.977)
	sh.write(tmp_row, tmp_col+9, SPEnergy[i] + (optZPE[i]-optEnergy[i])*0.977 + optEnthalpy[i]-optZPE[i])
	sh.write(tmp_row, tmp_col+10, multi[i])
	sh.write(tmp_row, tmp_col+11, RSN[i])
	sh.write(tmp_row, tmp_col+12, textExtractor.geometryExtractor(geom[i]).replace('\t','    '))
	tmp_row += 1

wb.close()

