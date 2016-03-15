# this is used to get group additivity input files
import re
import os 
import time
import numpy as np
import xlsxwriter
import xlrd

import chem
import thermoDatabase

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
			__energy__ = 'CBS-QB3'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs freq and energy are used in this calculation\n-------------------------------------\n'
		elif re.match('b3lyp', (tmp_line.strip()).lower()) != None:
			__energy__ = tmp_line.strip()
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

#####################################################################
# read data from the database excel file and generate input file
#####################################################################
wb=xlrd.open_workbook('database.xlsx')
sh=wb.sheet_by_name('speciesInfo')

# definition of variables
all_moles = []
all_groups = set()
groupIndex = {}

# definition of t emporary variables
tmp_name = ''
tmp_energy = 0.0
tmp_geom = ''
num_rows = sh.nrows
num_cols = sh.ncols
tmp_groups = []

# read info from database
for tmp_row in xrange(1, num_rows):
	tmp_groups = []
	tmp_mole = chem.molecule()

	tmp_name = sh.cell_value(tmp_row, 0)
	tmp_formula = sh.cell_value(tmp_row, 2)
	tmp_energy = sh.cell_value(tmp_row, 9)
	tmp_geom = sh.cell_value(tmp_row, 12)
	tmp_geom = tmp_geom.strip()
	tmp_geom = tmp_geom.split('\n')
	tmp_mole.getGjfGeom(tmp_geom)
	tmp_mole.setLabel(tmp_name)
	tmp_mole.fulfillBonds()

	# update the energy as enthalpy of formation at 298.15 K
	tmp_mole.calcFormula()
	if tmp_formula != tmp_mole.formula:
		print 'Error! The formula in the database is difference from the geometry!'
	# note that the refEnthalpy0 used here is not real refEnthalpy0, but refEnthalpy298, thus H298mH0 = 0.0
	tmp_energy = thermoDatabase.getFormationH(formula = tmp_formula, refQMMethod = __energy__, refEnthalpy0 = tmp_energy, H298mH0 = 0.0)
	# tmp_energy = thermoDatabase.getEnthalpyDifference(formula = tmp_formula, refQMMethod = __energy__, refEnthalpy0 = tmp_energy, H298mH0 = 0.0)
	# tmp_energy = thermoDatabase.getAtomizationEnergy(formula = tmp_formula, refQMMethod = __energy__, refEnergy0 = tmp_energy)
	# note that this is not real ZPE, but reference energy 
	# currently tmp_energy is the entaly of formation at 298.15 K
	tmp_mole.setZPE(tmp_energy)

	tmp_groups = tmp_mole.get1stOrderGroup()
	all_moles.append(tmp_mole)
	all_groups = all_groups | set(tmp_groups)

# # generate input file
# # method 1
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)
# wb2 = xlsxwriter.Workbook('inputFile_1.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

# tmp2_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh2.write(tmp2_row, tmp2_col, tmp_text)
# 		groupIndex[tmp_text] = tmp2_col
# 		tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

# tmp3_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh3.write(tmp3_row, tmp3_col, tmp_text)
# 		groupIndex[tmp_text] = tmp3_col
# 		tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

# tmp4_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh4.write(tmp4_row, tmp4_col, tmp_text)
# 		groupIndex[tmp_text] = tmp4_col
# 		tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for i in xrange(n):
# 	for j in xrange(N*(N+3)/2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector1()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)		
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# vectorGroups = []
# vectorMole = []
# acyclicVecIndex = []
# cyclicVecIndex = []

# wb3 = xlsxwriter.Workbook('inputFile_m1.xlsx')
# sh5 = wb3.add_worksheet('inputVectors')
# sh6 = wb3.add_worksheet('acyclic')
# sh7 = wb3.add_worksheet('cyclic')

# tmp5_row = 0
# tmp5_col = 0
# sh5.write(tmp5_row, tmp5_col, 'ID')
# sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
# sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

# tmp5_row = 1
# sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

# tmp5_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh5.write(tmp5_row, tmp5_col+i, i+1)

# tmp5_row = 2 
# for i in xrange(N):
# 	sh5.write(tmp5_row, tmp5_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp5_col
# 	tmp5_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_text)
# 		groupIndex[tmp_text] = tmp5_col
# 		tmp5_col += 1

# sh5.write(tmp5_row, tmp5_col+2, 'Name')
# sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

# tmp6_row = 0
# tmp6_col = 0
# sh6.write(tmp6_row, tmp6_col, 'ID')
# sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
# sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

# tmp6_row = 1
# sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

# tmp6_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh6.write(tmp6_row, tmp6_col+i, i+1)

# tmp6_row = 2 
# for i in xrange(N):
# 	sh6.write(tmp6_row, tmp6_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp6_col
# 	tmp6_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh6.write(tmp6_row, tmp6_col, tmp_text)
# 		groupIndex[tmp_text] = tmp6_col
# 		tmp6_col += 1

# sh6.write(tmp6_row, tmp6_col+2, 'Name')
# sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

# tmp7_row = 0
# tmp7_col = 0
# sh7.write(tmp7_row, tmp7_col, 'ID')
# sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
# sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

# tmp7_row = 1
# sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

# tmp7_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh7.write(tmp7_row, tmp7_col+i, i+1)

# tmp7_row = 2 
# for i in xrange(N):
# 	sh7.write(tmp7_row, tmp7_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp7_col
# 	tmp7_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh7.write(tmp7_row, tmp7_col, tmp_text)
# 		groupIndex[tmp_text] = tmp7_col
# 		tmp7_col += 1

# sh7.write(tmp7_row, tmp7_col, 'CycleSize')
# sh7.write(tmp7_row, tmp7_col+2, 'Name')
# sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

# tmp5_row = 3
# tmp5_col = 0
# tmp6_row = 3
# tmp6_col = 0
# tmp7_row = 3
# tmp7_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	tmp_groupVector = tmp_mole.getGroupVector1()
	
# 	flag_exsit = 0
# 	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
# 		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
# 			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
# 			if max(abs(tmp_diff)) < 1e-5:			
# 				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
# 				flag_exsit = 1
# 	if flag_exsit == 0:
# 		vectorGroups.append(tmp_groupVector)
# 		vectorMole.append({})
# 		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
# 		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
# 		for j in xrange(N*(N+3)/2):
# 			sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 		if not tmp_mole.existRings():
# 			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			acyclicVecIndex.append(len(vectorGroups))
# 			tmp6_row += 1
# 		else:
# 			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 			cyclicVecIndex.append(len(vectorGroups))
# 			tmp7_row += 1
		
# 		tmp5_row += 1

# tmp5_row = 3
# tmp6_row = 3
# tmp7_row = 3
# for i in xrange(len(vectorGroups)):
# 	tmp5_col = N*(N+3)/2 + 7
# 	tmp6_col = N*(N+3)/2 + 7
# 	tmp7_col = N*(N+3)/2 + 7

# 	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
# 	for tmp_item in tmp_list:
# 		# print tmp5_col, tmp_item[0], tmp_item[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
# 		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
# 		tmp5_col += 2
# 	if (i+1) in acyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
# 			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
# 			tmp6_col += 2 
# 		tmp6_row += 1
# 	elif (i+1) in cyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
# 			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
# 			tmp7_col += 2
# 		tmp7_row += 1
# 	else:
# 		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

# 	tmp5_row += 1

# wb3.close()


# # generate input file
# # method 2
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_2.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

# tmp2_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh2.write(tmp2_row, tmp2_col, tmp_text)
# 		groupIndex[tmp_text] = tmp2_col
# 		tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

# tmp3_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh3.write(tmp3_row, tmp3_col, tmp_text)
# 		groupIndex[tmp_text] = tmp3_col
# 		tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

# tmp4_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh4.write(tmp4_row, tmp4_col, tmp_text)
# 		groupIndex[tmp_text] = tmp4_col
# 		tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for i in xrange(n):
# 	for j in xrange(N*(N+3)/2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector2()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# vectorGroups = []
# vectorMole = []
# acyclicVecIndex = []
# cyclicVecIndex = []

# wb3 = xlsxwriter.Workbook('inputFile_m2.xlsx')
# sh5 = wb3.add_worksheet('inputVectors')
# sh6 = wb3.add_worksheet('acyclic')
# sh7 = wb3.add_worksheet('cyclic')

# tmp5_row = 0
# tmp5_col = 0
# sh5.write(tmp5_row, tmp5_col, 'ID')
# sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
# sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

# tmp5_row = 1
# sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

# tmp5_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh5.write(tmp5_row, tmp5_col+i, i+1)

# tmp5_row = 2 
# for i in xrange(N):
# 	sh5.write(tmp5_row, tmp5_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp5_col
# 	tmp5_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_text)
# 		groupIndex[tmp_text] = tmp5_col
# 		tmp5_col += 1

# sh5.write(tmp5_row, tmp5_col+2, 'Name')
# sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

# tmp6_row = 0
# tmp6_col = 0
# sh6.write(tmp6_row, tmp6_col, 'ID')
# sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
# sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

# tmp6_row = 1
# sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

# tmp6_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh6.write(tmp6_row, tmp6_col+i, i+1)

# tmp6_row = 2 
# for i in xrange(N):
# 	sh6.write(tmp6_row, tmp6_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp6_col
# 	tmp6_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh6.write(tmp6_row, tmp6_col, tmp_text)
# 		groupIndex[tmp_text] = tmp6_col
# 		tmp6_col += 1

# sh6.write(tmp6_row, tmp6_col+2, 'Name')
# sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

# tmp7_row = 0
# tmp7_col = 0
# sh7.write(tmp7_row, tmp7_col, 'ID')
# sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
# sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

# tmp7_row = 1
# sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

# tmp7_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh7.write(tmp7_row, tmp7_col+i, i+1)

# tmp7_row = 2 
# for i in xrange(N):
# 	sh7.write(tmp7_row, tmp7_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp7_col
# 	tmp7_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh7.write(tmp7_row, tmp7_col, tmp_text)
# 		groupIndex[tmp_text] = tmp7_col
# 		tmp7_col += 1
# sh7.write(tmp7_row, tmp7_col, 'CycleSize')
# sh7.write(tmp7_row, tmp7_col+2, 'Name')
# sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

# tmp5_row = 3
# tmp5_col = 0
# tmp6_row = 3
# tmp6_col = 0
# tmp7_row = 3
# tmp7_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	tmp_groupVector = tmp_mole.getGroupVector2()
	
# 	flag_exsit = 0
# 	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
# 		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
# 			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
# 			if max(abs(tmp_diff)) < 1e-5:			
# 				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
# 				flag_exsit = 1
# 	if flag_exsit == 0:
# 		vectorGroups.append(tmp_groupVector)
# 		vectorMole.append({})
# 		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
# 		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
# 		for j in xrange(N*(N+3)/2):
# 				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 		if not tmp_mole.existRings():
# 			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			acyclicVecIndex.append(len(vectorGroups))
# 			tmp6_row += 1
# 		else:
# 			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 			cyclicVecIndex.append(len(vectorGroups))
# 			tmp7_row += 1
		
# 		tmp5_row += 1

# tmp5_row = 3
# tmp6_row = 3
# tmp7_row = 3
# for i in xrange(len(vectorGroups)):
# 	tmp5_col = N*(N+3)/2 + 7
# 	tmp6_col = N*(N+3)/2 + 7
# 	tmp7_col = N*(N+3)/2 + 7

# 	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
# 	for tmp_item in tmp_list:
# 		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
# 		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
# 		tmp5_col += 2
# 	if (i+1) in acyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
# 			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
# 			tmp6_col += 2
# 		tmp6_row += 1
# 	elif (i+1) in cyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
# 			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
# 			tmp7_col += 2
# 		tmp7_row += 1
# 	else:
# 		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

# 	tmp5_row += 1

# wb3.close()

# # generate input file
# # method 3
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_3.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*2)

# tmp2_col = 5
# for i in xrange(N*2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	


# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh2.write(tmp2_row, tmp2_col, tmp_text)
# 	groupIndex[tmp_text] = tmp2_col
# 	tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*2)

# tmp3_col = 5
# for i in xrange(N*2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	


# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh3.write(tmp3_row, tmp3_col, tmp_text)
# 	groupIndex[tmp_text] = tmp3_col
# 	tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*2)

# tmp4_col = 5
# for i in xrange(N*2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh4.write(tmp4_row, tmp4_col, tmp_text)
# 	groupIndex[tmp_text] = tmp4_col
# 	tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# for i in xrange(n):
# 	for j in xrange(N*2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector3()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()


# # generate input file
# # method 4
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_4.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*2)

# tmp2_col = 5
# for i in xrange(N*2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh2.write(tmp2_row, tmp2_col, tmp_text)
# 	groupIndex[tmp_text] = tmp2_col
# 	tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*2)

# tmp3_col = 5
# for i in xrange(N*2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	


# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh3.write(tmp3_row, tmp3_col, tmp_text)
# 	groupIndex[tmp_text] = tmp3_col
# 	tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*2)

# tmp4_col = 5
# for i in xrange(N*2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	


# for i in xrange(N):
# 	tmp_text = all_groups[i] + ' - other Groups'
# 	sh4.write(tmp4_row, tmp4_col, tmp_text)
# 	groupIndex[tmp_text] = tmp4_col
# 	tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# for i in xrange(n):
# 	for j in xrange(N*2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector4()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# # generate input file
# # method 5
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_5.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

# tmp2_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh2.write(tmp2_row, tmp2_col, tmp_text)
# 		groupIndex[tmp_text] = tmp2_col
# 		tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

# tmp3_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh3.write(tmp3_row, tmp3_col, tmp_text)
# 		groupIndex[tmp_text] = tmp3_col
# 		tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

# tmp4_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh4.write(tmp4_row, tmp4_col, tmp_text)
# 		groupIndex[tmp_text] = tmp4_col
# 		tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# for i in xrange(n):
# 	for j in xrange(N*(N+3)/2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector5()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# vectorGroups = []
# vectorMole = []
# acyclicVecIndex = []
# cyclicVecIndex = []

# wb3 = xlsxwriter.Workbook('inputFile_m5.xlsx')
# sh5 = wb3.add_worksheet('inputVectors')
# sh6 = wb3.add_worksheet('acyclic')
# sh7 = wb3.add_worksheet('cyclic')

# tmp5_row = 0
# tmp5_col = 0
# sh5.write(tmp5_row, tmp5_col, 'ID')
# sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
# sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

# tmp5_row = 1
# sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

# tmp5_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh5.write(tmp5_row, tmp5_col+i, i+1)

# tmp5_row = 2 
# for i in xrange(N):
# 	sh5.write(tmp5_row, tmp5_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp5_col
# 	tmp5_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_text)
# 		groupIndex[tmp_text] = tmp5_col
# 		tmp5_col += 1

# sh5.write(tmp5_row, tmp5_col+2, 'Name')
# sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

# tmp6_row = 0
# tmp6_col = 0
# sh6.write(tmp6_row, tmp6_col, 'ID')
# sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
# sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

# tmp6_row = 1
# sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

# tmp6_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh6.write(tmp6_row, tmp6_col+i, i+1)

# tmp6_row = 2 
# for i in xrange(N):
# 	sh6.write(tmp6_row, tmp6_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp6_col
# 	tmp6_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh6.write(tmp6_row, tmp6_col, tmp_text)
# 		groupIndex[tmp_text] = tmp6_col
# 		tmp6_col += 1

# sh6.write(tmp6_row, tmp6_col+2, 'Name')
# sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

# tmp7_row = 0
# tmp7_col = 0
# sh7.write(tmp7_row, tmp7_col, 'ID')
# sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
# sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

# tmp7_row = 1
# sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

# tmp7_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh7.write(tmp7_row, tmp7_col+i, i+1)

# tmp7_row = 2 
# for i in xrange(N):
# 	sh7.write(tmp7_row, tmp7_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp7_col
# 	tmp7_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh7.write(tmp7_row, tmp7_col, tmp_text)
# 		groupIndex[tmp_text] = tmp7_col
# 		tmp7_col += 1
# sh7.write(tmp7_row, tmp7_col, 'CycleSize')
# sh7.write(tmp7_row, tmp7_col+2, 'Name')
# sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

# tmp5_row = 3
# tmp5_col = 0
# tmp6_row = 3
# tmp6_col = 0
# tmp7_row = 3
# tmp7_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	tmp_groupVector = tmp_mole.getGroupVector5()
	
# 	flag_exsit = 0
# 	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
# 		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
# 			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
# 			if max(abs(tmp_diff)) < 1e-5:			
# 				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
# 				flag_exsit = 1
# 	if flag_exsit == 0:
# 		vectorGroups.append(tmp_groupVector)
# 		vectorMole.append({})
# 		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
# 		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
# 		for j in xrange(N*(N+3)/2):
# 				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 		if not tmp_mole.existRings():
# 			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			acyclicVecIndex.append(len(vectorGroups))
# 			tmp6_row += 1
# 		else:
# 			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 			cyclicVecIndex.append(len(vectorGroups))
# 			tmp7_row += 1
		
# 		tmp5_row += 1

# tmp5_row = 3
# tmp6_row = 3
# tmp7_row = 3
# for i in xrange(len(vectorGroups)):
# 	tmp5_col = N*(N+3)/2 + 7
# 	tmp6_col = N*(N+3)/2 + 7
# 	tmp7_col = N*(N+3)/2 + 7

# 	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
# 	for tmp_item in tmp_list:
# 		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
# 		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
# 		tmp5_col += 2
# 	if (i+1) in acyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
# 			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
# 			tmp6_col += 2
# 		tmp6_row += 1
# 	elif (i+1) in cyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
# 			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
# 			tmp7_col += 2
# 		tmp7_row += 1
# 	else:
# 		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

# 	tmp5_row += 1

# wb3.close()

# # generate input file
# # method 6
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_6.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

# tmp2_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh2.write(tmp2_row, tmp2_col, tmp_text)
# 		groupIndex[tmp_text] = tmp2_col
# 		tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

# tmp3_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh3.write(tmp3_row, tmp3_col, tmp_text)
# 		groupIndex[tmp_text] = tmp3_col
# 		tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

# tmp4_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh4.write(tmp4_row, tmp4_col, tmp_text)
# 		groupIndex[tmp_text] = tmp4_col
# 		tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for i in xrange(n):
# 	for j in xrange(N*(N+3)/2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector6()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# vectorGroups = []
# vectorMole = []
# acyclicVecIndex = []
# cyclicVecIndex = []

# wb3 = xlsxwriter.Workbook('inputFile_m6.xlsx')
# sh5 = wb3.add_worksheet('inputVectors')
# sh6 = wb3.add_worksheet('acyclic')
# sh7 = wb3.add_worksheet('cyclic')

# tmp5_row = 0
# tmp5_col = 0
# sh5.write(tmp5_row, tmp5_col, 'ID')
# sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
# sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

# tmp5_row = 1
# sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

# tmp5_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh5.write(tmp5_row, tmp5_col+i, i+1)

# tmp5_row = 2 
# for i in xrange(N):
# 	sh5.write(tmp5_row, tmp5_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp5_col
# 	tmp5_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_text)
# 		groupIndex[tmp_text] = tmp5_col
# 		tmp5_col += 1

# sh5.write(tmp5_row, tmp5_col+2, 'Name')
# sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

# tmp6_row = 0
# tmp6_col = 0
# sh6.write(tmp6_row, tmp6_col, 'ID')
# sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
# sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

# tmp6_row = 1
# sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

# tmp6_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh6.write(tmp6_row, tmp6_col+i, i+1)

# tmp6_row = 2 
# for i in xrange(N):
# 	sh6.write(tmp6_row, tmp6_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp6_col
# 	tmp6_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh6.write(tmp6_row, tmp6_col, tmp_text)
# 		groupIndex[tmp_text] = tmp6_col
# 		tmp6_col += 1

# sh6.write(tmp6_row, tmp6_col+2, 'Name')
# sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

# tmp7_row = 0
# tmp7_col = 0
# sh7.write(tmp7_row, tmp7_col, 'ID')
# sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
# sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

# tmp7_row = 1
# sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

# tmp7_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh7.write(tmp7_row, tmp7_col+i, i+1)

# tmp7_row = 2 
# for i in xrange(N):
# 	sh7.write(tmp7_row, tmp7_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp7_col
# 	tmp7_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh7.write(tmp7_row, tmp7_col, tmp_text)
# 		groupIndex[tmp_text] = tmp7_col
# 		tmp7_col += 1
# sh7.write(tmp7_row, tmp7_col, 'CycleSize')
# sh7.write(tmp7_row, tmp7_col+2, 'Name')
# sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

# tmp5_row = 3
# tmp5_col = 0
# tmp6_row = 3
# tmp6_col = 0
# tmp7_row = 3
# tmp7_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	tmp_groupVector = tmp_mole.getGroupVector6()
	
# 	flag_exsit = 0
# 	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
# 		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
# 			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
# 			if max(abs(tmp_diff)) < 1e-5:			
# 				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
# 				flag_exsit = 1
# 	if flag_exsit == 0:
# 		vectorGroups.append(tmp_groupVector)
# 		vectorMole.append({})
# 		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
# 		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
# 		for j in xrange(N*(N+3)/2):
# 				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 		if not tmp_mole.existRings():
# 			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			acyclicVecIndex.append(len(vectorGroups))
# 			tmp6_row += 1
# 		else:
# 			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 			cyclicVecIndex.append(len(vectorGroups))
# 			tmp7_row += 1
		
# 		tmp5_row += 1

# tmp5_row = 3
# tmp6_row = 3
# tmp7_row = 3
# for i in xrange(len(vectorGroups)):
# 	tmp5_col = N*(N+3)/2 + 7
# 	tmp6_col = N*(N+3)/2 + 7
# 	tmp7_col = N*(N+3)/2 + 7

# 	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
# 	for tmp_item in tmp_list:
# 		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
# 		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
# 		tmp5_col += 2
# 	if (i+1) in acyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
# 			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
# 			tmp6_col += 2
# 		tmp6_row += 1
# 	elif (i+1) in cyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
# 			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
# 			tmp7_col += 2
# 		tmp7_row += 1
# 	else:
# 		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

# 	tmp5_row += 1

# wb3.close()

# # generate input file
# # method 7
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('inputFile_7.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name') 
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

# tmp2_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh2.write(tmp2_row, tmp2_col, tmp_text)
# 		groupIndex[tmp_text] = tmp2_col
# 		tmp2_col += 1

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

# tmp3_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh3.write(tmp3_row, tmp3_col, tmp_text)
# 		groupIndex[tmp_text] = tmp3_col
# 		tmp3_col += 1

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

# tmp4_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh4.write(tmp4_row, tmp4_col, tmp_text)
# 		groupIndex[tmp_text] = tmp4_col
# 		tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, 'CycleSize')

# tmp2_row = 3
# tmp2_col = 5
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for i in xrange(n):
# 	for j in xrange(N*(N+3)/2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	tmp_groupVector = tmp_mole.getGroupVector7()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		sh3.write(tmp3_row, tmp3_col, index+1)
# 		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		sh4.write(tmp4_row, tmp4_col, index+1)
# 		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 		for j in xrange(N*(N+3)/2):
# 			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()

# vectorGroups = []
# vectorMole = []
# acyclicVecIndex = []
# cyclicVecIndex = []

# wb3 = xlsxwriter.Workbook('inputFile_m7.xlsx')
# sh5 = wb3.add_worksheet('inputVectors')
# sh6 = wb3.add_worksheet('acyclic')
# sh7 = wb3.add_worksheet('cyclic')

# tmp5_row = 0
# tmp5_col = 0
# sh5.write(tmp5_row, tmp5_col, 'ID')
# sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
# sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

# tmp5_row = 1
# sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

# tmp5_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh5.write(tmp5_row, tmp5_col+i, i+1)

# tmp5_row = 2 
# for i in xrange(N):
# 	sh5.write(tmp5_row, tmp5_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp5_col
# 	tmp5_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh5.write(tmp5_row, tmp5_col, tmp_text)
# 		groupIndex[tmp_text] = tmp5_col
# 		tmp5_col += 1

# sh5.write(tmp5_row, tmp5_col+2, 'Name')
# sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

# tmp6_row = 0
# tmp6_col = 0
# sh6.write(tmp6_row, tmp6_col, 'ID')
# sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
# sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

# tmp6_row = 1
# sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

# tmp6_col = 5
# for i in xrange(N*(N+3)/2):
# 	sh6.write(tmp6_row, tmp6_col+i, i+1)

# tmp6_row = 2 
# for i in xrange(N):
# 	sh6.write(tmp6_row, tmp6_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp6_col
# 	tmp6_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh6.write(tmp6_row, tmp6_col, tmp_text)
# 		groupIndex[tmp_text] = tmp6_col
# 		tmp6_col += 1

# sh6.write(tmp6_row, tmp6_col+2, 'Name')
# sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

# tmp7_row = 0
# tmp7_col = 0
# sh7.write(tmp7_row, tmp7_col, 'ID')
# sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
# sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

# tmp7_row = 1
# sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

# tmp7_col = 5
# for i in xrange(N*(N+3)/2+1):
# 	sh7.write(tmp7_row, tmp7_col+i, i+1)

# tmp7_row = 2 
# for i in xrange(N):
# 	sh7.write(tmp7_row, tmp7_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp7_col
# 	tmp7_col += 1	

# for i in xrange(N):
# 	for j in xrange(i, N):
# 		tmp_list = sorted([all_groups[i], all_groups[j]])
# 		tmp_text = tmp_list[0] + '-' + tmp_list[1]
# 		sh7.write(tmp7_row, tmp7_col, tmp_text)
# 		groupIndex[tmp_text] = tmp7_col
# 		tmp7_col += 1
# sh7.write(tmp7_row, tmp7_col, 'CycleSize')
# sh7.write(tmp7_row, tmp7_col+2, 'Name')
# sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

# tmp5_row = 3
# tmp5_col = 0
# tmp6_row = 3
# tmp6_col = 0
# tmp7_row = 3
# tmp7_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	tmp_groupVector = tmp_mole.getGroupVector7()
	
# 	flag_exsit = 0
# 	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
# 		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
# 			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
# 			if max(abs(tmp_diff)) < 1e-5:			
# 				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
# 				flag_exsit = 1
# 	if flag_exsit == 0:
# 		vectorGroups.append(tmp_groupVector)
# 		vectorMole.append({})
# 		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
# 		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
# 		for j in xrange(N*(N+3)/2):
# 				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 		if not tmp_mole.existRings():
# 			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			acyclicVecIndex.append(len(vectorGroups))
# 			tmp6_row += 1
# 		else:
# 			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
# 			for j in xrange(N*(N+3)/2):
# 				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
# 			for tmp_vectorEle in tmp_groupVector.keys():
# 				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
# 			cyclicVecIndex.append(len(vectorGroups))
# 			tmp7_row += 1
		
# 		tmp5_row += 1

# tmp5_row = 3
# tmp6_row = 3
# tmp7_row = 3
# for i in xrange(len(vectorGroups)):
# 	tmp5_col = N*(N+3)/2 + 7
# 	tmp6_col = N*(N+3)/2 + 7
# 	tmp7_col = N*(N+3)/2 + 7

# 	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
# 	for tmp_item in tmp_list:
# 		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
# 		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
# 		tmp5_col += 2
# 	if (i+1) in acyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
# 			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
# 			tmp6_col += 2
# 		tmp6_row += 1
# 	elif (i+1) in cyclicVecIndex:
# 		for tmp_item in tmp_list:
# 			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
# 			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
# 			tmp7_col += 2
# 		tmp7_row += 1
# 	else:
# 		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

# 	tmp5_row += 1

# wb3.close()

# generate input file
# method 8
localtime = time.asctime(time.localtime(time.time()))
print localtime
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = xlsxwriter.Workbook('inputFile_8.xlsx')
sh2 = wb2.add_worksheet('inputVectors')
sh3 = wb2.add_worksheet('acyclic')
sh4 = wb2.add_worksheet('cyclic')

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

tmp2_row = 1
sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

tmp2_col = 5
for i in xrange(N*(N+3)/2):
	sh2.write(tmp2_row, tmp2_col+i, i+1)

tmp2_row = 2 
for i in xrange(N):
	sh2.write(tmp2_row, tmp2_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp2_col
	tmp2_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh2.write(tmp2_row, tmp2_col, tmp_text)
		groupIndex[tmp_text] = tmp2_col
		tmp2_col += 1

tmp3_row = 0
tmp3_col = 0
sh3.write(tmp3_row, tmp3_col, 'ID')
sh3.write(tmp3_row, tmp3_col+1, 'Name')
sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

tmp3_row = 1
sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

tmp3_col = 5
for i in xrange(N*(N+3)/2):
	sh3.write(tmp3_row, tmp3_col+i, i+1)

tmp3_row = 2 
for i in xrange(N):
	sh3.write(tmp3_row, tmp3_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp3_col
	tmp3_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh3.write(tmp3_row, tmp3_col, tmp_text)
		groupIndex[tmp_text] = tmp3_col
		tmp3_col += 1

tmp4_row = 0
tmp4_col = 0
sh4.write(tmp4_row, tmp4_col, 'ID')
sh4.write(tmp4_row, tmp4_col+1, 'Name')
sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

tmp4_row = 1
sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

tmp4_col = 5
for i in xrange(N*(N+3)/2+1):
	sh4.write(tmp4_row, tmp4_col+i, i+1)

tmp4_row = 2 
for i in xrange(N):
	sh4.write(tmp4_row, tmp4_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp4_col
	tmp4_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh4.write(tmp4_row, tmp4_col, tmp_text)
		groupIndex[tmp_text] = tmp4_col
		tmp4_col += 1
sh4.write(tmp4_row, tmp4_col, 'CycleSize')

tmp2_row = 3
tmp2_col = 5
tmp3_row = 3
tmp3_col = 0
tmp4_row = 3
tmp4_col = 0
for i in xrange(n):
	for j in xrange(N*(N+3)/2):
		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

tmp2_row = 3
tmp2_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	sh2.write(tmp2_row, tmp2_col, index+1)
	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

	tmp_groupVector = tmp_mole.getGroupVector8()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

	if not tmp_mole.existRings():
		sh3.write(tmp3_row, tmp3_col, index+1)
		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
		for j in xrange(N*(N+3)/2):
			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
		tmp3_row += 1
	else:
		sh4.write(tmp4_row, tmp4_col, index+1)
		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
		for j in xrange(N*(N+3)/2):
			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
		tmp4_row += 1
	
	tmp2_row += 1

wb2.close()

vectorGroups = []
vectorMole = []
acyclicVecIndex = []
cyclicVecIndex = []

wb3 = xlsxwriter.Workbook('inputFile_m8.xlsx')
sh5 = wb3.add_worksheet('inputVectors')
sh6 = wb3.add_worksheet('acyclic')
sh7 = wb3.add_worksheet('cyclic')

tmp5_row = 0
tmp5_col = 0
sh5.write(tmp5_row, tmp5_col, 'ID')
sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

tmp5_row = 1
sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

tmp5_col = 5
for i in xrange(N*(N+3)/2):
	sh5.write(tmp5_row, tmp5_col+i, i+1)

tmp5_row = 2 
for i in xrange(N):
	sh5.write(tmp5_row, tmp5_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp5_col
	tmp5_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh5.write(tmp5_row, tmp5_col, tmp_text)
		groupIndex[tmp_text] = tmp5_col
		tmp5_col += 1

sh5.write(tmp5_row, tmp5_col+2, 'Name')
sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

tmp6_row = 0
tmp6_col = 0
sh6.write(tmp6_row, tmp6_col, 'ID')
sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

tmp6_row = 1
sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

tmp6_col = 5
for i in xrange(N*(N+3)/2):
	sh6.write(tmp6_row, tmp6_col+i, i+1)

tmp6_row = 2 
for i in xrange(N):
	sh6.write(tmp6_row, tmp6_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp6_col
	tmp6_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh6.write(tmp6_row, tmp6_col, tmp_text)
		groupIndex[tmp_text] = tmp6_col
		tmp6_col += 1

sh6.write(tmp6_row, tmp6_col+2, 'Name')
sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

tmp7_row = 0
tmp7_col = 0
sh7.write(tmp7_row, tmp7_col, 'ID')
sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

tmp7_row = 1
sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

tmp7_col = 5
for i in xrange(N*(N+3)/2+1):
	sh7.write(tmp7_row, tmp7_col+i, i+1)

tmp7_row = 2 
for i in xrange(N):
	sh7.write(tmp7_row, tmp7_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp7_col
	tmp7_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh7.write(tmp7_row, tmp7_col, tmp_text)
		groupIndex[tmp_text] = tmp7_col
		tmp7_col += 1
sh7.write(tmp7_row, tmp7_col, 'CycleSize')
sh7.write(tmp7_row, tmp7_col+2, 'Name')
sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

tmp5_row = 3
tmp5_col = 0
tmp6_row = 3
tmp6_col = 0
tmp7_row = 3
tmp7_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	tmp_groupVector = tmp_mole.getGroupVector8()
	
	flag_exsit = 0
	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
			if max(abs(tmp_diff)) < 1e-5:			
				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
				flag_exsit = 1
	if flag_exsit == 0:
		vectorGroups.append(tmp_groupVector)
		vectorMole.append({})
		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
		for j in xrange(N*(N+3)/2):
				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

		if not tmp_mole.existRings():
			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
			for j in xrange(N*(N+3)/2):
				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
			for tmp_vectorEle in tmp_groupVector.keys():
				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
			acyclicVecIndex.append(len(vectorGroups))
			tmp6_row += 1
		else:
			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
			for j in xrange(N*(N+3)/2):
				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
			for tmp_vectorEle in tmp_groupVector.keys():
				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
			cyclicVecIndex.append(len(vectorGroups))
			tmp7_row += 1
		
		tmp5_row += 1

tmp5_row = 3
tmp6_row = 3
tmp7_row = 3
for i in xrange(len(vectorGroups)):
	tmp5_col = N*(N+3)/2 + 7
	tmp6_col = N*(N+3)/2 + 7
	tmp7_col = N*(N+3)/2 + 7

	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
	for tmp_item in tmp_list:
		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
		tmp5_col += 2
	if (i+1) in acyclicVecIndex:
		for tmp_item in tmp_list:
			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
			tmp6_col += 2
		tmp6_row += 1
	elif (i+1) in cyclicVecIndex:
		for tmp_item in tmp_list:
			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
			tmp7_col += 2
		tmp7_row += 1
	else:
		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

	tmp5_row += 1

wb3.close()

# # just used for alkanes
# # generate input file
# # conventional method 
# localtime = time.asctime(time.localtime(time.time()))
# print localtime
# groupIndex = {}
# all_groups = sorted(list(all_groups))
# N = len(all_groups)
# n = len(all_moles)

# wb2 = xlsxwriter.Workbook('conventionalGA.xlsx')
# sh2 = wb2.add_worksheet('inputVectors')
# sh3 = wb2.add_worksheet('acyclic')
# sh4 = wb2.add_worksheet('cyclic')

# tmp2_row = 0
# tmp2_col = 0
# sh2.write(tmp2_row, tmp2_col, 'ID')
# sh2.write(tmp2_row, tmp2_col+1, 'Name')
# sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
# sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
# sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

# tmp2_row = 1
# sh2.write(tmp2_row, tmp2_col+3, N+2)

# tmp2_col = 5
# for i in xrange(N+2):
# 	sh2.write(tmp2_row, tmp2_col+i, i+1)

# tmp2_row = 2 
# for i in xrange(N):
# 	sh2.write(tmp2_row, tmp2_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp2_col
# 	tmp2_col += 1	

# sh2.write(tmp2_row, tmp2_col, 'GAUCHE')
# groupIndex['GAUCHE'] = tmp2_col
# tmp2_col += 1
# sh2.write(tmp2_row, tmp2_col, '1-5_interaction')
# groupIndex['1-5_interaction'] = tmp2_col

# tmp3_row = 0
# tmp3_col = 0
# sh3.write(tmp3_row, tmp3_col, 'ID')
# sh3.write(tmp3_row, tmp3_col+1, 'Name')
# sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
# sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
# sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

# tmp3_row = 1
# sh3.write(tmp3_row, tmp3_col+3, N+2)

# tmp3_col = 5
# for i in xrange(N+2):
# 	sh3.write(tmp3_row, tmp3_col+i, i+1)

# tmp3_row = 2 
# for i in xrange(N):
# 	sh3.write(tmp3_row, tmp3_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp3_col
# 	tmp3_col += 1	

# sh3.write(tmp3_row, tmp3_col, 'GAUCHE')
# groupIndex['GAUCHE'] = tmp3_col
# tmp3_col += 1
# sh3.write(tmp3_row, tmp3_col, '1-5_interaction')
# groupIndex['1-5_interaction'] = tmp3_col

# tmp4_row = 0
# tmp4_col = 0
# sh4.write(tmp4_row, tmp4_col, 'ID')
# sh4.write(tmp4_row, tmp4_col+1, 'Name')
# sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
# sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
# sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

# tmp4_row = 1
# sh4.write(tmp4_row, tmp4_col+3, N+2)

# tmp4_col = 5
# for i in xrange(N+2):
# 	sh4.write(tmp4_row, tmp4_col+i, i+1)

# tmp4_row = 2 
# for i in xrange(N):
# 	sh4.write(tmp4_row, tmp4_col, all_groups[i])
# 	groupIndex[all_groups[i]] = tmp4_col
# 	tmp4_col += 1	

# sh4.write(tmp4_row, tmp4_col, 'GAUCHE')
# groupIndex['GAUCHE'] = tmp4_col
# tmp4_col += 1
# sh4.write(tmp4_row, tmp4_col, '1-5_interaction')
# groupIndex['1-5_interaction'] = tmp4_col

# tmp2_row = 3
# tmp2_col = 5
# for i in xrange(n):
# 	for j in xrange(N+2):
# 		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

# tmp2_row = 3
# tmp2_col = 0
# tmp3_row = 3
# tmp3_col = 0
# tmp4_row = 3
# tmp4_col = 0
# for (index, tmp_mole) in enumerate(all_moles):
# 	tmp_groupVector = {}

# 	sh2.write(tmp2_row, tmp2_col, index+1)
# 	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
# 	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

# 	sh3.write(tmp3_row, tmp3_col, index+1)
# 	sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
# 	sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
# 	for j in xrange(N+2):
# 		sh3.write(tmp3_row, tmp3_col+5+j, 0.0)

# 	sh4.write(tmp4_row, tmp4_col, index+1)
# 	sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
# 	sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
# 	for j in xrange(N+2):
# 		sh4.write(tmp4_row, tmp4_col+5+j, 0.0)

# 	tmp_groupVector = tmp_mole.getConventionalGAVector()
# 	for tmp_vectorEle in tmp_groupVector.keys():
# 		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

# 	if not tmp_mole.existRings():
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp3_row += 1
# 	else:
# 		for tmp_vectorEle in tmp_groupVector.keys():
# 			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
# 		tmp4_row += 1
	
# 	tmp2_row += 1

# wb2.close()