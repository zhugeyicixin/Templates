# READING--------------------------------------------------------------------------------------
from xlrd import *
from xlwt import *
import os
import re
import shutil
from xlutils.copy import copy
import numpy as np
import matplotlib.pyplot as plt

import phys
import arrhenius

# constants
phys1=phys.phys()

# open workbook
name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
T_fit = temperature[2:13]
lowT_index = 2
highT_index = 13
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[5].strip(' \n')
		temperature = map(float, tmp_line.split())
		tmp_line = tmp_lines[11].strip('\n')
		tmp_line = map(float, tmp_line.split())
		lowT_index, highT_index = phys1.TRangeIndex(temperature, tmp_line[0], tmp_line[1])
		T_fit = temperature[lowT_index:highT_index]
		fr.close()

wb=open_workbook(name + '.xls')
sheets=[s.name for s in wb.sheets()]

# constants
# the number of rows and columns of the displayed fitting figures
FIG_ROW = 6
FIG_COL = 5

# variables
num_reac=[]
num_prod=[]
TSs_abbr=[]
reactionsDict={}
reacNames = []
rate_f = []
coeff_f = []
deviation_f = []
rate_f_fitted = []
rate_r = []
coeff_r = []
deviation_r = []
rate_r_fitted = []
Kconst = []
coeff_K = []
deviation_K = []
Kconst_fitted = []

# temporary variables
num_rows = 0
num_cols = 0
tmp_row = 0
tmp_col = 0
tmp_rate = []
tmp_K = []
tmp_coeff = []
tmp_deviation = []
sigma_miu = 0

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


# read thermo data from excel
# read sketch info of all reaction
# sh=wb.sheet_by_name('Reactions')
# num_rows = sh.nrows
# num_cols = sh.ncols
# for tmp_row in range(2,num_rows):
# 	if int(sh.cell_value(tmp_row,0)) != 0:
# 		num_reac.append(int(int(sh.cell_value(tmp_row,0))/10))
# 		num_prod.append(int(sh.cell_value(tmp_row,0))%10)
# 		TSs_abbr.append(sh.cell_value(tmp_row, 7))
# 		if num_reac[-1] != 1:
# 			print 'Error! The number of reactants is not 1 in the forward direction!'
# 		reactionsDict[TSs_abbr[-1]] = [num_reac[-1], num_prod[-1]]

# read info of forward reaction
sh=wb.sheet_by_name('Rate')
num_rows = sh.nrows
num_cols = sh.ncols
tmp_row = 3
tmp_col = 2

for tmp_row in range(3, num_rows):
	if sh.cell_value(tmp_row, 1) == '':
		continue
	# start line of a reaction
	if (tmp_row%(len(temperature)+1))==3:
		tmp_rate =[]

		tmp_name = sh.cell_value(tmp_row, 0)
		reacNames.append(tmp_name)
		# if tmp_name not in reactionsDict:
		# 	continue
		# else:
		# 	reacNames.append(tmp_name)
		# 	if reactionsDict[tmp_name][0] != 1:
		# 		print 'Error! The number of reactants is not 1 in the forward direction!' + reacNames[-1]


	# if tmp_name not in reactionsDict:
	# 	continue

	tmp_col = 2
	tmp_rate.append(float(sh.cell_value(tmp_row, tmp_col)))

	# end line of a reaction
	if (tmp_row%(len(temperature)+1))==1:
		rate_f.append(tmp_rate)
		tmp_rate = []

# # read info of reverse reaction
# sh=wb.sheet_by_name('ReverseRate')
# num_rows = sh.nrows
# num_cols = sh.ncols
# tmp_row = 3
# tmp_col = 2

# for tmp_row in range(3, num_rows):
# 	if sh.cell_value(tmp_row, 1) == '':
# 		continue
# 	# start line of a reaction
# 	if (tmp_row%(len(temperature)+1))==3:
# 		tmp_rate =[]

# 		tmp_name = sh.cell_value(tmp_row, 0)		
# 		if tmp_name not in reactionsDict:
# 			continue
# 		else:
# 			# reacNames.append(sh.cell_value(tmp_row, 0))
# 			sigma_miu = reactionsDict[tmp_name][1] - reactionsDict[tmp_name][0]
		

# 	# if tmp_name not in reactionsDict:
# 	# 	continue
# 	tmp_col = 2
# 	tmp_rate.append(float(sh.cell_value(tmp_row, tmp_col))*(phys1.NA)**sigma_miu)

# 	# end line of a reaction
# 	if (tmp_row%(len(temperature)+1))==1:
# 		rate_r.append(tmp_rate)
# 		tmp_rate = []

# # read info of equilibrium constants
# sh=wb.sheet_by_name('EquilibriumConstants')
# num_rows = sh.nrows
# num_cols = sh.ncols
# tmp_row = 2
# tmp_col = 2

# for tmp_row in range(2, num_rows):
# 	if sh.cell_value(tmp_row, 1) == '':
# 		continue
# 	# start line of a reaction
# 	if (tmp_row%(len(temperature)+1))==2:
# 		tmp_K =[]

# 		tmp_name = sh.cell_value(tmp_row, 0)
# 		if tmp_name not in reactionsDict:
# 			continue
# 		else:
# 			# reacNames.append(sh.cell_value(tmp_row, 0))
# 			pass

# 	# if tmp_name	not in reactionsDict:
# 	# 	continue
# 	tmp_col = 2
# 	tmp_K.append(float(sh.cell_value(tmp_row, tmp_col)))

# 	# end line of a reaction
# 	if (tmp_row%(len(temperature)+1))==0:
# 		Kconst.append(tmp_K)
# 		tmp_K = []

# fitting the parameters with arrhenius formula
T_fit = np.array(T_fit)
for (index, tmp_name) in enumerate(reacNames):
	temperature = np.array(temperature)
	rate_f[index] = np.array(rate_f[index])
	# rate_r[index] = np.array(rate_r[index])
	# Kconst[index] = np.array(Kconst[index])	
	
	tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(T_fit, rate_f[index][lowT_index: highT_index], threshold=5e-2)
	if rela_RMS > 5e-2:
		print 'reaction name:\t' + tmp_name + '\ttype:\tforward rate fitting\n---'
	coeff_f.append(tmp_coeff)
	deviation_f.append(tmp_deviation)

	# tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(T_fit, rate_r[index][lowT_index: highT_index], threshold=5e-2)
	# if rela_RMS > 5e-2:
	# 	print 'reaction name:\t' + tmp_name + '\ttype:\treverse rate fitting\n---'
	# coeff_r.append(tmp_coeff)
	# deviation_r.append(tmp_deviation)

	# tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(T_fit, Kconst[index][lowT_index: highT_index], threshold=5e-2)
	# if rela_RMS > 5e-2:
	# 	print 'reaction name:\t' + tmp_name + '\ttype:\tequilibrium constant fitting\n---'
	# coeff_K.append(tmp_coeff)
	# deviation_K.append(tmp_deviation)

# draw figures
tmp_fig = plt.figure(figsize=(22,12))
tmp_fig2 = plt.figure(figsize=(22,12))
tmp_fig3 = plt.figure(figsize=(22,12))
for (index, tmp_name) in enumerate(reacNames):
	tmp_ax = tmp_fig.add_subplot(FIG_ROW,FIG_COL,index+1)
	tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	rate_f_fitted.append(arrhenius.func_arrhenius(temperature,*coeff_f[index]))
	tmp_ax.plot(1000.0/T_fit, np.log10(rate_f[index][lowT_index: highT_index]), 'b*', 1000.0/T_fit, np.log10(rate_f_fitted[-1][lowT_index: highT_index]),'r-')
	tmp_ax.set_title(tmp_name)

	# tmp_ax2 = tmp_fig2.add_subplot(FIG_ROW,FIG_COL,index+1)
	# tmp_fig2.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	# rate_r_fitted.append(arrhenius.func_arrhenius(temperature,*coeff_r[index]))
	# tmp_ax2.plot(1000.0/T_fit, np.log10(rate_r[index][lowT_index: highT_index]), 'b*', 1000.0/T_fit, np.log10(rate_r_fitted[-1][lowT_index: highT_index]),'r-')
	# tmp_ax2.set_title(tmp_name)

	# tmp_ax3 = tmp_fig3.add_subplot(FIG_ROW,FIG_COL,index+1)
	# tmp_fig3.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	# Kconst_fitted.append(arrhenius.func_arrhenius(temperature,*coeff_K[index]))
	# tmp_ax3.plot(1000.0/T_fit, np.log10(Kconst[index][lowT_index: highT_index]), 'b*', 1000.0/T_fit, np.log10(Kconst_fitted[-1][lowT_index: highT_index]),'r-')
	# tmp_ax3.set_title(tmp_name)

tmp_fig.show()
# tmp_fig2.show()
# tmp_fig3.show()
tmp_fig.savefig('rate_fitting' + '.png',dpi=300)
# tmp_fig2.savefig('thermo_rate_reverse' + '.png',dpi=300)
# tmp_fig3.savefig('thermo_equilibrium constants' + '.png',dpi=300)
plt.close(tmp_fig)
# plt.close(tmp_fig2)
# plt.close(tmp_fig3)

# write to excel
# write forward reaction
wb_new = copy(wb)
sh=wb_new.get_sheet(sheets.index('rate_f'))
sh.cell_overwrite_ok = True
tmp_row = 1
tmp_col = 0
for (index, tmp_name) in enumerate(reacNames):
	sh.write(tmp_row, tmp_col+0, tmp_name)
	sh.write(tmp_row, tmp_col+1, coeff_f[index][0])
	sh.write(tmp_row, tmp_col+2, coeff_f[index][1])
	sh.write(tmp_row, tmp_col+3, coeff_f[index][2])
	tmp_row += 1

tmp_row = 1
tmp_col = 5
for (index, tmp_name) in enumerate(reacNames):
	if (tmp_row%(len(temperature)+1))==1:
		tmp_col = 5
		sh.write(tmp_row, tmp_col, tmp_name)
	for i in range(len(temperature)):
		sh.write(tmp_row+i, tmp_col+1, temperature[i])
		sh.write(tmp_row+i, tmp_col+2, rate_f[index][i])
		sh.write(tmp_row+i, tmp_col+3, rate_f_fitted[index][i])
		sh.write(tmp_row+i, tmp_col+4, (rate_f_fitted[index][i]-rate_f[index][i])/rate_f[index][i])
	tmp_row += len(temperature)+1	

# # write reverse reaction
# sh=wb_new.get_sheet(sheets.index('rate_r'))
# sh.cell_overwrite_ok = True
# tmp_row = 1
# tmp_col = 0
# for (index, tmp_name) in enumerate(reacNames):
# 	sh.write(tmp_row, tmp_col+0, tmp_name)
# 	sh.write(tmp_row, tmp_col+1, coeff_r[index][0])
# 	sh.write(tmp_row, tmp_col+2, coeff_r[index][1])
# 	sh.write(tmp_row, tmp_col+3, coeff_r[index][2])
# 	tmp_row += 1

# tmp_row = 1
# tmp_col = 5
# for (index, tmp_name) in enumerate(reacNames):
# 	if (tmp_row%(len(temperature)+1))==1:
# 		tmp_col = 5
# 		sh.write(tmp_row, tmp_col, tmp_name)
# 	for i in range(len(temperature)):
# 		sh.write(tmp_row+i, tmp_col+1, temperature[i])
# 		sh.write(tmp_row+i, tmp_col+2, rate_r[index][i])
# 		sh.write(tmp_row+i, tmp_col+3, rate_r_fitted[index][i])
# 		sh.write(tmp_row+i, tmp_col+4, (rate_r_fitted[index][i]-rate_r[index][i])/rate_r[index][i])
# 	tmp_row += len(temperature)+1	

# # write equilibrium constants
# sh=wb_new.get_sheet(sheets.index('Kconst'))
# sh.cell_overwrite_ok = True
# tmp_row = 1
# tmp_col = 0
# for (index, tmp_name) in enumerate(reacNames):
# 	sh.write(tmp_row, tmp_col+0, tmp_name)
# 	sh.write(tmp_row, tmp_col+1, coeff_K[index][0])
# 	sh.write(tmp_row, tmp_col+2, coeff_K[index][1])
# 	sh.write(tmp_row, tmp_col+3, coeff_K[index][2])
# 	tmp_row += 1

# tmp_row = 1
# tmp_col = 5
# for (index, tmp_name) in enumerate(reacNames):
# 	if (tmp_row%(len(temperature)+1))==1:
# 		tmp_col = 5
# 		sh.write(tmp_row, tmp_col, tmp_name)
# 	for i in range(len(temperature)):
# 		sh.write(tmp_row+i, tmp_col+1, temperature[i])
# 		sh.write(tmp_row+i, tmp_col+2, Kconst[index][i])
# 		sh.write(tmp_row+i, tmp_col+3, Kconst_fitted[index][i])
# 		sh.write(tmp_row+i, tmp_col+4, (Kconst_fitted[index][i]-Kconst[index][i])/Kconst[index][i])
# 	tmp_row += len(temperature)+1

wb_new.save(name + '.xls')

print 'Arrhenius fiited successfully!\n'



