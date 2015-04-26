# READING--------------------------------------------------------------------------------------
from xlrd import *
import os
import re
import shutil
import numpy as np

import mesmer
import chem
import bathDatabase
import phys
import textExtractor

__barrier__ = True
__HR__ = False

# input region
mesmer1 = mesmer.mesmer('D:/hetanjin/professionalSoftware/Mesmer/Mesmer-3.0')
mesmer1.setGrainSize(20.0)
mesmer1.setEAboveTop(300.0)

# processing
name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[1].strip(' \n')
		if tmp_line == 'barrier':
			__barrier__ = True
			print '\n-------------------------------------\nbarrier reactions\n-------------------------------------\n'
		elif tmp_line == 'barrierless':
			__barrier__ = False
			print '\n-------------------------------------\nbarrierless reaction\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! Barrier or barrierless is not announced! Barrier is used as default!\n-------------------------------------\n'
		tmp_line = tmp_lines[7].strip(' \n')
		temperature = map(float, tmp_line.split())
		tmp_line = tmp_lines[9].strip(' \n')
		if tmp_line == 'no':
			__HR__ = False
			print '\n-------------------------------------\nhindered rotation correction not used\n-------------------------------------\n'
		elif tmp_line == 'yes':
			__HR__ = True
			print '\n-------------------------------------\nhindered rotation correction used\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! hindered rotation correction or not is not announced! Hindered rotation correction is not used as default!\n-------------------------------------\n'
		fr.close()

wb = open_workbook(name + '.xls')
sh = wb.sheet_by_name('SpeciesInfo')
sh2 = wb.sheet_by_name('SpeciesGeom')
sh3 = wb.sheet_by_name('SpeciesHessian')
sh4 = wb.sheet_by_name('HRNameMerge')

if __HR__ == True:
	wb_HR = open_workbook('HR_fit.xls')

phys1 = phys.phys()

# Define variables
total=int(sh.cell_value(1,0)) 		# Total number of activated reactions
reacs_line = 0  					# Total number of reactants line in excel, not equal to those in activated reactions, would changed while reading, it's used to count lines
prods_line = 0 						# Total number of products line in excel, not equal to those in activated reactions, would changed while reading, it's used to count lines
HR_dict = {}						# the dict of hindered rotations, including all the scanned rotations in HR_fit.xls
HRNameMerge_dict={} 				# the dict of file names need to be merged in case that different file name were given in hindered rotation scan 
# max_freq=75

# parameters of R 
name_R = []						# name abbreviation
filename_R = []					# name of the log without suffix
energy_R = []					# enthalpy of formation at 0 K in kcal/mol
rotConsts_R = []				# rotational constants in GHZ
RSN_R = []						# rotational symmetry number of R
multi_R = []					# multiplicity of R in ground sate
freq_R = []						# frequency array 
num_freq_R = []					# Frequency counter
formula_R = []					# chemical formula 
geom_R = [] 					# geometry structure in xyz
hessian_R = [] 					# hessian LT matrix 

# parameters of P 
name_P = []						# name abbreviation
filename_P = []					# name of the log without suffix
energy_P = []					# enthalpy of formation at 0 K in kcal/mol
rotConsts_P = []				# rotational constants in GHZ
RSN_P = []						# rotational symmetry number of R
multi_P = []					# multiplicity of R in ground sate
freq_P = []						# frequency array 
num_freq_P = []					# Frequency counter
formula_P = []					# chemical formula 
geom_P = [] 					# geometry structure in xyz
hessian_P = [] 					# hessian LT matrix 

# parameters of TS
name_TS = []					# name abbreviation
filename_TS = []				# name of the log without suffix
energy_TS = []					# enthalpy of formation at 0 K in kcal/mol
# reverse_barrier = []			# reverse barrier energy
rotConsts_TS = []				# rotational constants in GHZ
RSN_TS = []						# rotational symmetry number of TS
multi_TS = []					# multiplicity of TS in ground sate
i_freq_TS = []					# imaginary frequency array
freq_TS = []					# frequency array 
num_freq_TS = []				# Frequency counter
formula_TS = []					# chemical formula 
geom_TS = []					# geometry structure in xyz
hessian_TS = [] 				# hessian LT matrix

#temporary variables
tmp_name = []
tmp_filename = []
tmp_energy = []
tmp_formula = []
tmp_rotConsts = []
tmp_RSN = []
tmp_multi = []
tmp_num_freq = []
tmp_i_freq = []
tmp_freq=[]
tmp_geom = []
tmp_hessian = []

tmp2_freq = []
tmp2_geom = []
tmp2_hessian = []

tmp_num = 0
tmp_row = 0

# Read the information about HR file name merging 
tmp_row = 1
tmp_col = 2
while tmp_row < sh4.nrows: 	
	while tmp_col < sh4.ncols:
		if sh4.cell_value(tmp_row, tmp_col) != '':
			HRNameMerge_dict[sh4.cell_value(tmp_row, tmp_col)] = sh4.cell_value(tmp_row, 0)
			tmp_col += 1 
		else:
			break
	tmp_col = 2
	tmp_row += 1		

# Read the information about hindered rotation
if __HR__ == True:
	sheetsName_HR = [s.name for s in wb_HR.sheets()]
	for tmp_sheetName in sheetsName_HR:
		if re.match('.*_fit', tmp_sheetName):
			tmp_sheet = wb_HR.sheet_by_name(tmp_sheetName)
			num_rows = tmp_sheet.nrows
			for tmp_row in range(0, num_rows, 30):
				tmp_species = tmp_sheet.cell_value(tmp_row, 0)
				tmp_species = tmp_species[0:-4]
				if re.match('.*_[0-9]_scan', tmp_species):
					tmp_species = tmp_species[0:-7]
				if tmp_species in HRNameMerge_dict.keys():
					tmp_species = HRNameMerge_dict[tmp_species]
				tmp_rot = [int(tmp_sheet.cell_value(tmp_row+1,2)), int(tmp_sheet.cell_value(tmp_row+1,3)), tmp_sheet.cell_value(tmp_row+11,1), tmp_sheet.cell_value(tmp_row+12,1)]
				if tmp_species not in HR_dict.keys():
					HR_dict[tmp_species]=[tmp_rot]
				else:
					HR_dict[tmp_species].append(tmp_rot)

# Read the information about R
tmp_row = 3
while sh.cell_value(tmp_row,0) != '':
	reacs_line += 1

	if int(sh.cell_value(tmp_row,0)) != 0:
		tmp_name = []
		tmp_filename = []
		tmp_energy = []
		tmp_formula = []
		tmp_rotConsts = []
		tmp_RSN = []
		tmp_multi = []
		tmp_num_freq = []
		tmp_i_freq = []
		tmp_freq=[]
		tmp_geom = []
		tmp_hessian = []

		num_reac = int(int(sh.cell_value(tmp_row,0))/10);
		num_prod = int(sh.cell_value(tmp_row,0))%10;

		for i in range(num_reac):
			tmp_name.append(sh.cell_value(tmp_row,1))
			tmp_filename.append(sh.cell_value(tmp_row,2))
			tmp_energy.append(phys1.hartreeTokcalmol(float(sh.cell_value(tmp_row,3))))
			tmp_formula.append(sh.cell_value(tmp_row,10))
			if abs(float(sh.cell_value(tmp_row, 11)))>1e-2:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,11)),float(sh.cell_value(tmp_row,12)),float(sh.cell_value(tmp_row,13))])
			else:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,12))])
			tmp_rotConsts[-1] = phys1.GHZTocmm1(np.array(tmp_rotConsts[-1]))
			tmp_RSN.append(int(sh.cell_value(tmp_row,15)))
			tmp_multi.append(int(sh.cell_value(tmp_row,16)))
			tmp_num_freq.append(int(sh.cell_value(tmp_row,19)))

			tmp2_freq = []
			for tmp_col in range(tmp_num_freq[-1]): 
				tmp2_freq.append(float(sh.cell_value(tmp_row,21+tmp_col)))
			tmp_freq.append(tmp2_freq)
			
			tmp2_geom = []
			tmp_num = int(sh2.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_geom.append(sh2.cell_value(tmp2_row+3, tmp_row-2))
			tmp_geom.append(tmp2_geom)

			tmp2_hessian = []
			tmp_num = int(sh3.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_hessian.append(sh3.cell_value(tmp2_row+3, tmp_row-2))
			tmp_hessian.append(tmp2_hessian)

			tmp_row += 1

		name_R.append(tmp_name)
		filename_R.append(tmp_filename)
		energy_R.append(tmp_energy)
		formula_R.append(tmp_formula)
		rotConsts_R.append(tmp_rotConsts)
		RSN_R.append(tmp_RSN)
		multi_R.append(tmp_multi)
		num_freq_R.append(tmp_num_freq)
		freq_R.append(tmp_freq)
		geom_R.append(tmp_geom)
		hessian_R.append(tmp_hessian)

	else:
		tmp_row += 1

# read the information about P
tmp_row += 1
while sh.cell_value(tmp_row,0) != '':
	prods_line += 1

	if int(sh.cell_value(tmp_row,0)) != 0:
		tmp_name = []
		tmp_filename = []
		tmp_energy = []
		tmp_formula = []
		tmp_rotConsts = []
		tmp_RSN = []
		tmp_multi = []
		tmp_num_freq = []
		tmp_i_freq = []
		tmp_freq=[]
		tmp_geom = []
		tmp_hessian = []

		num_reac = int(int(sh.cell_value(tmp_row,0))/10);
		num_prod = int(sh.cell_value(tmp_row,0))%10;

		for i in range(num_prod):
			tmp_name.append(sh.cell_value(tmp_row,1))
			tmp_filename.append(sh.cell_value(tmp_row,2))
			tmp_energy.append(phys1.hartreeTokcalmol(float(sh.cell_value(tmp_row,3))))
			tmp_formula.append(sh.cell_value(tmp_row,10))
			if abs(float(sh.cell_value(tmp_row, 11)))>1e-2:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,11)),float(sh.cell_value(tmp_row,12)),float(sh.cell_value(tmp_row,13))])
			else:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,12))])
			tmp_rotConsts[-1] = phys1.GHZTocmm1(np.array(tmp_rotConsts[-1]))
			tmp_RSN.append(int(sh.cell_value(tmp_row,15)))
			tmp_multi.append(int(sh.cell_value(tmp_row,16)))
			tmp_num_freq.append(int(sh.cell_value(tmp_row,19)))

			tmp2_freq = []
			for tmp_col in range(tmp_num_freq[-1]): 
				tmp2_freq.append(float(sh.cell_value(tmp_row,21+tmp_col)))
			tmp_freq.append(tmp2_freq)
			
			tmp2_geom = []
			tmp_num = int(sh2.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_geom.append(sh2.cell_value(tmp2_row+3, tmp_row-2))
			tmp_geom.append(tmp2_geom)

			tmp2_hessian = []
			tmp_num = int(sh3.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_hessian.append(sh3.cell_value(tmp2_row+3, tmp_row-2))
			tmp_hessian.append(tmp2_hessian)

			tmp_row += 1

		name_P.append(tmp_name)
		filename_P.append(tmp_filename)
		energy_P.append(tmp_energy)
		formula_P.append(tmp_formula)
		rotConsts_P.append(tmp_rotConsts)
		RSN_P.append(tmp_RSN)
		multi_P.append(tmp_multi)
		num_freq_P.append(tmp_num_freq)
		freq_P.append(tmp_freq)
		geom_P.append(tmp_geom)
		hessian_P.append(tmp_hessian)

	else:
		tmp_row += 1

# read the information about TS
tmp_row += 1
while sh.cell_value(tmp_row,0) != '':
	if int(sh.cell_value(tmp_row,0)) != 0:
		tmp_name = []
		tmp_filename = []
		tmp_energy = []
		tmp_formula = []
		tmp_rotConsts = []
		tmp_RSN = []
		tmp_multi = []
		tmp_num_freq = []
		tmp_i_freq = []
		tmp_freq=[]
		tmp_geom = []
		tmp_hessian = []

		num_TS = 1

		for i in range(num_TS):
			tmp_name.append(sh.cell_value(tmp_row,1))
			tmp_filename.append(sh.cell_value(tmp_row,2))
			tmp_energy.append(phys1.hartreeTokcalmol(float(sh.cell_value(tmp_row,3))))
			tmp_formula.append(sh.cell_value(tmp_row,10))
			if abs(float(sh.cell_value(tmp_row, 11)))>1e-2:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,11)),float(sh.cell_value(tmp_row,12)),float(sh.cell_value(tmp_row,13))])
			else:
				tmp_rotConsts.append([float(sh.cell_value(tmp_row,12))])
			tmp_rotConsts[-1] = phys1.GHZTocmm1(np.array(tmp_rotConsts[-1]))
			tmp_RSN.append(int(sh.cell_value(tmp_row,15)))
			tmp_multi.append(int(sh.cell_value(tmp_row,16)))
			tmp_i_freq.append(float(sh.cell_value(tmp_row,18)))
			if not tmp_i_freq[-1] > 0:
				print 'Error! There is some problem with the imaginary frequency of ' + tmp_name[-1]	
			tmp_num_freq.append(int(sh.cell_value(tmp_row,19)))

			tmp2_freq = []
			for tmp_col in range(tmp_num_freq[-1]): 
				tmp2_freq.append(float(sh.cell_value(tmp_row,21+tmp_col)))
			tmp_freq.append(tmp2_freq)
			
			tmp2_geom = []
			tmp_num = int(sh2.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_geom.append(sh2.cell_value(tmp2_row+3, tmp_row-2))
			tmp_geom.append(tmp2_geom)

			tmp2_hessian = []
			tmp_num = int(sh3.cell_value(2, tmp_row-2))
			for tmp2_row in range(tmp_num):
				tmp2_hessian.append(sh3.cell_value(tmp2_row+3, tmp_row-2))
			tmp_hessian.append(tmp2_hessian)

			tmp_row += 1

		name_TS.append(tmp_name)
		filename_TS.append(tmp_filename)
		energy_TS.append(tmp_energy)
		formula_TS.append(tmp_formula)
		rotConsts_TS.append(tmp_rotConsts)
		RSN_TS.append(tmp_RSN)
		multi_TS.append(tmp_multi)
		i_freq_TS.append(tmp_i_freq)
		num_freq_TS.append(tmp_num_freq)
		freq_TS.append(tmp_freq)
		geom_TS.append(tmp_geom)
		hessian_TS.append(tmp_hessian)

	else:
		tmp_row += 1
	if tmp_row >= sh.nrows:
		break
		
print 'get reactions successfully!'


# WRITING --------------------------------------------------------------------------------------

total = len(name_TS)
if os.path.exists(os.getcwd()+'/mesmerInput'):
	shutil.rmtree(os.getcwd()+'/mesmerInput')
os.mkdir('mesmerInput')

for k in range(total):
	# Read from the existing template file	
	# write a the new .xml file for mesmer input
	tmp_reactants = []
	tmp_TSs = []
	tmp_products = []

	for i in range(len(name_R[k])):				
		tmp_reactant = chem.molecule(geom=geom_R[k][i])
		tmp_reactant.setRingBanned(True)
		tmp_reactant.fulfillBonds()
		tmp_reactant.setLabel(name_R[k][i])
		tmp_reactant.setZPE(energy_R[k][i])
		tmp_reactant.setRotConsts(rotConsts_R[k][i])
		tmp_reactant.setSymmetryNumber(RSN_R[k][i]) 
		# tmp_reactant.setFreqScaleFactor(1)
		tmp_reactant.setFrequencies(freq_R[k][i])
		tmp_reactant.setHessian(hessian_R[k][i])
		tmp_reactant.setSpinMultiplicity(multi_R[k][i])
		tmp_reactant.setEpsilon(500.0)
		tmp_reactant.setSigma(5.0)
		tmp_reactant.setExponentialDown(400.0)
		tmp_reactant.setDescription(formula_R[k][i] + ' ' + filename_R[k][i])
		tmp_reactant.setRole('modelled')
		tmp_bonds_actual = []
		tmp_bonds_ideal = []
		tmp_hinderedRotations = []
		if filename_R[k][i] not in HR_dict.keys():
			if __HR__ == True:
				print 'Error! There is no information for the hindered rotation of ' + filename_R[k][i]
		else:
			for tmp_rot in HR_dict[filename_R[k][i]]:
				tmp_axis = tmp_reactant.getBond(tmp_rot[0], tmp_rot[1])
				tmp_hinderedRot = chem.rotation(rotBondAxis=tmp_axis)
				tmp_angles = textExtractor.floatFromSummary(tmp_rot[2])
				tmp_angles = phys1.radTodegree(np.array(tmp_angles))
				tmp_energies = textExtractor.floatFromSummary(tmp_rot[3])
				tmp_hinderedRot.setPotential(tmp_angles, tmp_energies)
				tmp_bond = [tmp_rot[0], tmp_rot[1]]
				tmp_bond.sort()
				if not tmp_bond in tmp_bonds_actual:
					tmp_bonds_actual.append(tmp_bond)
					tmp_hinderedRotations.append(tmp_hinderedRot)
				else:
					print 'Error! There is a bond scanned more than once in hindered rotation processing!', tmp_bond
			tmp_rotations = tmp_reactant.getRotations()
			for tmp_rot in tmp_rotations:
				tmp_bond = [tmp_rot.rotBondAxis.atom1.label, tmp_rot.rotBondAxis.atom2.label]
				tmp_bond.sort()
				tmp_bonds_ideal.append(tmp_bond)
			tmp_bonds_actual.sort()
			tmp_bonds_ideal.sort()
			if tmp_bonds_actual != tmp_bonds_ideal:
				print 'Error! The actual hindered rotation is not the same as the theoretical analysis!'
				print '\tmolecule (reactant): ', tmp_reactant.label
				print '\tactual rotations: ', tmp_bonds_actual
				print '\ttheoretical rotations: ', tmp_bonds_ideal
		tmp_reactant.setHinderedRotorQM1D(tmp_hinderedRotations)
		tmp_reactants.append(tmp_reactant)

	for i in range(len(name_TS[k])):	
		tmp_TS = chem.molecule(geom=geom_TS[k][i])
		tmp_TS.setRingBanned(True)
		tmp_TS.fulfillBonds()
		tmp_TS.setLabel(name_TS[k][i])
		tmp_TS.setZPE(energy_TS[k][i])
		tmp_TS.setRotConsts(rotConsts_TS[k][i])
		tmp_TS.setSymmetryNumber(RSN_TS[k][i])
		# tmp_TS.setFreqScaleFactor(1)
		tmp_TS.setImfreq(i_freq_TS[k][i])
		tmp_TS.setFrequencies(freq_TS[k][i])
		tmp_TS.setHessian(hessian_TS[k][i])
		tmp_TS.setSpinMultiplicity(multi_TS[k][i])
		tmp_TS.setEpsilon(500.0)
		tmp_TS.setSigma(5.0)
		tmp_TS.setExponentialDown(400.0)
		# need to be completed
		# tmp_TS.setHinderedRotorQM1D() 
		tmp_TS.setDescription(formula_TS[k][i] + ' ' + filename_TS[k][i])
		tmp_TS.setRole('transitionState')
		tmp_bonds_actual = []
		tmp_bonds_ideal = []
		tmp_hinderedRotations = []
		if filename_TS[k][i] not in HR_dict.keys():
			if __HR__ == True:
				print 'Error! There is no information for the hindered rotation of ' + filename_TS[k][i]
		else:
			for tmp_rot in HR_dict[filename_TS[k][i]]:
				tmp_hinderedRot = chem.rotation(rotBondAxis=tmp_TS.getBond(tmp_rot[0], tmp_rot[1]))
				tmp_angles = textExtractor.floatFromSummary(tmp_rot[2])
				tmp_angles = phys1.radTodegree(np.array(tmp_angles))
				tmp_energies = textExtractor.floatFromSummary(tmp_rot[3])
				tmp_hinderedRot.setPotential(tmp_angles, tmp_energies)
				tmp_bond = [tmp_rot[0], tmp_rot[1]]
				tmp_bond.sort()
				if not tmp_bond in tmp_bonds_actual:
					tmp_bonds_actual.append(tmp_bond)
					tmp_hinderedRotations.append(tmp_hinderedRot)
				else:
					print 'Error! There is a bond scanned more than once in hindered rotation processing!', tmp_bond
			tmp_rotations = tmp_TS.getRotations()
			for tmp_rot in tmp_rotations:
				tmp_bond = [tmp_rot.rotBondAxis.atom1.label, tmp_rot.rotBondAxis.atom2.label]
				tmp_bond.sort()
				tmp_bonds_ideal.append(tmp_bond)
			tmp_bonds_actual.sort()
			tmp_bonds_ideal.sort()
			if tmp_bonds_actual != tmp_bonds_ideal:
				print 'Error! The actual hindered rotation is not the same as the theoretical analysis!'
				print '\tmolecule (TS): ', tmp_TS.label
				print '\tactual rotations: ', tmp_bonds_actual
				print '\ttheoretical rotations: ', tmp_bonds_ideal
		tmp_TS.setHinderedRotorQM1D(tmp_hinderedRotations)
		tmp_TSs.append(tmp_TS)

	for i in range(len(name_P[k])):	
		tmp_product = chem.molecule(geom=geom_P[k][i])
		tmp_product.setRingBanned(True)
		tmp_product.fulfillBonds()
		tmp_product.setLabel(name_P[k][i])
		tmp_product.setZPE(energy_P[k][i])
		tmp_product.setRotConsts(rotConsts_P[k][i])
		tmp_product.setSymmetryNumber(RSN_P[k][i]) 
		# tmp_product.setFreqScaleFactor(1)
		tmp_product.setFrequencies(freq_P[k][i])
		tmp_product.setHessian(hessian_P[k][i])
		tmp_product.setSpinMultiplicity(multi_P[k][i])
		tmp_product.setEpsilon(500.0)
		tmp_product.setSigma(5.0)
		tmp_product.setExponentialDown(400.0)
		tmp_product.setDescription(formula_P[k][i] + ' ' + filename_P[k][i])
		if len(name_P[k]) > 1:
			tmp_product.setRole('sink')
		else:
			tmp_product.setRole('modelled')
		tmp_bonds_actual = []
		tmp_bonds_ideal = []
		tmp_hinderedRotations = []
		if filename_P[k][i] not in HR_dict.keys():
			if __HR__ == True:
				print 'Error! There is no information for the hindered rotation of ' + filename_P[k][i]
		else:
			for tmp_rot in HR_dict[filename_P[k][i]]:
				tmp_axis = tmp_product.getBond(tmp_rot[0], tmp_rot[1])
				tmp_hinderedRot = chem.rotation(rotBondAxis=tmp_axis)
				tmp_angles = textExtractor.floatFromSummary(tmp_rot[2])
				tmp_angles = phys1.radTodegree(np.array(tmp_angles))
				tmp_energies = textExtractor.floatFromSummary(tmp_rot[3])
				tmp_hinderedRot.setPotential(tmp_angles, tmp_energies)
				tmp_bond = [tmp_rot[0], tmp_rot[1]]
				tmp_bond.sort()
				if not tmp_bond in tmp_bonds_actual:
					tmp_bonds_actual.append(tmp_bond)
					tmp_hinderedRotations.append(tmp_hinderedRot)
				else:
					print 'Error! There is a bond scanned more than once in hindered rotation processing!', tmp_bond
			tmp_rotations = tmp_product.getRotations()
			for tmp_rot in tmp_rotations:
				tmp_bond = [tmp_rot.rotBondAxis.atom1.label, tmp_rot.rotBondAxis.atom2.label]
				tmp_bond.sort()
				tmp_bonds_ideal.append(tmp_bond)
			tmp_bonds_actual.sort()
			tmp_bonds_ideal.sort()
			if tmp_bonds_actual != tmp_bonds_ideal:
				print 'Error! The actual hindered rotation is not the same as the theoretical analysis!'
				print '\tmolecule (product): ', tmp_product.label
				print '\tactual rotations: ', tmp_bonds_actual
				print '\ttheoretical rotations: ', tmp_bonds_ideal
		tmp_product.setHinderedRotorQM1D(tmp_hinderedRotations)
		tmp_products.append(tmp_product)
	
	tmp_reaction = chem.reaction(tmp_reactants, tmp_TSs, tmp_products)
	tmp_system = chem.reactionSystem()
	tmp_system.addReaction(tmp_reaction)
	tmp_system.setFreqScale(1.0)
	tmp_system.addBathGas(bathDatabase.useBathGas('He'))
	tmp_system.addPTpairs([[20, x] for x in temperature])
	tmp_system.hinderedRotationCorrection(__HR__)
	# if tmp_TS.label == 'TS_1_1b':
	mesmer1.genInput(tmp_system)

	shutil.move(tmp_TSs[0].label + '.xml', 'mesmerInput/' + tmp_TSs[0].label + '.xml')

print '\nMesmer input generated successfully!\n'		

# THE END


