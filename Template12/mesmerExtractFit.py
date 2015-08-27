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
import thermoDatabase

__thermo__ = 'rate'

# open .name file to read the command and open workbook
name = ''
__energy__ = 'cbs'
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
		tmp_line = tmp_lines[3].strip(' \n')
		if tmp_line == 'cbs':
			__energy__ = 'cbs'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs energy is used to calculate the enthalpy of formation\n-------------------------------------\n'
		elif tmp_line == 'b3lyp':
			__energy__ = 'b3lyp'
			print '\n-------------------------------------\nb3lyp energy is used to calculate the enthalpy of formation\n-------------------------------------\n'
		elif tmp_line == 'cbsb3lyp':
			__energy__ = 'cbsb3lyp'
			print '\n-------------------------------------\ncbs verified and b3lyp energy in cbs computation is used to calculate the enthalpy of formation\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'		
		tmp_line = tmp_lines[5].strip(' \n')
		temperature = map(float, tmp_line.split())
		tmp_line = tmp_lines[11].strip('\n')
		tmp_line = map(int, tmp_line.split())
		fit_lowT = tmp_line[0]
		fit_highT = tmp_line[1]
		tmp_line = tmp_lines[13].strip(' \n')
		if tmp_line == 'thermodynamic':
			__thermo__ = 'thermodynamic'
			print '\n-------------------------------------\nthermodynamic data will be extracted\n-------------------------------------\n'
		elif tmp_line == 'singleThermodynamic':
			__thermo__ = 'singleThermodynamic'
			print '\n-------------------------------------\nthermodynamic data for single molecule will be extracted\n-------------------------------------\n'			
		elif tmp_line == 'rate':
			__thermo__ = 'rate'
			print '\n-------------------------------------\nrate constants will be extracted\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! thermodynamic or rate computation is not announced! Rate constants will be extracted as default!\n-------------------------------------\n'		
		fr.close()

wb=open_workbook(name + '.xls')
sheets=[s.name for s in wb.sheets()]

# constants
mesmer1 = mesmer.mesmer()
phys1 = phys.phys()
QMMethodDict = {'cbs': 'CBS-QB3', 'b3lyp': 'B3LYP/6-31G(d)'}
# the number of rows and columns of the displayed fitting figures
FIG_ROW = 6
FIG_COL = 5

# variables
num_reac=[]
num_prod=[]
TSs_abbr=[]
reactionsDict={}
tunnellingDict={}
absEnergyDict={}
relaEnergyDict={}
formulaDict={}
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
sh.cell_overwrite_ok = True
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
		reactionsDict[TSs_abbr[-1]].append(sh.cell_value(tmp_row, 3))
		tmp_prods = []
		for i in range(num_prod[-1]):
			tmp_prods.append(sh.cell_value(tmp_row, 11+i*4))
		reactionsDict[TSs_abbr[-1]].append(tmp_prods)


# write output data to excel, fit and draw or extract the thermodynamic data and the NASA coefficients
if __thermo__ == 'rate':
	wb_new = copy(wb)
	sh=wb_new.get_sheet(sheets.index('MesmerRate'))				#if overwrite to use cell_overwrite_ok=True
	sh.cell_overwrite_ok = True

	tmp_pic = 1
	tmp_fig = plt.figure(figsize=(22,12))
	tmp_fig2 = plt.figure(figsize=(22,12))
	tmp_fig3 = plt.figure(figsize=(22,12))
	tmp_figs = [tmp_fig]
	tmp_figs2 = [tmp_fig2]
	tmp_figs3 = [tmp_fig3] 

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
		if index >= (FIG_ROW*FIG_COL*tmp_pic):
			tmp_pic += 1
			tmp_fig = plt.figure(figsize=(22,12))
			tmp_fig2 = plt.figure(figsize=(22,12))
			tmp_fig3 = plt.figure(figsize=(22,12))
			tmp_figs.append(tmp_fig)
			tmp_figs2.append(tmp_fig2) 
			tmp_figs3.append(tmp_fig3)  
		tmp_num = 0
		tmp_name = tmp_file[4:-4]
		tmp_CanoRate, tmp_PhenoRate = mesmer1.readOutXml('mesmerOutput/' + tmp_file)
		tmp_TSTRate = mesmer1.readOutTest('mesmerOutput/' + tmp_name + '.test', thermodynamic = False)

		tmp_ax = tmp_fig.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
		tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
		tmp_ax.set_title(tmp_name)
		tmp_ax2 = tmp_fig2.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
		tmp_fig2.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
		tmp_ax2.set_title(tmp_name)	
		tmp_ax3 = tmp_fig3.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
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

	for i in range(tmp_pic):   
		tmp_figs[i].show()
		tmp_figs2[i].show()
		tmp_figs3[i].show()
		tmp_figs[i].savefig('mesmer_rate_forward' + '_' + str(i+1) + '.png',dpi=300)
		tmp_figs2[i].savefig('mesmer_rate_reverse' + '_' + str(i+1) + '.png',dpi=300)
		tmp_figs3[i].savefig('mesmer_equilibrium constants' + '_' + str(i+1) + '.png',dpi=300)
		plt.close(tmp_figs[i])
		plt.close(tmp_figs2[i])
		plt.close(tmp_figs3[i])

elif __thermo__ == 'thermodynamic':
	# read tunnelling effect
	sh=wb.sheet_by_name('TunnellingCoeff')
	num_rows = sh.nrows
	num_cols = sh.ncols

	tunnellingBegin_done = -1
	tunnellingEnd_done = -1

	for tmp_row in range(1,num_rows):
		if tunnellingBegin_done != 1:		
			if sh.cell_value(tmp_row, 0) != '':
				tmp_name = sh.cell_value(tmp_row, 0)
				tmp_tunnellingCoeff = {}
				tmp_tunnellingCoeff[float(sh.cell_value(tmp_row, 1))] = float(sh.cell_value(tmp_row, 2))
				tunnellingEnd_done = -1
				tunnellingBegin_done = 1
		elif tunnellingEnd_done != 1:			
			if sh.cell_value(tmp_row, 1) != '':
				tmp_tunnellingCoeff[float(sh.cell_value(tmp_row, 1))] = float(sh.cell_value(tmp_row, 2))
			if sh.cell_value(tmp_row, 1) == ''  or tmp_row+1 == num_rows:
				tunnellingDict[tmp_name] = tmp_tunnellingCoeff
				tunnellingBegin_done = -1
				tunnellingEnd_done = 1

	# read energy data
	sh=wb.sheet_by_name('SpeciesInfo')
	num_rows = sh.nrows
	num_cols = sh.ncols

	for tmp_row in range(3,num_rows):
		tmp_name = sh.cell_value(tmp_row, 1)
		if tmp_name != '':
			if tmp_name not in absEnergyDict.keys():
				absEnergyDict[tmp_name] = float(sh.cell_value(tmp_row, 3))
				formulaDict[tmp_name] = sh.cell_value(tmp_row, 10)
		if sh.cell_value(tmp_row, 4) == 'T':
			if tmp_name not in relaEnergyDict.keys():
				relaEnergyDict[tmp_name] = [-float(sh.cell_value(tmp_row, 7)), -float(sh.cell_value(tmp_row, 8))]

	# read and write thermodynamic data
	wb_new = copy(wb)
	sh = wb_new.get_sheet(sheets.index('thermodynamicData'))
	sh.cell_overwrite_ok = True

	os.chdir('mesmerOutput')
	pwd = os.getcwd()
	tmp_fileLists = os.listdir(pwd)
	tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('.test', tmp_file)]
	os.chdir('..')

	totalNum = len(tmp_fileLists)

	all_thermoData = []
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_names, tmp_temperatures, tmp_thermos, tmp_NASAs = mesmer1.readOutTest('mesmerOutput/' + tmp_file, thermodynamic = True)
		tmp_dict = {}
		for j in range(len(tmp_names)):
			tmp_dict[tmp_names[j]] = [tmp_temperatures[j], tmp_thermos[j], tmp_NASAs[j]]
		all_thermoData.append(tmp_dict)
		
	# write species data and rate and equilibrium constants
	tmp_row = 2
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_species = []
		tmp_species.append(reactionsDict[tmp_file[0:-5]][2])
		tmp_species.append(tmp_file[0:-5])
		tmp_species += reactionsDict[tmp_file[0:-5]][3]

		print all_thermoData[index].keys()
		tmp_deltaHs = [0.0]*len(all_thermoData[index][tmp_file[0:-5]][0])
		tmp_deltaSs = [0.0]*len(all_thermoData[index][tmp_file[0:-5]][0])

		# write species data
		tmp_col = 17
		for (index2, tmp_name) in enumerate(tmp_species):
			if tmp_name in all_thermoData[index].keys():
				sh.write(tmp_row, tmp_col, tmp_name)
				sh.write(tmp_row, tmp_col+6, all_thermoData[index][tmp_name][2])
				sh.write(tmp_row, tmp_col+7, ' ')
				for i in range(len(all_thermoData[index][tmp_name][0])):						
					sh.write(tmp_row, tmp_col+1, all_thermoData[index][tmp_name][0][i])
					sh.write(tmp_row, tmp_col+2, all_thermoData[index][tmp_name][1][0][i])
					sh.write(tmp_row, tmp_col+3, all_thermoData[index][tmp_name][1][1][i])
					sh.write(tmp_row, tmp_col+4, all_thermoData[index][tmp_name][1][2][i])
					sh.write(tmp_row, tmp_col+5, all_thermoData[index][tmp_name][1][3][i])
					if index2 < 1:
						tmp_deltaHs[i] -= all_thermoData[index][tmp_name][1][1][i]
						tmp_deltaSs[i] -= all_thermoData[index][tmp_name][1][2][i]
					elif index2 > 1:
						tmp_deltaHs[i] += all_thermoData[index][tmp_name][1][1][i]
						tmp_deltaSs[i] += all_thermoData[index][tmp_name][1][2][i]
					tmp_row += 1
				tmp_row -= len(all_thermoData[index][tmp_name][0])
			else:
				print 'Error! The thermodynamic data of ' + tmp_name + ' is missing!'
			tmp_col += 8 

		# write rate and equilibrium constants
		tmp_col = 9
		tmp_name = tmp_file[0: -5]
		sh.write(tmp_row, tmp_col, tmp_name)
		tmp_kfs = []
		tmp_krs = []
		tmp_Kcs = []
		for i in range(len(all_thermoData[index][tmp_name][0])):
			tmp_temperature = all_thermoData[index][tmp_name][0][i]
			sh.write(tmp_row, tmp_col+1, tmp_temperature)
			tmp_kf =  all_thermoData[index][tmp_name][1][0][i] / all_thermoData[index][tmp_species[0]][1][0][i]
			tmp_kf = phys1.k*tmp_temperature/phys1.h * all_thermoData[index][tmp_name][1][0][i] / all_thermoData[index][tmp_species[0]][1][0][i] * np.exp(-(0.0-phys1.calToJoul(1000.0*relaEnergyDict[tmp_name][0]))/phys1.R/tmp_temperature)
			sh.write(tmp_row, tmp_col+5, tmp_kf)
			if tmp_name in tunnellingDict.keys():
				if tmp_temperature in tunnellingDict[tmp_name].keys():
					tmp_kf *= tunnellingDict[tmp_name][tmp_temperature]
					sh.write(tmp_row, tmp_col+2, tmp_kf)
					tmp_kfs.append(tmp_kf)
			if tmp_name in relaEnergyDict.keys():
				# unit: [cal] [mol] [K]
				tmp_deltaHs[i] += 1000.0*(relaEnergyDict[tmp_name][1] - relaEnergyDict[tmp_name][0])
				tmp_K_theta = np.exp(-phys1.calToJoul((tmp_deltaHs[i] - tmp_temperature*tmp_deltaSs[i]))/phys1.R/tmp_temperature)
				tmp_Kc = tmp_K_theta * (phys1.atm/phys1.R/tmp_temperature*1e-6)**(reactionsDict[tmp_name][1] - reactionsDict[tmp_name][0])
				tmp_kr = tmp_kf/tmp_Kc
				sh.write(tmp_row, tmp_col+6, tmp_K_theta)
				sh.write(tmp_row, tmp_col+3, tmp_Kc)
				sh.write(tmp_row, tmp_col+4, tmp_kr)
				sh.write(tmp_row, tmp_col+7, phys1.calToJoul((tmp_deltaHs[i] - tmp_temperature*tmp_deltaSs[i])))
				tmp_krs.append(tmp_kr)
				tmp_Kcs.append(tmp_Kc)
			tmp_row += 1
		rate_f.append(tmp_kfs)
		rate_r.append(tmp_krs)
		Kconst.append(tmp_Kcs)		
		
		tmp_row += 1

	# write NASA format summary
	tmp_row = 2
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_species = []
		tmp_species.append(reactionsDict[tmp_file[0:-5]][2])
		tmp_species.append(tmp_file[0:-5])
		tmp_species += reactionsDict[tmp_file[0:-5]][3]

		tmp_col = 5 
		for tmp_name in tmp_species:
			if tmp_name in all_thermoData[index].keys():
				tmp_H298 = thermoDatabase.getFormationH(formulaDict[tmp_name], QMMethodDict[__energy__], absEnergyDict[tmp_name], all_thermoData[index][tmp_name][1][1][0])
				sh.write(tmp_row, tmp_col, tmp_name)
				sh.write(tmp_row, tmp_col+1, tmp_file[0:-5])
				sh.write(tmp_row, tmp_col+3, ' ')
				sh.write(tmp_row, tmp_col+2, thermoDatabase.NSSAH298Correction(all_thermoData[index][tmp_name][2], tmp_H298))
				tmp_row += 1
			else:
				print 'Error! The thermodynamic data of ' + tmp_name + ' is missing!' 
		tmp_row += 1

	# write fiiting coefficients and draw figures
	tmp_fig = plt.figure(figsize=(22,12))
	tmp_fig2 = plt.figure(figsize=(22,12))
	tmp_fig3 = plt.figure(figsize=(22,12))
	
	tmp_row = 2
	tmp_col = 0
	tmp_pic = 1 

	sh.write(tmp_row, tmp_col, 'kf')
	sh.write(tmp_row+len(tmp_fileLists)+2, tmp_col, 'kr')
	sh.write(tmp_row+(len(tmp_fileLists)+2)*2, tmp_col, 'Kc')
	
	tmp_row += 1
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_name = tmp_file[0:-5]

		if index >= (FIG_ROW*FIG_COL*tmp_pic):
			tmp_fig.savefig('mesmerThermo_rate_forward' + '_' + str(tmp_pic) + '.png',dpi=300)
			tmp_fig2.savefig('mesmerThermo_rate_reverse' + '_' + str(tmp_pic) + '.png',dpi=300)
			tmp_fig3.savefig('mesmerThermo_equilibrium constants' + '_' + str(tmp_pic) + '.png',dpi=300)
			tmp_fig.clf()
			tmp_fig2.clf()
			tmp_fig3.clf()
			tmp_pic += 1

		tmp_ax = tmp_fig.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
		tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
		tmp_ax.set_title(tmp_name)
		tmp_ax2 = tmp_fig2.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
		tmp_fig2.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
		tmp_ax2.set_title(tmp_name)	
		tmp_ax3 = tmp_fig3.add_subplot(FIG_ROW,FIG_COL,index+1-FIG_ROW*FIG_COL*(tmp_pic-1))
		tmp_fig3.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
		tmp_ax3.set_title(tmp_name)	

		tmp_x = np.array(all_thermoData[index][tmp_name][0])
		TRange = phys1.TRangeIndex(tmp_x, fit_lowT, fit_highT)

		tmp_y = np.array(rate_f[index])
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_x[TRange[0]: TRange[1]], tmp_y[TRange[0]: TRange[1]], threshold = 5e-2)		
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\tforward high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_x, *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_y)/tmp_y
		coeff_f.append(tmp_coeff)
		deviation_f.append(tmp_fitted - tmp_y)
		sh.write(tmp_row, tmp_col, tmp_name)
		sh.write(tmp_row, tmp_col+1, tmp_coeff[0])
		sh.write(tmp_row, tmp_col+2, tmp_coeff[1])
		sh.write(tmp_row, tmp_col+3, tmp_coeff[2])
		tmp_ax.plot(1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_y[TRange[0]: TRange[1]]), 'rs', 1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')

		tmp_y = np.array(rate_r[index])
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_x[TRange[0]: TRange[1]], tmp_y[TRange[0]: TRange[1]], threshold = 5e-2)		
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\rreverse high-pressure rate fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_x, *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_y)/tmp_y
		coeff_r.append(tmp_coeff)
		deviation_r.append(tmp_fitted - tmp_y)
		sh.write(tmp_row+len(tmp_fileLists)+2, tmp_col, tmp_name)
		sh.write(tmp_row+len(tmp_fileLists)+2, tmp_col+1, tmp_coeff[0])
		sh.write(tmp_row+len(tmp_fileLists)+2, tmp_col+2, tmp_coeff[1])
		sh.write(tmp_row+len(tmp_fileLists)+2, tmp_col+3, tmp_coeff[2])
		tmp_ax2.plot(1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_y[TRange[0]: TRange[1]]), 'rs', 1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')

		tmp_y = np.array(Kconst[index])
		tmp_coeff, tmp_deviation, rela_RMS = arrhenius.fit_arrhenius_noGuess(tmp_x[TRange[0]: TRange[1]], tmp_y[TRange[0]: TRange[1]], threshold = 5e-2)		
		if rela_RMS > 5e-2:
			print 'reaction name:\t' + tmp_name + '\ttype:\tequilibrium constant fitting\n---'
		tmp_fitted = arrhenius.func_arrhenius(tmp_x, *tmp_coeff)
		tmp_relaRMS = (tmp_fitted - tmp_y)/tmp_y
		coeff_K.append(tmp_coeff)
		deviation_K.append(tmp_fitted - tmp_y)
		sh.write(tmp_row+(len(tmp_fileLists)+2)*2, tmp_col, tmp_name)
		sh.write(tmp_row+(len(tmp_fileLists)+2)*2, tmp_col+1, tmp_coeff[0])
		sh.write(tmp_row+(len(tmp_fileLists)+2)*2, tmp_col+2, tmp_coeff[1])
		sh.write(tmp_row+(len(tmp_fileLists)+2)*2, tmp_col+3, tmp_coeff[2])
		tmp_ax3.plot(1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_y[TRange[0]: TRange[1]]), 'rs', 1000.0/tmp_x[TRange[0]: TRange[1]], np.log10(tmp_fitted[TRange[0]: TRange[1]]), 'r-')

		tmp_row+=1

	tmp_fig.savefig('mesmerThermo_rate_forward' + '_' + str(tmp_pic) + '.png',dpi=300)
	tmp_fig2.savefig('mesmerThermo_rate_reverse' + '_' + str(tmp_pic) + '.png',dpi=300)
	tmp_fig3.savefig('mesmerThermo_equilibrium constants' + '_' + str(tmp_pic) + '.png',dpi=300)
	tmp_fig.clf()
	tmp_fig2.clf()
	tmp_fig3.clf()
	plt.close(tmp_fig)
	plt.close(tmp_fig2)
	plt.close(tmp_fig3)		

	wb_new.save(name + '.xls')

elif __thermo__ == 'singleThermodynamic':
	# read energy data
	sh=wb.sheet_by_name('SpeciesInfo')
	num_rows = sh.nrows
	num_cols = sh.ncols

	for tmp_row in range(3,num_rows):
		tmp_name = sh.cell_value(tmp_row, 1)
		if tmp_name != '':
			if tmp_name not in absEnergyDict.keys():
				absEnergyDict[tmp_name] = float(sh.cell_value(tmp_row, 3))
				formulaDict[tmp_name] = sh.cell_value(tmp_row, 10)
		if sh.cell_value(tmp_row, 4) == 'T':
			if tmp_name not in relaEnergyDict.keys():
				relaEnergyDict[tmp_name] = [-float(sh.cell_value(tmp_row, 7)), -float(sh.cell_value(tmp_row, 8))]

	# read and write thermodynamic data
	wb_new = copy(wb)
	sh = wb_new.get_sheet(sheets.index('thermodynamicData'))
	sh.cell_overwrite_ok = True

	os.chdir('mesmerOutput')
	pwd = os.getcwd()
	tmp_fileLists = os.listdir(pwd)
	tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('.test', tmp_file)]
	os.chdir('..')

	totalNum = len(tmp_fileLists)

	all_thermoData = []
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_names, tmp_temperatures, tmp_thermos, tmp_NASAs = mesmer1.readOutTest('mesmerOutput/' + tmp_file, thermodynamic = True)
		tmp_dict = {}
		for j in range(len(tmp_names)):
			tmp_dict[tmp_names[j]] = [tmp_temperatures[j], tmp_thermos[j], tmp_NASAs[j]]
		all_thermoData.append(tmp_dict)
		
	# write species data and rate and equilibrium constants
	tmp_row = 2
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_species = []
		tmp_species.append(tmp_file[0:-5])

		print all_thermoData[index].keys()

		# write species data
		tmp_col = 17
		for (index2, tmp_name) in enumerate(tmp_species):
			if tmp_name in all_thermoData[index].keys():
				sh.write(tmp_row, tmp_col, tmp_name)
				sh.write(tmp_row, tmp_col+6, all_thermoData[index][tmp_name][2])
				sh.write(tmp_row, tmp_col+7, ' ')
				for i in range(len(all_thermoData[index][tmp_name][0])):						
					sh.write(tmp_row, tmp_col+1, all_thermoData[index][tmp_name][0][i])
					sh.write(tmp_row, tmp_col+2, all_thermoData[index][tmp_name][1][0][i])
					sh.write(tmp_row, tmp_col+3, all_thermoData[index][tmp_name][1][1][i])
					sh.write(tmp_row, tmp_col+4, all_thermoData[index][tmp_name][1][2][i])
					sh.write(tmp_row, tmp_col+5, all_thermoData[index][tmp_name][1][3][i])
					tmp_row += 1
			else:
				print 'Error! The thermodynamic data of ' + tmp_name + ' is missing!'
		tmp_row += 1 

	# write NASA format summary
	tmp_row = 2
	for (index, tmp_file) in enumerate(tmp_fileLists):
		tmp_species = []
		tmp_species.append(tmp_file[0:-5])

		tmp_col = 5 
		for tmp_name in tmp_species:
			if tmp_name in all_thermoData[index].keys():
				tmp_H298 = thermoDatabase.getFormationH(formulaDict[tmp_name], QMMethodDict[__energy__], absEnergyDict[tmp_name], all_thermoData[index][tmp_name][1][1][0])
				sh.write(tmp_row, tmp_col, tmp_name)
				sh.write(tmp_row, tmp_col+1, tmp_file[0:-5])
				sh.write(tmp_row, tmp_col+3, ' ')
				sh.write(tmp_row, tmp_col+2, thermoDatabase.NSSAH298Correction(all_thermoData[index][tmp_name][2], tmp_H298))
				tmp_row += 1
			else:
				print 'Error! The thermodynamic data of ' + tmp_name + ' is missing!' 
		tmp_row += 1

	wb_new.save(name + '.xls')

print 'Mesmer output extracted and fiited successfully!\n'



