import re
import os
import shutil
import numpy as np

import phys
import chem
import fourier
import mesmer
import textExtractor
import symCalc

__HR__ = True
__thermo__ = 'singleThermodynamic'

# input region
temperature=[298.15] + range(300, 1000, 50) + range(1100, 2500, 100)
mesmer1 = mesmer.mesmer('D:/hetanjin/professionalSoftware/Mesmer-4.0')
mesmer1.setGrainSize(50)
mesmer1.setEAboveTop(200.0)

PGPotential_dict={
'C/C/H3-C/C3/H':1095.1194735,
'C/C/H3-C/C2/H2':1080.32979104,
'C/C/H3-C/C/H3':1010.52741351,
'C/C2/H2-C/C2/H2':3077.65062581,
'C/C/H3-C/C4':1314.42848423,
'C/C3/H-C/C3/H':5727.71858707,
'C/C4-C/C4':1230.40881738,
'C/C2/H2-C/C3/H':3780.51269096,
'C/C2/H2-C/C4':3245.14287413,
'C/C3/H-C/C4':3487.46917136,
}

# constants
phys1 = phys.phys()
pattern_geomFileName = re.compile('^([CHO0-9]+_[0-9]+)_.*opt.*$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_freqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
# note that Input orientation should be used in MESMER rather than standard orientation when hessian used
pattern_input = re.compile('^.*Input orientation:.*$') 
# pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_SCFEnergy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *(-?[0-9]+\.[0-9]+) *A\.U\. after.*$')
pattern_freq = re.compile('^.*Frequencies -- *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)?$')
pattern_RSN = re.compile('^.*Rotational symmetry number *([0-9]+).*$')
pattern_rots = re.compile('^.*Rotational constants \(GHZ\): *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+)$')
pattern2_rots = re.compile('^.*Rotational constant \(GHZ\): *(-?[0-9]+\.[0-9]+)$')
pattern_ZPEEnergy = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
pattern_freqSum = re.compile('^.*\\\\Freq\\\\.*$')

anglesIndegree = np.array(range(0, 360, 10))*1.0
anglesInrad = phys1.degreeTorad(anglesIndegree)
PGPotentialCoeff_dict={}
PGPotentialCurve_dict={}
for tmp_rot in PGPotential_dict.keys():
	tmp_PG_V = PGPotential_dict[tmp_rot]
	tmp_PG_coeff_V_n1 = tmp_PG_V*np.array([0.5, -0.5, 0.0, 0.0])
	tmp_PG_coeff_V_n2 = tmp_PG_V*np.array([0.5, 0.0, -0.5, 0.0, 0.0, 0.0])
	tmp_PG_coeff_V_n3 = tmp_PG_V*np.array([0.5, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0])		
	PGPotentialCoeff_dict[tmp_rot] = [anglesIndegree, tmp_PG_coeff_V_n1, tmp_PG_coeff_V_n2, tmp_PG_coeff_V_n3]
	PGPotentialCurve_dict[tmp_rot] = [anglesIndegree, fourier.func_fourier(anglesInrad, *tmp_PG_coeff_V_n1), fourier.func_fourier(anglesInrad, *tmp_PG_coeff_V_n2), fourier.func_fourier(anglesInrad, *tmp_PG_coeff_V_n3)]

# target variables
mole_dict = {}

# read geom files
tmp_fileList = os.listdir('geom')
for tmp_file in tmp_fileList:
	tmp_m = pattern_geomFileName.match(tmp_file)
	if tmp_m:
		tmp_moleLabel = tmp_m.group(1)

		fr = file(os.path.join('geom', tmp_file), 'r')

		tmp_multi = 1
		tmp_energy = 0.0
		tmp_RSN = 1
		tmp_rotConsts = []
		tmp_freq = []
		tmp_hessian = []

		multi_done = -1
		freqCom_done = -1
		input_done = -1
		coordinate_done = -1
		energy_done = -1		
		freq_done = -1
		RSN_done = -1
		rots_done = -1
		freqSum_done = -1


		tmp_lines = fr.readlines()		
		for (lineNum, tmp_line) in enumerate(tmp_lines):
			if multi_done != 1:
				tmp_m = pattern_multi.match(tmp_line)
				if tmp_m:
					tmp_multi = int(tmp_m.group(1))
					multi_done = 1
			elif freqCom_done != 1:
				if lineNum < len(tmp_lines) - 1:
					tmp2_line = tmp_lines[lineNum].strip() + tmp_lines[lineNum+1].strip()
					tmp_m = pattern_freqCom.match(tmp2_line)
					if tmp_m:
						freqCom_done = 1
			elif input_done != 1:
				tmp_m = pattern_input.match(tmp_line)
				if tmp_m:
					tmp_num = lineNum + 5
					input_done = 1
			elif coordinate_done != 1:
				tmp_m = pattern_endline.match(tmp_line)
				if tmp_m:
					if lineNum > tmp_num:
						tmp_geom = tmp_lines[tmp_num: lineNum]
						coordinate_done = 1

			elif freq_done != 1:
				tmp_m = pattern_freq.match(tmp_line)
				if tmp_m:
					tmp_freq.extend(map(float,tmp_m.groups()))
					freq_done = 0
				if freq_done == 0:
					if re.search('Thermochemistry', tmp_line):
						while None in tmp_freq:
							tmp_freq.remove(None)
						freq_done = 1
			elif RSN_done != 1:
				tmp_m = pattern_RSN.match(tmp_line)
				if tmp_m:
					tmp_RSN = int(tmp_m.group(1))
					RSN_done = 1
			elif rots_done != 1:
				tmp_m = pattern_rots.match(tmp_line)
				if tmp_m:
					tmp_rotConsts = map(float,tmp_m.groups())
					tmp_rotConsts = phys1.GHZTocmm1(np.array(tmp_rotConsts))
					rots_done = 1
			elif energy_done != 1:
				tmp_m = pattern_ZPEEnergy.match(tmp_line)
				if tmp_m:
					tmp_energy = float(tmp_m.group(1))
					energy_done = 1
			elif freqSum_done != 1:
				if freqSum_done < 0:
					tmp_m = pattern_freqSum.match(tmp_line)
					if tmp_m:
						freqSum_done = 0
						tmp_num = lineNum
				elif tmp_line != '\n':
					continue
				else:
					tmp_hessian = textExtractor.hessianExtractor(tmp_lines[tmp_num: lineNum])
					if len(tmp_hessian) != (3*len(tmp_geom)*(3*len(tmp_geom)+1)/2):
						print 'Error! The size of hessian matrix does not equal to 3*N!'
					freqSum_done = 1
					break
		fr.close()



		tmp_mole = chem.molecule()
		tmp_mole.getLogGeom(tmp_geom)
		tmp_mole.setRingBanned(True)
		tmp_mole.fulfillBonds()
		tmp_mole.calcFormula()
		tmp_mole.setLabel(tmp_moleLabel)
		tmp_mole.setZPE(tmp_energy)
		tmp_mole.setRotConsts(tmp_rotConsts)
		tmp_mole.setFrequencies(tmp_freq)
		tmp_mole.setHessian(tmp_hessian)
		tmp_mole.setSpinMultiplicity(tmp_multi)
		tmp_mole.setEpsilon(500.0)
		tmp_mole.setSigma(5.0)
		tmp_mole.setExponentialDown(400.0)
		tmp_mole.setDescription(tmp_mole.formula + ' ' + tmp_mole.label)
		tmp_mole.setRole('forThermo')

		tmp_text = ''
		tmp_text += str(tmp_mole.getAtomsNum()) + '\n'
		tmp_text += ''.join([str(chem.eleLabelDict[x.symbol]) + ' ' + str(x.coordinate[0]) + ' ' + str(x.coordinate[1])+ ' ' + str(x.coordinate[2]) + '\n' for x in tmp_mole.atoms])
		tmp_text += '\n'
		tmp_result = symCalc.symCalcFromStr(tmp_text)
		tmp_RSN = chem.groupPointDict[tmp_result.pointGroup]
		tmp_mole.setSymmetryNumber(tmp_RSN)
		
		tmp_hinderedRotations = []
		tmp_groups = tmp_mole.get1stOrderGroup()
		tmp_groupDict = {}
		for tmp_atom in tmp_mole.atoms:
			if tmp_atom.symbol != 'H':
				tmp_groupDict[tmp_atom.label] = tmp_groups.pop(0)
		if len(tmp_groups) != 0:
			print 'Error! The number of groups is larger than the number of non-H atoms!'
		tmp_rotations = tmp_mole.getRotations()
		for i in xrange(len(tmp_rotations)):
			tmp_rot = tmp_rotations[i]
			tmp_list = sorted([tmp_groupDict[tmp_rot.rotBondAxis.atom1.label], tmp_groupDict[tmp_rot.rotBondAxis.atom2.label]])
			tmp_text = tmp_list[0] + '-' + tmp_list[1]
			if tmp_text not in PGPotential_dict.keys():
				print 'Error! Rotation ' + tmp_text + ' not in PGPotential_dict!'
			tmp_rot.detectPeriod()
			# tmp_rot.setPotential(PGPotentialCurve_dict[tmp_text][0], PGPotentialCurve_dict[tmp_text][tmp_rot.period])
			tmp_rot.setFourierCoefficients(PGPotentialCoeff_dict[tmp_text][tmp_rot.period])
			tmp_hinderedRotations.append(tmp_rot)
		tmp_mole.setHinderedRotorQM1D(tmp_hinderedRotations)			
		mole_dict[tmp_moleLabel] = tmp_mole

print len(mole_dict)

# # calculate external systry number, i.e. RSN
# allGroup = []
# for tmp_species in mole_dict.keys():
# 	tmp_text = ''
# 	tmp_text += str(mole_dict[tmp_species].getAtomsNum()) + '\n'
# 	tmp_text += ''.join([str(chem.eleLabelDict[x.symbol]) + ' ' + str(x.coordinate[0]) + ' ' + str(x.coordinate[1])+ ' ' + str(x.coordinate[2]) + '\n' for x in mole_dict[tmp_species].atoms])
# 	tmp_text += '\n'
# 	tmp_result = symCalc.symCalcFromStr(tmp_text)
# 	if chem.groupPointDict[tmp_result.pointGroup] != mole_dict[tmp_species].symmetryNumber:
# 		print tmp_species, chem.groupPointDict[tmp_result.pointGroup], mole_dict[tmp_species].symmetryNumber, chem.groupPointDict[tmp_result.pointGroup] - mole_dict[tmp_species].symmetryNumber
# 	allGroup.append(tmp_result.pointGroup)

# print set(allGroup)

# Mesmer input generation
if os.path.exists('mesmerInput'):
	shutil.rmtree('mesmerInput')
os.mkdir('mesmerInput')
for tmp_species in mole_dict.keys():
	tmp_reaction = chem.reaction([mole_dict[tmp_species]], [mole_dict[tmp_species]], [mole_dict[tmp_species]])
	tmp_system = chem.reactionSystem()
	tmp_system.addReaction(tmp_reaction)
	tmp_system.setFreqScale(0.977)
	tmp_system.hinderedRotationCorrection(__HR__)
	tmp_system.thermodynamic(__thermo__)
	mesmer1.genInput(tmp_system)
	shutil.move(tmp_species + '.xml', 'mesmerInput/' + tmp_species + '.xml')

print '\nMesmer input generated successfully!\n'		


