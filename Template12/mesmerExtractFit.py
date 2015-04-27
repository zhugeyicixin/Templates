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
import mesmer

# open workbook
name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
fit_lowT = 400
fit_highT = 900
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
		tmp_line = map(int, tmp_line.split())
		fit_lowT = tmp_line[0]
		fit_highT = tmp_line[1]
		fr.close()

wb=open_workbook(name + '.xls')
sheets=[s.name for s in wb.sheets()]

# constants
mesmer1 = mesmer.mesmer()
phys1 = phys.phys()
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
totalNum = 0

# read sketch info of all reaction
sh=wb.sheet_by_name('Reactions')
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

# write output data to excel, fit and draw
wb_new = copy(wb)
sh=wb_new.get_sheet(sheets.index('MesmerRate'))				#if overwrite to use cell_overwrite_ok=True
sh.cell_overwrite_ok = True

tmp_fig = plt.figure(figsize=(22,12))
tmp_fig2 = plt.figure(figsize=(22,12))
tmp_fig3 = plt.figure(figsize=(22,12))

os.chdir('mesmerOutput')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('out_',tmp_file)]
os.chdir('..')

totalNum = len(tmp_fileLists)

sh.write(2, 0, 'kf')
sh.write(2+totalNum+2, 0, 'kr')
sh.write(2+(totalNum+2)*2, 0, 'Kc')
sh.write(2, 14, 'kf')
sh.write(2+totalNum+2, 14, 'kr')
sh.write(2+(totalNum+2)*2, 14, 'Kc')
sh.write(2, 29, 'kf')
sh.write(2+totalNum+2, 29, 'kr')
sh.write(2+(totalNum+2)*2, 29, 'Kc')

tmp_row = 2
for (index, tmp_file) in enumerate(tmp_fileLists):
	tmp_num = 0
	tmp_name = tmp_file[4:-4]
	tmp_CanoRate, tmp_PhenoRate = mesmer1.readOutXml('mesmerOutput/' + tmp_file)
	tmp_TSTRate = mesmer1.readOutTest('mesmerOutput/' + tmp_name + '.test')

	tmp_ax = tmp_fig.add_subplot(FIG_ROW,FIG_COL,index+1)
	tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	tmp_ax.set_title(tmp_name)
	tmp_ax2 = tmp_fig2.add_subplot(FIG_ROW,FIG_COL,index+1)
	tmp_fig2.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	tmp_ax2.set_title(tmp_name)	
	tmp_ax3 = tmp_fig3.add_subplot(FIG_ROW,FIG_COL,index+1)
	tmp_fig3.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
	tmp_ax3.set_title(tmp_name)				

	tmp_col = 5
	sh.write(tmp_row, tmp_col, tmp_name)
	if len(tmp_CanoRate) > 2:
		tmp_Kc = tmp_CanoRate[1]/tmp_CanoRate[2]
	tmp_num = len(tmp_CanoRate[0])
	for i in range(len(tmp_CanoRate[0])):
		sh.write(tmp_row+i, tmp_col+1, tmp_CanoRate[0][i])
		sh.write(tmp_row+i, tmp_col+2, tmp_CanoRate[1][i])
		if len(tmp_CanoRate) > 2:
			sh.write(tmp_row+i, tmp_col+3, tmp_CanoRate[2][i])
			sh.write(tmp_row+i, tmp_col+4, tmp_Kc[i])

	TRange = phys1.TRangeIndex(tmp_CanoRate[0], fit_lowT, fit_highT)
	tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_CanoRate[0][TRange[0]: TRange[1]], tmp_CanoRate[1][TRange[0]: TRange[1]], threshold = 5e-2)
	if rela_RMS > 5e-2:
		print 'reaction name:\t' + tmp_name + '\ttype:\tforward micro high-pressure rate fitting\n---'
	tmp_fitted = arrhenius.func_arrhenius(tmp_CanoRate[0], *tmp_coeff)
	tmp_relaRMS = (tmp_fitted - tmp_CanoRate[1])/tmp_CanoRate[1]
	sh.write(index+3, tmp_col-5, tmp_name)
	sh.write(index+3, tmp_col-4, tmp_coeff[0])
	sh.write(index+3, tmp_col-3, tmp_coeff[1])
	sh.write(index+3, tmp_col-2, tmp_coeff[2])
	for i in range(len(tmp_CanoRate[0])):
		sh.write(tmp_row+i, tmp_col+5, tmp_relaRMS[i])
	tmp_ax.plot(1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_CanoRate[1][TRange[0]: TRange[1]]), 'bs', 1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'b-')

	if len(tmp_CanoRate) > 2:
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_CanoRate[0][TRange[0]: TRange[1]], tmp_CanoRate[2][TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse micro high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_CanoRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_CanoRate[2])/tmp_CanoRate[2]

		sh.write(index+3+totalNum+2, tmp_col-5, tmp_name)
		sh.write(index+3+totalNum+2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+totalNum+2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+totalNum+2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_CanoRate[0])):
			sh.write(tmp_row+i, tmp_col+6, tmp_relaRMS[i])
		tmp_ax2.plot(1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_CanoRate[2][TRange[0]: TRange[1]]), 'bs', 1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'b-')		

		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_CanoRate[0][TRange[0]: TRange[1]], tmp_Kc[TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse micro high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_CanoRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_Kc)/tmp_Kc	
		sh.write(index+3+(totalNum+2)*2, tmp_col-5, tmp_name)
		sh.write(index+3+(totalNum+2)*2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+(totalNum+2)*2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+(totalNum+2)*2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_CanoRate[0])):
			sh.write(tmp_row+i, tmp_col+7, tmp_relaRMS[i])
		tmp_ax3.plot(1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_Kc[TRange[0]: TRange[1]]), 'bs', 1000.0/tmp_CanoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'b-')

	tmp_col = 19
	sh.write(tmp_row, tmp_col, tmp_name)
	if len(tmp_TSTRate) > 2:
		tmp_Kc = tmp_TSTRate[1]/tmp_TSTRate[2]
	if tmp_num < len(tmp_TSTRate[0]):
		tmp_num = len(tmp_TSTRate[0]) 
	for i in range(len(tmp_TSTRate[0])):
		sh.write(tmp_row+i, tmp_col+1, tmp_TSTRate[0][i])
		sh.write(tmp_row+i, tmp_col+2, tmp_TSTRate[1][i])
		if len(tmp_TSTRate) > 2:
			sh.write(tmp_row+i, tmp_col+3, tmp_TSTRate[2][i])
			sh.write(tmp_row+i, tmp_col+4, tmp_Kc[i])

	TRange = phys1.TRangeIndex(tmp_TSTRate[0], 400, 900)
	tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_TSTRate[0][TRange[0]: TRange[1]], tmp_TSTRate[1][TRange[0]: TRange[1]], threshold = 5e-2)
	if rela_RMS > 5e-2:
		print 'reaction name:\t' + tmp_name + '\ttype:\tforward TST high-pressure rate fitting\n---'
	tmp_fitted = arrhenius.func_arrhenius(tmp_TSTRate[0], *tmp_coeff)
	tmp_relaRMS = (tmp_fitted - tmp_TSTRate[1])/tmp_TSTRate[1]
	sh.write(index+3, tmp_col-5, tmp_name)
	sh.write(index+3, tmp_col-4, tmp_coeff[0])
	sh.write(index+3, tmp_col-3, tmp_coeff[1])
	sh.write(index+3, tmp_col-2, tmp_coeff[2])
	for i in range(len(tmp_TSTRate[0])):
		sh.write(tmp_row+i, tmp_col+5, tmp_relaRMS[i])
	tmp_ax.plot(1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_TSTRate[1][TRange[0]: TRange[1]]), 'r*', 1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')

	if len(tmp_TSTRate) > 2:
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_TSTRate[0][TRange[0]: TRange[1]], tmp_TSTRate[2][TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse TST high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_TSTRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_TSTRate[2])/tmp_TSTRate[2]	
		sh.write(index+3+totalNum+2, tmp_col-5, tmp_name)
		sh.write(index+3+totalNum+2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+totalNum+2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+totalNum+2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_TSTRate[0])):
			sh.write(tmp_row+i, tmp_col+6, tmp_relaRMS[i])
		tmp_ax2.plot(1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_TSTRate[2][TRange[0]: TRange[1]]), 'r*', 1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')		

		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_TSTRate[0][TRange[0]: TRange[1]], tmp_Kc[TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse TST high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_TSTRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_Kc)/tmp_Kc	
		sh.write(index+3+(totalNum+2)*2, tmp_col-5, tmp_name)
		sh.write(index+3+(totalNum+2)*2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+(totalNum+2)*2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+(totalNum+2)*2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_TSTRate[0])):
			sh.write(tmp_row+i, tmp_col+7, tmp_relaRMS[i])
		tmp_ax3.plot(1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_Kc[TRange[0]: TRange[1]]), 'r*', 1000.0/tmp_TSTRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')

	tmp_col = 34
	sh.write(tmp_row, tmp_col, tmp_name)
	if len(tmp_PhenoRate) > 2:
		tmp_Kc = tmp_PhenoRate[1]/tmp_PhenoRate[2]
	if tmp_num < len(tmp_PhenoRate[0]):
		tmp_num = len(tmp_PhenoRate[0]) 
	for i in range(len(tmp_PhenoRate[0])):
		sh.write(tmp_row+i, tmp_col+1, tmp_PhenoRate[0][i])
		sh.write(tmp_row+i, tmp_col+2, tmp_PhenoRate[1][i])
		if len(tmp_PhenoRate) > 2:
			sh.write(tmp_row+i, tmp_col+3, tmp_PhenoRate[2][i])
			sh.write(tmp_row+i, tmp_col+4, tmp_Kc[i])

	TRange = phys1.TRangeIndex(tmp_PhenoRate[0], 400, 900)
	tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_PhenoRate[0][TRange[0]: TRange[1]], tmp_PhenoRate[1][TRange[0]: TRange[1]], threshold = 5e-2)
	if rela_RMS > 5e-2:
		print 'reaction name:\t' + tmp_name + '\ttype:\tforward phenomenological high-pressure rate fitting\n---'
	tmp_fitted = arrhenius.func_arrhenius(tmp_PhenoRate[0], *tmp_coeff)
	tmp_relaRMS = (tmp_fitted - tmp_PhenoRate[1])/tmp_PhenoRate[1]
	sh.write(index+3, tmp_col-5, tmp_name)
	sh.write(index+3, tmp_col-4, tmp_coeff[0])
	sh.write(index+3, tmp_col-3, tmp_coeff[1])
	sh.write(index+3, tmp_col-2, tmp_coeff[2])
	for i in range(len(tmp_PhenoRate[0])):
		sh.write(tmp_row+i, tmp_col+5, tmp_relaRMS[i])
	tmp_ax.plot(1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_PhenoRate[1][TRange[0]: TRange[1]]), 'gh', 1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'g-')

	if len(tmp_PhenoRate) > 2:
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_PhenoRate[0][TRange[0]: TRange[1]], tmp_PhenoRate[2][TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse phenomenological high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_PhenoRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_PhenoRate[2])/tmp_PhenoRate[2]	
		sh.write(index+3+totalNum+2, tmp_col-5, tmp_name)
		sh.write(index+3+totalNum+2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+totalNum+2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+totalNum+2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_PhenoRate[0])):
			sh.write(tmp_row+i, tmp_col+6, tmp_relaRMS[i])
		tmp_ax2.plot(1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_PhenoRate[2][TRange[0]: TRange[1]]), 'gh', 1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'g-')		

		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_PhenoRate[0][TRange[0]: TRange[1]], tmp_Kc[TRange[0]: TRange[1]], threshold = 5e-2)
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\treverse phenomenological high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_PhenoRate[0], *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_Kc)/tmp_Kc	
		sh.write(index+3+(totalNum+2)*2, tmp_col-5, tmp_name)
		sh.write(index+3+(totalNum+2)*2, tmp_col-4, tmp_coeff[0])
		sh.write(index+3+(totalNum+2)*2, tmp_col-3, tmp_coeff[1])
		sh.write(index+3+(totalNum+2)*2, tmp_col-2, tmp_coeff[2])
		for i in range(len(tmp_PhenoRate[0])):
			sh.write(tmp_row+i, tmp_col+7, tmp_relaRMS[i])
		tmp_ax3.plot(1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_Kc[TRange[0]: TRange[1]]), 'gh', 1000.0/tmp_PhenoRate[0][TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'g-')

	tmp_row += tmp_num+1

wb_new.save(name + '.xls')

tmp_fig.show()
tmp_fig2.show()
tmp_fig3.show()
tmp_fig.savefig('mesmer_rate_forward' + '.png',dpi=300)
tmp_fig2.savefig('mesmer_rate_reverse' + '.png',dpi=300)
tmp_fig3.savefig('mesmer_equilibrium constants' + '.png',dpi=300)
plt.close(tmp_fig)
plt.close(tmp_fig2)
plt.close(tmp_fig3)


print 'Mesmer output extracted and fiited successfully!\n'



