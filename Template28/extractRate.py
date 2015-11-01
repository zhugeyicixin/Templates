# READING--------------------------------------------------------------------------------------
from xlrd import *
from xlwt import *
import os
import re
import shutil
import numpy as np
import matplotlib.pyplot as plt

# variable
rateDict = {}

# constants
pattern_sheet = re.compile('^rate-of-production_for_no_1_([0-9]+)$')
pattern_species = re.compile('^ *([\_\-cho0-9a-z]+)_ROP_GasRxn#([0-9]+)_\(mole/cm3-sec\).*| *([\_\-cho0-9a-z]+)_ROP_GasRxn_(Total)_\(mole/cm3-sec\).*$')

tLineNum = 53

targets = ['c9h20_26',
'c9h19_26_a','c9h19_26_b','c9h19_26_c','c9h19_26_d',
'c9h18_1_26','c9h18_2_26','c9h18_3_26',
'c9h19oo_1_26','c9h19oo_2_26','c9h19oo_3_26','c9h19oo_4_26',
'c9ooh_1_26_b', 'c9ooh_1_26_c', 'c9ooh_1_26_d', 'c9ooh_1_26_e', 'c9ooh_1_26_f', 'c9ooh_1_26_g',
'c9ooh_2_26_a', 'c9ooh_2_26_c', 'c9ooh_2_26_d', 'c9ooh_2_26_e', 'c9ooh_2_26_f', 'c9ooh_2_26_g',
'c9ooh_3_26_a', 'c9ooh_3_26_b', 'c9ooh_3_26_d', 'c9ooh_3_26_e', 'c9ooh_3_26_f', 'c9ooh_3_26_g',
'c9ooh_4_26_a', 'c9ooh_4_26_b', 'c9ooh_4_26_c',
'c9ooh_1_oo_1_26', 'c9ooh_1_oo_2_26', 'c9ooh_1_oo_3_26', 'c9ooh_1_oo_4_26', 'c9ooh_1_oo_5_26', 'c9ooh_1_oo_6_26',
'c9ooh_2_oo_1_26', 'c9ooh_2_oo_3_26', 'c9ooh_2_oo_4_26', 'c9ooh_2_oo_5_26', 'c9ooh_2_oo_6_26', 'c9ooh_2_oo_7_26',
'c9ooh_3_oo_1_26', 'c9ooh_3_oo_2_26', 'c9ooh_3_oo_4_26', 'c9ooh_3_oo_5_26', 'c9ooh_3_oo_6_26', 'c9ooh_3_oo_7_26',
'c9ooh_4_oo_1_26', 'c9ooh_4_oo_2_26', 'c9ooh_4_oo_3_26'
]

wbName = 'ROP_ver.1.2.14_10atm_1.0_2.76N2_750K.xlsx'

# open workbook
wb = open_workbook(wbName)
sheets = [s.name for s in wb.sheets()]

wb2 = Workbook()
sh2 = wb2.add_sheet('RateCollection')
sh3 = wb2.add_sheet('SimplifiedRate')

for tmp_sheet in sheets:
	tmp_m = pattern_sheet.match(tmp_sheet)
	if tmp_m:
		sh = wb.sheet_by_name(tmp_sheet)
		tmp_row = 0
		for tmp_col in xrange(sh.ncols):
			tmp2_m = pattern_species.match(sh.cell_value(tmp_row, tmp_col))
			if tmp2_m:
				if tmp2_m.group(1) == None:
					tmp_species = tmp2_m.group(3)
					tmp_reaction = tmp2_m.group(4)
				else:
					tmp_species = tmp2_m.group(1)
					tmp_reaction = tmp2_m.group(2)
				tmp_rate = float(sh.cell_value(tLineNum, tmp_col))
				if tmp_species not in rateDict.keys():
					rateDict[tmp_species] = []
				rateDict[tmp_species].append([tmp_reaction, tmp_rate])

tmp2_row = 0
tmp2_col = 0
tmp3_row = 0
tmp3_col = 0
for tmp_species in targets:
	totalRate = ''
	reactionList = []
	rateList = []

	if tmp_species not in rateDict.keys():
		print 'Error! The target is not in the excel file!', tmp_species
		print rateDict.keys()

	for tmp_pair in  rateDict[tmp_species]:
		if tmp_pair[0] == 'Total':
			if totalRate == '':
				totalRate = tmp_pair[1]
			else:
				print 'Error! There are two total rates!', tmp_species
		else:
			reactionList.append(int(tmp_pair[0]))
			rateList.append(tmp_pair[1])
	if totalRate == '':
		print 'Error! There is no total rate!', tmp_species
	tmp_set = set(reactionList)
	if len(tmp_set) < len(reactionList):
		print 'Error! There are duplicated reaction IDs!', tmp_species
	relaRate = np.array(rateList)/totalRate
	relaAbsRate = abs(relaRate)
	sortedRateIndex = sorted(range(len(rateList)), reverse=True, key=lambda x:relaAbsRate[x])
	tmp2_col = 0
	sh2.write(tmp2_row, tmp2_col, tmp_species)
	sh2.write(tmp2_row, tmp2_col+1, 'Total')
	sh2.write(tmp2_row+1, tmp2_col+1, totalRate)
	sh2.write(tmp2_row+2, tmp2_col+1, 1.0)
	tmp2_col += 2
	for (tmp_index, tmp_reaction) in enumerate(sortedRateIndex):
		tmp_num = tmp_index%200
		if tmp_num == 0 and tmp_index > 0:
			tmp2_row += 4
		sh2.write(tmp2_row, tmp2_col+tmp_num, reactionList[tmp_reaction])
		sh2.write(tmp2_row+1, tmp2_col+tmp_num, rateList[tmp_reaction])
		sh2.write(tmp2_row+2, tmp2_col+tmp_num, relaRate[tmp_reaction])
	tmp2_row += 5

	tmp3_col = 0
	sh3.write(tmp3_row, tmp3_col, tmp_species)
	sh3.write(tmp3_row, tmp3_col+1, 'Total')
	sh3.write(tmp3_row+1, tmp3_col+1, totalRate)
	sh3.write(tmp3_row+2, tmp3_col+1, 1.0)
	tmp3_col += 2
	for (tmp_index, tmp_reaction) in enumerate(sortedRateIndex):
		if abs(relaRate[tmp_reaction]) < 0.01:
			break
		tmp_num = tmp_index%200
		if tmp_num == 0 and tmp_index > 0:
			tmp3_row += 4
		sh3.write(tmp3_row, tmp3_col+tmp_index, reactionList[tmp_reaction])
		sh3.write(tmp3_row+1, tmp3_col+tmp_index, rateList[tmp_reaction])
		sh3.write(tmp3_row+2, tmp3_col+tmp_index, relaRate[tmp_reaction])

	tmp3_row += 5


wb2.save('RateExtraction.xls')

print 'Rate extracted successfully!\n'



