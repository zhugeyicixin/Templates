# READING--------------------------------------------------------------------------------------

import numpy as np
from xlrd import *
from xlwt import *
import pyExcelerator
from xlutils.copy import copy
import re
import os
import shutil
import matplotlib.pyplot as plt

import phys
import fourier
import chem
import lamm
#input
name = 'rotation'

# symbol indicating the position
pattern_name = re.compile('^.*_scan_.*$')
pattern_atoms = re.compile('^.*D *([0-9]+) *([0-9]+) *([0-9]+) *([0-9]+).*S *([0-9]+) *(-?[0-9]+\.[0-9]+).*$')
pattern_energy = re.compile('^.*SCF Done:  E\([UR]?B3LYP\) = *(-?[0-9]+\.[0-9]+).*$')
# pattern_energy = re.compile('^.*SCF Done:  E\([UR]?PM6\) = *([\.\-Ee0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$') 
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_input = re.compile('^.*Input orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_normal = re.compile('^.*Normal termination of Gaussian 09.*$')

# constants
# the number of rows and columns of the displayed fitting figures
FIG_ROW = 6
FIG_COL = 5

# modules
phys1 = phys.phys()
lamm1 = lamm.lamm()

#variables
atoms = []
# energy in hatree
steps = 0
step_length = 0.0
energy = []	
# dihedral in degree
dihedral = []
energy_cmm1 = []
dihedral_rad = []
coeff_V = []
deviation_V =[]
geoms = []
atomsNum = 0 
inertia = []
rotConst = []
coeff_I = []
deviation_I = []
coeff_B = []
deviation_B = []

#flags
atoms_done = 0
energy_done = 0
optimized_done = 0
dihedral_done = 0 
standard_done = 0
coordinate_done = -1
geom_start = 0
geom_end = 0

# temporary variables
tmp_m = []
tmp_energy = 0.0
tmp_dihedral = 0.0
tmp_num = 0
tmp_page = 1
tmp_pic = 1

pwd = os.getcwd()
wb_new = Workbook()

pattern_blue = Pattern() # Create the Pattern
pattern_blue.pattern = Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern_blue.pattern_fore_colour = 49
style_blue = XFStyle() # Create the Pattern
style_blue.pattern = pattern_blue

if os.path.exists(pwd + '/' + 'lammInput'):
	shutil.rmtree('lammInput')
os.mkdir('lammInput')

if os.path.exists(pwd + '/' + 'lammOutput'):
	shutil.rmtree('lammOutput')
os.mkdir('lammOutput')

tmp_fileLists = os.listdir(pwd)
# traverse folders
for tmp_file in tmp_fileLists:
	if not os.path.isdir(pwd + '/' + tmp_file):
		continue
	tmp_pwd = pwd + '/' + tmp_file
	# print tmp_pwd

	# if target directory found
	if re.search(name,tmp_file):		
		sh = wb_new.add_sheet(tmp_file)
		sh_fit = wb_new.add_sheet(tmp_file + '_fit')
		tmp_page = 1
		tmp_pic = 1
		tmp_fig = plt.figure(figsize=(22,12))
		tmp_fig2 = plt.figure(figsize=(22,12))
		tmp_fig3 = plt.figure(figsize=(22,12))

		print '\n------------------------------------ ' + tmp_file + ' ----------------------------------------'


		os.mkdir('lammInput/' + tmp_file)

		os.mkdir('lammOutput/' + tmp_file)

		# traverse files
		tmp_fileLists2 = os.listdir(tmp_pwd)
		tmp_num = 0
		for tmp_file2 in tmp_fileLists2:
			if not re.search('\.log', tmp_file2):
				continue
			tmp_m = pattern_name.match(tmp_file2[0:-4])	
			# if target file found
			if tmp_m:
				print tmp_file2
				tmp_num = tmp_num + 1

				# extract data from scan log file
				atoms_done = 0
				energy_done = 0
				optimized_done = 0
				dihedral_done = 0
				standard_done = 0
				coordinate_done = -1

				atoms = []
				steps = 0
				step_length = 0.0
				energy = []	
				dihedral = []
				energy_cmm1 = []
				dihedral_rad = []
				coeff_V = []
				deviation_V =[]
				geoms = []
				atomsNum = 0
				inertia = []
				rotConst = []
				coeff_I = []
				deviation_I = []
				coeff_B = []
				deviation_B = []

				fr = file(tmp_pwd + '/' + tmp_file2,'r')
				tmp_lines = fr.readlines()
				for i in range(0,len(tmp_lines)):
					tmp_line = tmp_lines[i]
					if atoms_done != 1:
						tmp_m = pattern_atoms.match(tmp_line)
						if tmp_m:
							atoms = map(int,tmp_m.groups()[0:4])
							steps = int(tmp_m.group(5))
							step_length = float(tmp_m.group(6))
							pattern_dihedral = re.compile('^.*D\(' + str(atoms[0]) + ',' + str(atoms[1]) + ',' + str(atoms[2]) + ',' + str(atoms[3]) + '\) *(-?[0-9]+\.[0-9]+).*-DE/DX.*$')
							atoms_done = 1
					elif (standard_done != 1 or coordinate_done != 1 or energy_done != 1 or optimized_done != 1):
						if geom_start > 0 and coordinate_done != 1:
							atomsNum += 1
						# tmp_m = pattern_standard.match(tmp_line)
						tmp_m = pattern_input.match(tmp_line)						
						if tmp_m:
							geom_start = i + 5
							atomsNum = -5
							coordinate_done = 0
						if coordinate_done == 0:
							tmp_m = pattern_endline.match(tmp_line)
							if tmp_m:
								if i > geom_start:
									geom_end = i
									coordinate_done = 1
						tmp_m = pattern_energy.match(tmp_line)
						if tmp_m:
							tmp_energy = float(tmp_m.group(1))
						tmp_m = pattern_optimized.match(tmp_line)
						if tmp_m:	
							energy.append(tmp_energy)
							if (geom_end - geom_start) != atomsNum:
								print 'Warning! The number of atoms is not correct! The geometry of ' + str(tmp_dihedral+step_length) + ' is not reliable!'
							tmp_mole = chem.molecule()	
							tmp_mole.getLogGeom(tmp_lines[geom_start: geom_end])
							tmp_mole.setLabel(tmp_file2[0:-4])
							geoms.append(tmp_mole)
							dihedral_done = 0 
							standard_done = 1
							coordinate_done = 1
							energy_done = 1
							optimized_done = 1
					elif dihedral_done != 1:
						tmp_m = pattern_dihedral.match(tmp_line)
						if tmp_m:
							tmp_dihedral=float(tmp_m.group(1))
							if len(dihedral) > 0:
								if step_length >= 0 and (step_length - 45.0) < 1e-2:
									while tmp_dihedral < dihedral[-1]:
										tmp_dihedral += 360
								elif step_length < 0 and (step_length + 45.0) > -1e-2:
									while tmp_dihedral > dihedral[-1]:
										tmp_dihedral -= 360
								else:
									print 'Error! The absolute value of step length is larger than 45 degree!'

								# if abs(step_length - 10.0) < 1e-2:
								# 	while tmp_dihedral < dihedral[-1]:
								# 		tmp_dihedral = tmp_dihedral + 360
								# elif abs(step_length + 10.0) < 1e-2:
								# 	while tmp_dihedral > dihedral[-1]:
								# 		tmp_dihedral = tmp_dihedral - 360
								# else:
								# 	print 'Warning! The step length is neither 10 or -10 degree!'

							dihedral.append(tmp_dihedral)
							standard_done = 0
							coordinate_done = -1
							energy_done = 0
							optimized_done = 0
							dihedral_done = 1 
				tmp_m = pattern_normal.match(tmp_lines[-1])
				if not tmp_m:
					print 'Notice that job ' + tmp_file2 + ' did not end successfully!'
				# else:
					# print tmp_file2 + 'successfully!'

				# fit potential energy data
				dihedral = np.array(dihedral)
				energy = np.array(energy)

				if step_length < 0:
					dihedral = 360 - dihedral
				dihedral_rad = phys1.degreeTorad(dihedral)
				dihedral_rad = dihedral_rad - dihedral_rad[0]
				energy_cmm1 = phys1.hatreeTocmm1(energy)
				energy_cmm1 = energy_cmm1- energy_cmm1[0]
				# notice that the np.std is sqrt(sum((x-mean)^2)/n) rather than n-1
				coeff_V, deviation_V = fourier.fit_fourier_noGuess(dihedral_rad, energy_cmm1, threshold=np.std(energy_cmm1)/1e1)
				# coeff_V, deviation_V = fourier.fit_fourier(dihedral_rad, energy_cmm1)

				# generate lamm input files
				lamm1.genInput(geoms, dihedral, energy_cmm1)
				#run lamm
				lamm1.run()
				# extract lamm data
				lamm_dihedral, inertia, rotConst = lamm1.extractOutput()
				lamm_dihedral = np.array(lamm_dihedral)
				inertia = np.array(inertia)
				rotConst = np.array(rotConst)

				lamm1.rename(reFileName = tmp_file2[0: -4])
				shutil.move(tmp_file2[0: -4] + '.dat' ,'lammInput/' + tmp_file)
				shutil.move(tmp_file2[0: -4] + '.out', 'lammOutput/' + tmp_file)
				# fit lamm data I0s, B0s 
				# coeff_I, deviation_I = fourier.fit_cosFourier_noGuess(dihedral_rad, inertia, threshold=np.std(inertia))
				# coeff_B, deviation_B = fourier.fit_cosFourier_noGuess(dihedral_rad, rotConst, threshold=np.std(rotConst)/2)

				coeff_I, deviation_I = fourier.fit_cosFourier_noGuess(lamm_dihedral, inertia, n=6)
				coeff_B, deviation_B = fourier.fit_cosFourier_noGuess(lamm_dihedral, rotConst, n=6)

				# coeff_I, deviation_I = fourier.fit_cosFourier_noGuess(lamm_dihedral, inertia, threshold=np.std(inertia))
				# coeff_B, deviation_B = fourier.fit_cosFourier_noGuess(lamm_dihedral, rotConst, threshold=np.std(rotConst)/2)


				# write to excel
				# original data
				if tmp_num > (15*tmp_page) :
					tmp_page += 1
					sh = wb_new.add_sheet(tmp_file + ' (' + str(tmp_page) + ')')
				tmp_row = 0
				tmp_col = 0 + (tmp_num - 15 * (tmp_page-1) - 1) * 15

				sh.col(tmp_col).width = 0x1500
				sh.write(0, tmp_col+0, tmp_file2,style_blue)
				sh.write(1, tmp_col+0, 'atoms')
				sh.write(1, tmp_col+1, atoms[0])
				sh.write(1, tmp_col+2, atoms[1])
				sh.write(1, tmp_col+3, atoms[2])
				sh.write(1, tmp_col+4, atoms[3])
				tmp_row = 3
				sh.col(tmp_col+1).width = 0x0d00
				sh.col(tmp_col+3).width = 0x1000
				sh.col(tmp_col+4).width = 0x1400
				sh.col(tmp_col+5).width = 0x1400				
				sh.col(tmp_col+7).width = 0x1000
				sh.col(tmp_col+8).width = 0x1400
				sh.col(tmp_col+9).width = 0x1400
				sh.col(tmp_col+11).width = 0x1000
				sh.col(tmp_col+12).width = 0x1400
				sh.col(tmp_col+13).width = 0x1400
				sh.write(tmp_row, tmp_col+0, 'dihedral (degree)')
				sh.write(tmp_row, tmp_col+1, 'energy (hatree)')
				sh.write(tmp_row, tmp_col+3, 'relative dihedral (rad)')
				sh.write(tmp_row, tmp_col+4, 'relative energy (cm^-1)')
				sh.write(tmp_row, tmp_col+5, 'fit deviation_V (cm^-1)')
				sh.write(tmp_row, tmp_col+7, 'relative dihedral (rad)')
				sh.write(tmp_row, tmp_col+8, 'inertia (amu.A^2)')
				sh.write(tmp_row, tmp_col+9, 'fit deviation_I (amu.A^2)')
				sh.write(tmp_row, tmp_col+11, 'relative dihedral (rad)')
				sh.write(tmp_row, tmp_col+12, 'rot const (cm^-1)')
				sh.write(tmp_row, tmp_col+13, 'fit deviation_B (cm^-1)')

				tmp_row = 4
				for i in range(0,len(dihedral)):
					sh.write(tmp_row+i, tmp_col+0, dihedral[i])
					sh.write(tmp_row+i, tmp_col+1, energy[i])
					sh.write(tmp_row+i, tmp_col+3, dihedral_rad[i])
					sh.write(tmp_row+i, tmp_col+4, energy_cmm1[i])
					sh.write(tmp_row+i, tmp_col+5, deviation_V[i])
				for i in range(0,len(lamm_dihedral)):
					sh.write(tmp_row+i, tmp_col+7, lamm_dihedral[i])
					sh.write(tmp_row+i, tmp_col+8, inertia[i])
					sh.write(tmp_row+i, tmp_col+9, deviation_I[i])
					sh.write(tmp_row+i, tmp_col+11, lamm_dihedral[i])
					sh.write(tmp_row+i, tmp_col+12, rotConst[i])
					sh.write(tmp_row+i, tmp_col+13, deviation_B[i])

				# fitted data
				tmp_row2 = 0 + (tmp_num - 1) * 30
				tmp_col2 = 0
				sh_fit.col(0).width = 0x2000					
				sh_fit.write(tmp_row2, 0, tmp_file2, style_blue)
				tmp_row2 = tmp_row2 + 1
				sh_fit.write(tmp_row2, 0, 'atoms')
				sh_fit.write(tmp_row2, 1, atoms[0])
				sh_fit.write(tmp_row2, 2, atoms[1])
				sh_fit.write(tmp_row2, 3, atoms[2])
				sh_fit.write(tmp_row2, 4, atoms[3])
				tmp_row2 = tmp_row2 + 1
				sh_fit.write(tmp_row2+0, tmp_col2, 'relative dihedral (rad)')
				sh_fit.write(tmp_row2+1, tmp_col2, 'relative energy (cm^-1)')
				sh_fit.write(tmp_row2+2, tmp_col2, 'fit deviation_V (cm^-1)')
				sh_fit.write(tmp_row2+3, tmp_col2, 'relative dihedral (rad)')
				sh_fit.write(tmp_row2+4, tmp_col2, 'inertia (amu.A^2)')
				sh_fit.write(tmp_row2+5, tmp_col2, 'fit deviation_I (amu.A^2)')
				sh_fit.write(tmp_row2+6, tmp_col2, 'relative dihedral (rad)')
				sh_fit.write(tmp_row2+7, tmp_col2, 'rot const (cm^-1)')
				sh_fit.write(tmp_row2+8, tmp_col2, 'fit deviation_B (cm^-1)')				
				sh_fit.write(tmp_row2+9, tmp_col2, 'data summary')
				tmp_col2 = tmp_col2 + 1
				for i in range(0, len(dihedral)):
					sh_fit.write(tmp_row2+0, tmp_col2+i, '%.6f' % dihedral_rad[i])
					sh_fit.write(tmp_row2+1, tmp_col2+i, '%.6f' % energy_cmm1[i])
					sh_fit.write(tmp_row2+2, tmp_col2+i, '%.6f' % deviation_V[i])
				for i in range(0, len(lamm_dihedral)):
					sh_fit.write(tmp_row2+3, tmp_col2+i, '%.6f' % lamm_dihedral[i])
					sh_fit.write(tmp_row2+4, tmp_col2+i, '%.6f' % inertia[i])
					sh_fit.write(tmp_row2+5, tmp_col2+i, '%.6f' % deviation_I[i])
					sh_fit.write(tmp_row2+6, tmp_col2+i, '%.6f' % lamm_dihedral[i])
					sh_fit.write(tmp_row2+7, tmp_col2+i, '%.6f' % rotConst[i])
					sh_fit.write(tmp_row2+8, tmp_col2+i, '%.6f' % deviation_B[i])
				sh_fit.write(tmp_row2+9, tmp_col2, str(list(dihedral_rad)))
				sh_fit.write(tmp_row2+10, tmp_col2, str(list(energy_cmm1)))
				sh_fit.write(tmp_row2+11, tmp_col2, str(list(deviation_V)))
				sh_fit.write(tmp_row2+12, tmp_col2, str(list(lamm_dihedral)))
				sh_fit.write(tmp_row2+13, tmp_col2, str(list(inertia)))
				sh_fit.write(tmp_row2+14, tmp_col2, str(list(deviation_I)))
				sh_fit.write(tmp_row2+15, tmp_col2, str(list(lamm_dihedral)))
				sh_fit.write(tmp_row2+16, tmp_col2, str(list(rotConst)))
				sh_fit.write(tmp_row2+17, tmp_col2, str(list(deviation_B)))
				tmp_row2 = tmp_row2 + 18
				tmp_col2 = 0
				sh_fit.write(tmp_row2, tmp_col2, 'fitted V_a coefficients (c=0, a0, a1...)')
				sh_fit.write(tmp_row2+1, tmp_col2, 'fitted V_b coefficients (b1, b2...)')
				sh_fit.write(tmp_row2+2, tmp_col2, 'fitted I coefficients (c, a0, a1, a2...)')
				sh_fit.write(tmp_row2+3, tmp_col2, 'fitted B coefficients (c, a0, a1, a2...)')
				tmp_col2 = tmp_col2 + 1
				for i in range(0, len(coeff_V)/2):
					sh_fit.write(tmp_row2, tmp_col2+i, coeff_V[i])
					if i > 0:
						sh_fit.write(tmp_row2+1, tmp_col2+i, coeff_V[i+len(coeff_V)/2])
				for (i, x) in enumerate(coeff_I):
					sh_fit.write(tmp_row2+2, tmp_col2+i, x)
				for (i, x) in enumerate(coeff_B):
					sh_fit.write(tmp_row2+3, tmp_col2+i, x)
				tmp_row2 = tmp_row2 + 4
				tmp_col2 = 0
				sh_fit.write(tmp_row2, tmp_col2, 'fitted parameters summary')
				tmp_row2 = tmp_row2 + 1
				sh_fit.write(tmp_row2, tmp_col2, str(atoms[1]) + ' ' + str(atoms[2]))
				tmp_row2 = tmp_row2 + 1
				sh_fit.row(tmp_row2+0).set_style(style_blue)
				sh_fit.row(tmp_row2+1).set_style(style_blue)
				sh_fit.row(tmp_row2+2).set_style(style_blue)
				sh_fit.write(tmp_row2+0, tmp_col2+0, 0, style_blue)
				sh_fit.write(tmp_row2+0, tmp_col2+1, 'hrd', style_blue)
				sh_fit.write(tmp_row2+1, tmp_col2+1, 'Vhrd3', style_blue)
				sh_fit.write(tmp_row2+2, tmp_col2+1, 'Ihrd1', style_blue)
				tmp_col2 = tmp_col2 + 2
				sh_fit.write(tmp_row2, tmp_col2+0, len(coeff_V)-1, style_blue)
				sh_fit.write(tmp_row2, tmp_col2+1, len(coeff_I)-1, style_blue)
				sh_fit.write(tmp_row2, tmp_col2+2, 1, style_blue)
				sh_fit.write(tmp_row2+1, tmp_col2+0, 1, style_blue)
				sh_fit.write(tmp_row2+1, tmp_col2+1, '0.0', style_blue)
				sh_fit.write(tmp_row2+2, tmp_col2+0, 1, style_blue)
				for i in range(0, len(coeff_V)):
					if i < len(coeff_V)/2:
						sh_fit.write(tmp_row2+1, tmp_col2+2+i, '%.6f' % coeff_V[i], style_blue)
					elif i > len(coeff_V)/2:
						sh_fit.write(tmp_row2+1, tmp_col2+1+i, '%.6f' % coeff_V[i], style_blue)
				for (i,x) in enumerate(coeff_I):
					sh_fit.write(tmp_row2+2, tmp_col2+1+i, x, style_blue)

				# draw figures
				if tmp_num > (FIG_ROW*FIG_COL*tmp_pic):
					tmp_fig.savefig('V' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
					tmp_fig2.savefig('I' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
					tmp_fig3.savefig('B' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
					tmp_fig.clf()
					tmp_fig2.clf()
					tmp_fig3.clf()
					tmp_pic += 1

				tmp_ax = tmp_fig.add_subplot(FIG_ROW,FIG_COL,tmp_num - FIG_ROW*FIG_COL*(tmp_pic-1))
				tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
				tmp_ax.plot(dihedral_rad, energy_cmm1, 'b*', dihedral_rad, fourier.func_fourier(dihedral_rad,*coeff_V),'r-')
				tmp_ax.set_title(tmp_file2)
				tmp_ax2 = tmp_fig2.add_subplot(FIG_ROW,FIG_COL,tmp_num - FIG_ROW*FIG_COL*(tmp_pic-1))
				tmp_fig2.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
				tmp_ax2.plot(lamm_dihedral, inertia, 'b*', dihedral_rad, fourier.func_cosFourier(dihedral_rad,*coeff_I),'r-')
				tmp_ax2.set_title(tmp_file2)
				tmp_ax3 = tmp_fig3.add_subplot(FIG_ROW,FIG_COL,tmp_num - FIG_ROW*FIG_COL*(tmp_pic-1))
				tmp_fig3.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
				tmp_ax3.plot(lamm_dihedral, rotConst, 'b*', dihedral_rad, fourier.func_cosFourier(dihedral_rad,*coeff_B),'r-')
				tmp_ax3.set_title(tmp_file2)			

		tmp_fig.savefig('V' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
		tmp_fig2.savefig('I' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
		tmp_fig3.savefig('B' + tmp_file + '_' + str(tmp_pic) + '.png',dpi=300)
		tmp_fig.clf()
		tmp_fig2.clf()
		tmp_fig3.clf()
		plt.close(tmp_fig)
		plt.close(tmp_fig2)
		plt.close(tmp_fig3)

if os.path.exists('HR_fit.xls'):
	os.remove('HR_fit.xls')
wb_new.save('HR_fit.xls')
print 'hindered rotation data extracted successfully!'

# THE END


