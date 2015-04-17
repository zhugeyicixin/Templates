# READING--------------------------------------------------------------------------------------
from xlrd import *
from xlwt import *
import os
import re
import shutil
from xlutils.copy import copy
import numpy as np

import phys

# open workbook
name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[5].strip(' \n')
		temperature = map(float, tmp_line.split())
		fr.close()

wb=open_workbook(name + '.xls')

# variables
phys1=phys.phys()
num_reac=[]
num_prod=[]
TSs_abbr=[]
reactionsDict={}
reacNames = []
DS_f = []
DH_f = []
DCp_f = []
DG_f =[]
Qelectr_R = []
entropy_R = []
Cp_R = []
H_R = []
DS_r = []
DH_r = []
DCp_r = []
DG_r =[]
Qelectr_P = []
entropy_P = []
Cp_P = []
H_P = []

# temporary variables
num_rows = 0
num_cols = 0
tmp_row = 0
tmp_col = 0
tmp_DS =[]
tmp_DH = []
tmp_DCp = []
tmp_DG = []
tmp_Qelectr = []
tmp_entropy = []
tmp_Cp = []
tmp_H = []
tmp_Qelectr2 = []
tmp_entropy2 = []
tmp_Cp2 = []
tmp_H2 = []
tmp_name = ''
tmp_K = 0.0

# read thermo data from excel
# read sketch info of all reaction
sh=wb.sheet_by_index(0)
num_rows = sh.nrows
num_cols = sh.ncols
for tmp_row in range(2,num_rows):
	if int(sh.cell_value(tmp_row,0)) != 0:
		num_reac.append(int(int(sh.cell_value(tmp_row,0))/10))
		num_prod.append(int(sh.cell_value(tmp_row,0))%10)
		TSs_abbr.append(sh.cell_value(tmp_row, 7))
		if num_reac[-1] != 1:
			print 'Error! The number of reactants is not 1 in the forward direction!'
		reactionsDict[TSs_abbr[-1]] = [num_reac[-1], num_prod[-1]]

# read info of forward reaction
sh=wb.sheet_by_index(2)
num_rows = sh.nrows
num_cols = sh.ncols
tmp_row = 3
tmp_col = 21

for tmp_row in range(3, num_rows):
	if sh.cell_value(tmp_row, 1) == '':
		continue
	# start line of a reaction
	if (tmp_row%(len(temperature)+1))==3:
		tmp_name = sh.cell_value(tmp_row, 0)
		reacNames.append(tmp_name)
		tmp_DS =[]
		tmp_DH = []
		tmp_DCp = []
		tmp_DG = []
		tmp_Qelectr = []
		tmp_entropy = []
		tmp_Cp = []
		tmp_H = []		

	tmp_col = 22
	tmp_DS.append(float(sh.cell_value(tmp_row, tmp_col+0)))
	tmp_DH.append(float(sh.cell_value(tmp_row, tmp_col+1)))
	tmp_DCp.append(float(sh.cell_value(tmp_row, tmp_col+2)))
	tmp_DG.append(float(sh.cell_value(tmp_row, tmp_col+3)))
	tmp_col += 4
	for i in range(reactionsDict[tmp_name][0]):
		tmp_Qelectr2.append(int(sh.cell_value(tmp_row, tmp_col + 0 + 4*i)))
		tmp_entropy2.append(float(sh.cell_value(tmp_row, tmp_col + 1 + 4*i)))
		tmp_Cp2.append(float(sh.cell_value(tmp_row, tmp_col + 2 + 4*i)))
		tmp_H2.append(float(sh.cell_value(tmp_row, tmp_col + 3 + 4*i)))
	tmp_Qelectr.append(tmp_Qelectr2)
	tmp_entropy.append(tmp_entropy2)
	tmp_Cp.append(tmp_Cp2)		
	tmp_H.append(tmp_H2)
	tmp_Qelectr2 = []
	tmp_entropy2 = []
	tmp_Cp2 = []
	tmp_H2 = []

	# end line of a reaction
	if (tmp_row%(len(temperature)+1))==1:
		DS_f.append(tmp_DS)
		DH_f.append(tmp_DH)
		DCp_f.append(tmp_DCp)
		DG_f.append(tmp_DG)
		Qelectr_R.append(tmp_Qelectr)
		entropy_R.append(tmp_entropy)
		Cp_R.append(tmp_Cp)
		H_R.append(tmp_H)
		tmp_DS =[]
		tmp_DH = []
		tmp_DCp = []
		tmp_DG = []
		tmp_Qelectr = []
		tmp_entropy = []
		tmp_Cp = []
		tmp_H = []

# read info of reverse reaction
sh=wb.sheet_by_index(3)
num_rows = sh.nrows
num_cols = sh.ncols
tmp_row = 3
tmp_col = 21

for tmp_row in range(3, num_rows):
	if sh.cell_value(tmp_row, 1) == '':
		continue
	# start line of a reaction
	if (tmp_row%(len(temperature)+1))==3:
		tmp_name = sh.cell_value(tmp_row, 0)
		# reacNames.append(sh.cell_value(tmp_row, 0))
		tmp_DS =[]
		tmp_DH = []
		tmp_DCp = []
		tmp_DG = []
		tmp_Qelectr = []
		tmp_entropy = []
		tmp_Cp = []
		tmp_H = []		

	tmp_col = 22
	tmp_DS.append(float(sh.cell_value(tmp_row, tmp_col+0)))
	tmp_DH.append(float(sh.cell_value(tmp_row, tmp_col+1)))
	tmp_DCp.append(float(sh.cell_value(tmp_row, tmp_col+2)))
	tmp_DG.append(float(sh.cell_value(tmp_row, tmp_col+3)))
	tmp_col += 4
	for i in range(reactionsDict[tmp_name][1]):
		tmp_Qelectr2.append(int(sh.cell_value(tmp_row, tmp_col + 0 + 4*i)))
		tmp_entropy2.append(float(sh.cell_value(tmp_row, tmp_col + 1 + 4*i)))
		tmp_Cp2.append(float(sh.cell_value(tmp_row, tmp_col + 2 + 4*i)))
		tmp_H2.append(float(sh.cell_value(tmp_row, tmp_col + 3 + 4*i)))
	tmp_Qelectr.append(tmp_Qelectr2)
	tmp_entropy.append(tmp_entropy2)
	tmp_Cp.append(tmp_Cp2)		
	tmp_H.append(tmp_H2)
	tmp_Qelectr2 = []
	tmp_entropy2 = []
	tmp_Cp2 = []
	tmp_H2 = []
	# end line of a reaction
	if (tmp_row%(len(temperature)+1))==1:
		DS_r.append(tmp_DS)
		DH_r.append(tmp_DH)
		DCp_r.append(tmp_DCp)
		DG_r.append(tmp_DG)
		Qelectr_P.append(tmp_Qelectr)
		entropy_P.append(tmp_entropy)
		Cp_P.append(tmp_Cp)
		H_P.append(tmp_H)
		tmp_DS =[]
		tmp_DH = []
		tmp_DCp = []
		tmp_DG = []
		tmp_Qelectr = []
		tmp_entropy = []
		tmp_Cp = []
		tmp_H = []

# write equilibrium data to excel
wb_new = copy(wb)
sh=wb_new.get_sheet(4)
sh.cell_overwrite_ok = True
tmp_row = 2
tmp_col = 0

for (index, tmp_name) in enumerate(reacNames):
	tmp_col = 0
	sh.write(tmp_row, tmp_col, tmp_name)
	for i in range(len(temperature)):
		tmp_col = 1
		sh.write(tmp_row, tmp_col+0, temperature[i])
		tmp_DG = DG_f[index][i] - DG_r[index][i]
		sh.write(tmp_row, tmp_col+4, DS_f[index][i] - DS_r[index][i])
		sh.write(tmp_row, tmp_col+5, DH_f[index][i] - DH_r[index][i])
		sh.write(tmp_row, tmp_col+6, DCp_f[index][i] - DCp_r[index][i])
		sh.write(tmp_row, tmp_col+7, tmp_DG)
		tmp_DG = phys1.calToJoul(tmp_DG*1000)
		sh.write(tmp_row, tmp_col+3, tmp_DG)
		tmp_K = np.exp(-tmp_DG/phys1.R/temperature[i])
		sh.write(tmp_row, tmp_col+2, tmp_K)
		tmp_K = tmp_K * (phys1.atm/phys1.R/temperature[i]*1e-6)**(reactionsDict[tmp_name][1] - reactionsDict[tmp_name][0])
		sh.write(tmp_row, tmp_col+1, tmp_K)
		tmp_col += 8
		for j in range(reactionsDict[tmp_name][0]):
			sh.write(tmp_row, tmp_col + 0 + 4*j, Qelectr_R[index][i][j])
			sh.write(tmp_row, tmp_col + 1 + 4*j, entropy_R[index][i][j])
			sh.write(tmp_row, tmp_col + 2 + 4*j, Cp_R[index][i][j])
			sh.write(tmp_row, tmp_col + 3 + 4*j, H_R[index][i][j])
		tmp_col += 4 * reactionsDict[tmp_name][0]
		for j in range(reactionsDict[tmp_name][1]):
			sh.write(tmp_row, tmp_col + 0 + 4*j, Qelectr_P[index][i][j])
			sh.write(tmp_row, tmp_col + 1 + 4*j, entropy_P[index][i][j])
			sh.write(tmp_row, tmp_col + 2 + 4*j, Cp_P[index][i][j])
			sh.write(tmp_row, tmp_col + 3 + 4*j, H_P[index][i][j])
		tmp_row += 1
	tmp_row += 1

wb_new.save(name + '.xls')

print 'Equilibrium constants collected successfully!'



