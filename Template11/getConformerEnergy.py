# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os
import xlsxwriter

######################################
#useful self defined functions 
######################################
def rotAtomsCmp(atomsString1,atomsString2):
	atoms1 = map(int, atomsString1.split(','))
	atoms2 = map(int, atomsString2.split(','))
	if atoms1[1] < atoms2[1]:
		return	-1
	elif atoms1[1] == atoms2[1]:
		if atoms1[2] < atoms2[2]:
			return -1
		elif atoms1[2] == atoms2[2]:
			if atoms1[0] < atoms2[0]:
				return -1
			elif atoms1[0] == atoms2[0]:
				if atoms1[3] < atoms2[3]:
					return -1
				elif atoms1[3] == atoms2[3]:
					return 0
	return 1				

def molEnergyDihedralCmp(mole1, mole2, allDihedral):
	# enthalpy_1 = mole1[1][3] - mole1[1][2] + 0.977 * (mole1[1][2] - mole1[1][0]) + mole1[1][0]
	# enthalpy_2 = mole2[1][3] - mole2[1][2] + 0.977 * (mole2[1][2] - mole2[1][0]) + mole2[1][0]
	# energyDiff = enthalpy_1 - enthalpy_2
	energyDiff = (mole1[1][0] - mole2[1][0])
	if energyDiff < -2.0E-6:
		return -1
	elif energyDiff < 2.0E-6:
		for tmp_dihedral in allDihedral:
			if tmp_dihedral not in mole1[1][4].keys():
				if tmp_dihedral in mole2[1][4].keys():
					return -1
				else:
					continue
			elif tmp_dihedral not in mole2[1][4].keys():
				return 1
			else:
				dihedralDiff = mole1[1][4][tmp_dihedral] - mole2[1][4][tmp_dihedral]
				if dihedralDiff < -2.0E-1:
					return -1
				elif dihedralDiff < 2.0E-1:
					continue
				else:
					return 1
	return 1


###################
#extract data
###################

#definition of goal parameters
rotAxes = []
molDict = {}

#definetion of comparing pattern
pattern_torsion = re.compile('^#torsion.*$')
pattern_rotAxis = re.compile('^ *([0-9]+) *([0-9]+)$')
# pattern_energy = re.compile('^.*SCF Done: *E\([UR]PM6\) *= *([-\.eE0-9]+) *A.U. after.*$')
# pattern_energy = re.compile('^.*SCF Done: *E\([UR]B3LYP\) *= *(-?[0-9]+\.[0-9]+) *A.U. after.*$')
pattern_energy = re.compile('^.*SCF Done: *E\([UR]M062X\) *= *(-?[0-9]+\.[0-9]+) *A.U. after.*$')
pattern_optimized = re.compile('^.* Optimized Parameters.*$')
pattern_dihedral = re.compile('^.*D[0-9]+ * D\(([0-9]+),([0-9]+),([0-9]+),([0-9]+)\) *([-\.0-9]+) *-DE/DX.*$')
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
# pattern_MP4 = re.compile('^.*#P Geom=AllCheck Guess=TCheck SCRF=Check MP4SDQ/CBSB4.*$')
# pattern_energy = re.compile('^.*QCISD\(T\)= *(-?[0-9]+\.[0-9]+)D\+(-?[0-9]+).*$')
pattern_zpe = re.compile('^.*Zero-point correction= *(-?[0-9]+\.[0-9]+) *\(Hartree/Particle\) *.*$')
pattern_energy0K = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_enthalpy298K = re.compile('^.*Sum of electronic and thermal Energies= *(-?[0-9]+\.[0-9]+).*$')
# pattern_energy = re.compile('^.*E2 =    -0.2898122586D+.*$')

#flags
SCFEnergy_done = -1
optimized_done = -1
dihedral_done = -1
endline_done = -1
ZPEEnergy_done = -1
Energy0K_done = -1
Enthalpy298K_done = -1

# temporary variables
SCFEnergy = 0.0
ZPEEnergy = 0.0
energy0K = 0.0
enthalpy298K = 0.0
tmp_row = 0

# extract info from .rot
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
rotExist = False
for tmp_file in tmp_fileLists:
	if re.search('.rot', tmp_file):
		print tmp_file
		rotExist = True
		torsionStart_done = -1
		torsionEnd_done = -1

		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		for tmp_line in tmp_lines:
			if torsionStart_done != 1:
				tmp_m = pattern_torsion.match(tmp_line)
				if tmp_m:
					torsionStart_done = 1
					torsionEnd_done = -1
			elif torsionEnd_done != 1:
				tmp_m = pattern_rotAxis.match(tmp_line)
				if tmp_m:
					rotAxes.append(sorted(map(int,tmp_m.groups())))
					torsionEnd_done = 1
					torsionStart_done = -1
		fr.close()
if rotExist == False:
	print 'Error! .rot file not found!'
print rotAxes

#extract info from .log
# os.chdir('tmpCBSFiles')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.log',tmp_file):
		print tmp_file
		
		SCFEnergy = 0.0
		ZPEEnergy = 0.0
		energy0K = 0.0
		enthalpy298K = 0.0

		SCFEnergy_done = -1
		optimized_done = -1
		dihedral_done = -1
		endline_done = -1
		ZPEEnergy_done = -1
		Energy0K_done = -1
		Enthalpy298K_done = -1

		if tmp_file[0:-4] in molDict.keys():
			print 'Error! Molecule ' + tmp_file[0:-4] + ' has already existed in molDict!'
		else:
			molDict[tmp_file[0:-4]] = [0.0, 0.0, 0.0, 0.0, {}]

		fr=file(tmp_file,'r')
		for tmp_line in fr.readlines():
			if SCFEnergy_done != 1 and optimized_done != 1:
				tmp_m = pattern_energy.match(tmp_line)
				if tmp_m:
					SCFEnergy = float(tmp_m.group(1))
				tmp_m = pattern_optimized.match(tmp_line)
				if tmp_m:
					molDict[tmp_file[0:-4]][0] = SCFEnergy
					SCFEnergy_done = 1
					optimized_done = 1
			elif dihedral_done != 1 and endline_done != 1:
				tmp_m = pattern_dihedral.match(tmp_line)
				if tmp_m:
					tmp_atoms = map(int, tmp_m.groups()[0:4])
					tmp_dihedral = float(tmp_m.groups()[4])
					if sorted(tmp_atoms[1:3]) in rotAxes:
						tmp_atom0 = str(sorted([tmp_atoms[0], tmp_atoms[3]])[0])
						tmp_atom1 = str(sorted([tmp_atoms[1], tmp_atoms[2]])[0])
						tmp_atom2 = str(sorted([tmp_atoms[1], tmp_atoms[2]])[1])						
						tmp_atom3 = str(sorted([tmp_atoms[0], tmp_atoms[3]])[1])
						molDict[tmp_file[0:-4]][4][','.join([tmp_atom0, tmp_atom1, tmp_atom2, tmp_atom3])] = tmp_dihedral
					dihedral_done = 0
				if dihedral_done == 0:
					tmp_m = pattern_endline.match(tmp_line)
					if tmp_m:
						dihedral_done = 1
						endline_done = 1
			elif ZPEEnergy_done != 1:
				tmp_m = pattern_zpe.match(tmp_line)
				if tmp_m:
					ZPEEnergy = float(tmp_m.group(1))
					molDict[tmp_file[0:-4]][1] = ZPEEnergy
					ZPEEnergy_done = 1
			elif Energy0K_done != 1:
				tmp_m = pattern_energy0K.match(tmp_line)
				if tmp_m:
					energy0K = float(tmp_m.group(1))
					molDict[tmp_file[0:-4]][2] = energy0K
					Energy0K_done = 1
			elif Enthalpy298K_done != 1:
				tmp_m = pattern_enthalpy298K.match(tmp_line)
				if tmp_m:
					enthalpy298K = float(tmp_m.group(1))
					molDict[tmp_file[0:-4]][3] = enthalpy298K
					Enthalpy298K_done = 1

###################
#write data
###################
# write info to excel

wb_new = xlsxwriter.Workbook('tmpConformerEnergy.xlsx')
sh = wb_new.add_worksheet('energy')
format1 = wb_new.add_format()
format1.set_bg_color('yellow')

tmp_row = 0
sh.write(tmp_row,0,'name')
# sh.write(tmp_row,1,'zpe')
# sh.write(tmp_row,2,'energy without zpe')
sh.write(tmp_row, 1, 'energy without zpe')
sh.write(tmp_row, 2, 'zpe')
sh.write(tmp_row, 3, 'energy with zpe at 0 K')
sh.write(tmp_row, 4, 'enthalpy at 298 K without scaling factor')
sh.write(tmp_row, 5, 'enthalpy at 298 K with scaling factor')
sh.write(tmp_row, 7, 'diheral (atoms and angles)')
tmp_row += 1
allDihedral = set()
for tmp_mol in molDict.keys():
	allDihedral = allDihedral | set(molDict[tmp_mol][4].keys())
allDihedral = sorted(list(allDihedral), cmp=rotAtomsCmp)
sortedMols = sorted(list(molDict.items()), cmp=lambda x,y: molEnergyDihedralCmp(x,y,allDihedral))

dihedralIndex = {}
for (index, tmp_dihedral) in enumerate(allDihedral):
	sh.write(tmp_row, 7+index, tmp_dihedral)
	dihedralIndex[tmp_dihedral] = 7+index
tmp_row += 1

for (tmp_molIndex, tmp_mol) in enumerate(sortedMols):
	sh.write(tmp_row, 0, tmp_mol[0])
	# sh.write(tmp_row,1,zpe)
	# sh.write(tmp_row,2,energy-zpe)
	sh.write(tmp_row, 1, tmp_mol[1][0])
	if tmp_molIndex > 0:
		if abs(tmp_mol[1][0] - sortedMols[tmp_molIndex-1][1][0]) < 2.0E-6:
			sh.write(tmp_row, 1, tmp_mol[1][0], format1)

	sh.write(tmp_row, 2, tmp_mol[1][1])
	sh.write(tmp_row, 3, tmp_mol[1][2])
	sh.write(tmp_row, 4, tmp_mol[1][3])
	sh.write(tmp_row, 5, tmp_mol[1][3] - tmp_mol[1][2] + 0.977 * (tmp_mol[1][2] - tmp_mol[1][0]) + tmp_mol[1][0])	
			
	for tmp_dihedral in tmp_mol[1][4].keys():
		sh.write(tmp_row, dihedralIndex[tmp_dihedral],tmp_mol[1][4][tmp_dihedral])
		if tmp_molIndex > 0 and tmp_dihedral in sortedMols[tmp_molIndex-1][1][4].keys():
			if abs(tmp_mol[1][4][tmp_dihedral] - sortedMols[tmp_molIndex-1][1][4][tmp_dihedral]) < 2.0E-1:
				sh.write(tmp_row, dihedralIndex[tmp_dihedral],tmp_mol[1][4][tmp_dihedral], format1)

	tmp_row += 1
		# break
wb_new.close()
print 'energy data extracted successfully!'


# THE END


