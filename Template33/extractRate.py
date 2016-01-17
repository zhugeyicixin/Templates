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
pattern_sheet = re.compile('^END_POINT_VS_PARAMETER_([0-9]+)$')
pattern_netHeat = re.compile('^ *Net_rxn_rate_GasRxn#([0-9]+)_end_point_.*$')

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

times = []
netHeat = []

# open workbook
wb = open_workbook(wbName)
sheets = [s.name for s in wb.sheets()]

wb2 = Workbook()
sh2 = wb2.add_sheet('netHeatRelease')

for tmp_sheet in sheets:
	tmp_m = pattern_sheet.match(tmp_sheet)
	if tmp_m:
		sh = wb.sheet_by_name(tmp_sheet)
		tmp_row = 0
		for tmp_col in xrange(sh.ncols):
			tmp2_m = pattern_species.match(sh.cell_value(tmp_row, tmp_col))
			if tmp2_m:
				for i in xrange(1,sh.nrows):
					if len(netHeat) < i:
						times.append(float(sh.cell_value(0+i, 0)))
						netHeat.append({})
					netHeat[i][float(tmp2_m.group(1))]	= float(sh.cell_value(tmp_row+i, tmp_col))
tmp2_row = 0
tmp2_col = 0
for i in xrange(len(times)):
	sh2.write(tmp2_row, tmp2_col+3*i, times[i])
	for item in netHeat[i].items():
		sh2.write(tmp2_row+item[0], tmp2_col+3*i, item[0])
		sh2.write(tmp2_row+item[0], tmp2_col+3*i+1, item[1])



wb2.save('heatExtraction.xls')

print 'Heat extracted successfully!\n'



