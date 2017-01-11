import xlrd
import re
import numpy as np
import os
import xlsxwriter

import phaseSpaceIntegral
import phys
import chem
import textExtractor

# constant
phys1 = phys.phys()
molecule1 = chem.molecule()
pattern_scanFileName = re.compile('^([CHO0-9]+_[0-9]+)_.*scan.*$')
pattern_geomFileName = re.compile('^([CHO0-9]+_[0-9]+)_.*opt.*$')
pattern_freqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')

# variables
temperature = [298.15] + range(300,2600,100)

# target variables
HR_dict = {}
mole_dict = {}

# read data and get integral

wbr = xlrd.open_workbook('HR_fit.xls')
sheetsName = [s.name for s in wbr.sheets()]
for tmp_sheetName in sheetsName:
	if re.match('.*_fit', tmp_sheetName):
		tmp_sheet = wbr.sheet_by_name(tmp_sheetName)
		num_rows = tmp_sheet.nrows
		for tmp_row in xrange(0, num_rows, 30):
			tmp_species = tmp_sheet.cell_value(tmp_row, 0)
			tmp_name = tmp_species
			tmp_m = pattern_scanFileName.match(tmp_species)
			if tmp_m:
				tmp_name = tmp_m.group(1)
				# print tmp_species
			else:
				print 'error', tmp_species
			tmp_rot = [int(tmp_sheet.cell_value(tmp_row+1, 2)), int(tmp_sheet.cell_value(tmp_row+1, 3)), tmp_sheet.cell_value(tmp_row+11, 1), tmp_sheet.cell_value(tmp_row+12, 1)]

			tmp_coeff_V = []
			i = 0
			while tmp_sheet.cell_value(tmp_row+20, 1+i) != '':
				tmp_coeff_V.append(float(tmp_sheet.cell_value(tmp_row+20, 1+i)))
				i += 1
			tmp_l = len(tmp_coeff_V)
			tmp_coeff_V.append(0.0)
			i = 0
			while tmp_sheet.cell_value(tmp_row+21, 2+i) != '':
				tmp_coeff_V.append(float(tmp_sheet.cell_value(tmp_row+21, 2+i)))
				i += 1
			if len(tmp_coeff_V) != 2*tmp_l:
				print 'Error! The length of cosine items does not equal to sine items'
			tmp_rot.append(tmp_coeff_V)

			tmp_integralDict = {}
			for tmp_T in temperature:
				tmp_integralResult = phaseSpaceIntegral.fourierPotentialInt(coeff_V=tmp_coeff_V, temperature=tmp_T, numSegment=300, zeroShift=True)
				tmp_integralDict[tmp_T] = tmp_integralResult
			tmp_rot.append(tmp_integralDict)

			# tmp_coeff_I = []
			# i = 0
			# while tmp_sheet.cell_value(tmp_row+22, 1+i) != '':
			# 	tmp_coeff_I.append(float(tmp_sheet.cell_value(tmp_row+22, 1+i)))
			# 	i += 1
			# tmp_rot.append(tmp_coeff_I)

			# tmp_integralResult = phaseSpaceIntegral.fourierPotentialInertiaInt(coeff_V=tmp_coeff_V, coeff_I=tmp_coeff_I, temperature=298.15, numSegment=300)
			# tmp_rot.append(tmp_integralResult)

			if tmp_name not in HR_dict.keys():
				HR_dict[tmp_name] = [tmp_rot]
			else:
				HR_dict[tmp_name].append(tmp_rot)

print len(HR_dict)

# read geom files
tmp_fileList = os.listdir('geom')
for tmp_file in tmp_fileList:
	tmp_m = pattern_geomFileName.match(tmp_file)
	if tmp_m:
		tmp_moleLabel = tmp_m.group(1)

		fr = file(os.path.join('geom', tmp_file), 'r')
		freqCom_done = -1
		standard_done = -1
		coordinate_done = -1
		tmp_lines = fr.readlines()		
		for (lineNum, tmp_line) in enumerate(tmp_lines):
			if freqCom_done != 1:
				if lineNum < len(tmp_lines) - 1:
					tmp2_line = tmp_lines[lineNum].strip() + tmp_lines[lineNum+1].strip()
					tmp_m = pattern_freqCom.match(tmp2_line)
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
						tmp_geom = tmp_lines[tmp_num: lineNum]
						coordinate_done = 1
		fr.close()

		mole_dict[tmp_moleLabel] = tmp_geom

print len(mole_dict)

# analyze all rotational potential integral
integral_dict = {}

# checklist = '''
# C6H14_5
# C7H16_4
# C7H16_5
# '''
# checkSpecies = checklist.strip()
# checkSpecies = checklist.split()

for tmp_species in HR_dict.keys():
# for tmp_species in checkSpecies:
	if tmp_species not in mole_dict.keys():
		print 'Error! ' + tmp_species + ' not found in mole_dict!'
		break
	molecule1.getLogGeom(mole_dict[tmp_species])
	molecule1.fulfillBonds()
	tmp_groups = molecule1.get1stOrderGroup()
	tmp_groupDict = {}
	for tmp_atom in molecule1.atoms:
		if tmp_atom.symbol != 'H':
			tmp_groupDict[tmp_atom.label] = tmp_groups.pop(0)
	if len(tmp_groups) != 0:
		print 'Error! The number of groups is larger than the number of non-H atoms!'
	for tmp_rot in HR_dict[tmp_species]:
		tmp_list = sorted([tmp_groupDict[tmp_rot[0]], tmp_groupDict[tmp_rot[1]]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		tmp_integralResult = tmp_rot[5][298.15]
		if tmp_text in integral_dict.keys():
			integral_dict[tmp_text].append(tmp_integralResult)
		else:
			integral_dict[tmp_text] = [tmp_integralResult]

print integral_dict.keys()
for tmp_rot in integral_dict.keys():
	# print tmp_rot
	integrals = np.array(integral_dict[tmp_rot])
	# integrals = phys1.JoulTocal(phys1.R)*np.log(integrals)
	print '\'' + tmp_rot + '\':' + str(np.mean(integrals)) + ','
	# print np.std(integrals)


# write to excel
wbw = xlsxwriter.Workbook('1DHRIntegral.xlsx')
shw = wbw.add_worksheet('Integral')

tmp_row = 0
tmp_col = 0
shw.write(tmp_row, tmp_col, 'Name Abbreviation')
shw.write(tmp_row, tmp_col+1, 'Name')
shw.write(tmp_row, tmp_col+2, 'Formula')
shw.write(tmp_row, tmp_col+3, 'Geometry')
shw.write(tmp_row, tmp_col+4, 'Rotation')
shw.write(tmp_row, tmp_col+5, 'Rotation atom 1')
shw.write(tmp_row, tmp_col+6, 'Rotation atom 2')
shw.write(tmp_row, tmp_col+7, 'Temperature')

tmp_row += 1
tmp_col += 7
for i in xrange(len(temperature)):
	shw.write(tmp_row, tmp_col+i, temperature[i])

tmp_row +=1
tmp_col = 0
all_species = sorted(HR_dict.keys(), cmp=molecule1.moleFormulaCmp)
for tmp_species in all_species:
	if tmp_species not in mole_dict.keys():
		print 'Error! ' + tmp_species + ' not found in mole_dict!'
		break
	molecule1.getLogGeom(mole_dict[tmp_species])
	molecule1.fulfillBonds()
	molecule1.calcFormula()
	tmp_groups = molecule1.get1stOrderGroup()
	tmp_groupDict = {}
	for tmp_atom in molecule1.atoms:
		if tmp_atom.symbol != 'H':
			tmp_groupDict[tmp_atom.label] = tmp_groups.pop(0)
	if len(tmp_groups) != 0:
		print 'Error! The number of groups is larger than the number of non-H atoms!'
	shw.write(tmp_row, tmp_col, tmp_species)
	shw.write(tmp_row, tmp_col+1, tmp_species)
	shw.write(tmp_row, tmp_col+2, molecule1.formula)
	shw.write(tmp_row, tmp_col+3, textExtractor.geometryExtractor(mole_dict[tmp_species]).replace('\t','    '))
	for tmp_rot in HR_dict[tmp_species]:
		tmp_list = sorted([tmp_groupDict[tmp_rot[0]], tmp_groupDict[tmp_rot[1]]])
		tmp_rotText = tmp_list[0] + '-' + tmp_list[1]
		shw.write(tmp_row, tmp_col+4, tmp_rotText)
		shw.write(tmp_row, tmp_col+5, tmp_rot[0])
		shw.write(tmp_row, tmp_col+6, tmp_rot[1])
		for (i, tmp_T) in enumerate(temperature):
			shw.write(tmp_row, tmp_col+7+i, tmp_rot[5][tmp_T])
		tmp_row += 1

wbw.close()





