# this is used to get group additivity input files
from xlwt import *
from xlrd import *

import chem
import thermoDatabase
import re

# get commands from .name file
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
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'
		fr.close()	

#####################################################################
# read data from the database excel file and generate input file
#####################################################################
wb=open_workbook('database.xls')
sh=wb.sheet_by_name('speciesInfo')

# definition of variables
all_moles = []
all_groups = set()
groupIndex = {}

# definition of temporary variables
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
	tmp_energy = sh.cell_value(tmp_row, 4)
	tmp_geom = sh.cell_value(tmp_row, 7)
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
	# note that this is not real ZPE, but reference energy 
	# currently tmp_energy is the entaly of formation at 298.15 K
	tmp_mole.setZPE(tmp_energy)

	tmp_groups = tmp_mole.get1stOrderGroup()
	all_moles.append(tmp_mole)
	all_groups = all_groups | set(tmp_groups)

# generate input file
# method 1
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = Workbook()
sh2 = wb2.add_sheet('inputVectors', cell_overwrite_ok = True)

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimenstionIndex')

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

tmp2_row = 3
tmp2_col = 5
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

	tmp_groupVector = tmp_mole.getGroupVector1()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
	
	tmp2_row += 1

wb2.save('inputFile_1.xls')


# generate input file
# method 2
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = Workbook()
sh2 = wb2.add_sheet('inputVectors', cell_overwrite_ok = True)

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimenstionIndex')

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

tmp2_row = 3
tmp2_col = 5
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

	tmp_groupVector = tmp_mole.getGroupVector2()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
	
	tmp2_row += 1

wb2.save('inputFile_2.xls')


# generate input file
# method 3
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = Workbook()
sh2 = wb2.add_sheet('inputVectors', cell_overwrite_ok = True)

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimenstionIndex')

tmp2_row = 1
sh2.write(tmp2_row, tmp2_col+3, N*2)

tmp2_col = 5
for i in xrange(N*2):
	sh2.write(tmp2_row, tmp2_col+i, i+1)

tmp2_row = 2 
for i in xrange(N):
	sh2.write(tmp2_row, tmp2_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp2_col
	tmp2_col += 1	


for i in xrange(N):
	tmp_text = all_groups[i] + ' - other Groups'
	sh2.write(tmp2_row, tmp2_col, tmp_text)
	groupIndex[tmp_text] = tmp2_col
	tmp2_col += 1

tmp2_row = 3
tmp2_col = 5
for i in xrange(n):
	for j in xrange(N*2):
		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

tmp2_row = 3
tmp2_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	sh2.write(tmp2_row, tmp2_col, index+1)
	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

	tmp_groupVector = tmp_mole.getGroupVector3()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
	
	tmp2_row += 1

wb2.save('inputFile_3.xls')


# generate input file
# method 3
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = Workbook()
sh2 = wb2.add_sheet('inputVectors', cell_overwrite_ok = True)

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimenstionIndex')

tmp2_row = 1
sh2.write(tmp2_row, tmp2_col+3, N*2)

tmp2_col = 5
for i in xrange(N*2):
	sh2.write(tmp2_row, tmp2_col+i, i+1)

tmp2_row = 2 
for i in xrange(N):
	sh2.write(tmp2_row, tmp2_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp2_col
	tmp2_col += 1	


for i in xrange(N):
	tmp_text = all_groups[i] + ' - other Groups'
	sh2.write(tmp2_row, tmp2_col, tmp_text)
	groupIndex[tmp_text] = tmp2_col
	tmp2_col += 1

tmp2_row = 3
tmp2_col = 5
for i in xrange(n):
	for j in xrange(N*2):
		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

tmp2_row = 3
tmp2_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	sh2.write(tmp2_row, tmp2_col, index+1)
	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

	tmp_groupVector = tmp_mole.getGroupVector4()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
	
	tmp2_row += 1

wb2.save('inputFile_4.xls')


