# This is a database for bath gas and usual molecules
# it should be write to a .xml file in the future if the database is much larger
import chem
import phys
import re

# constants
phys1 = phys.phys()

moleBase = {}

tmp_mole = chem.molecule()
tmp_mole.setLabel('C')
tmp_mole.setDescription('gas-phase Carbon atom, charge: 0, multiplicity: 3')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
tmp_mole.setFormationH(171.2882409)
# tmp_mole.setFormationH(169.5)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -37.785377, 'B3LYP/6-31G(d)': -37.846280, 'M062X/def2TZVP': -37.842511})
tmp_mole.setRefH298({'CBS-QB3': -37.783017, 'B3LYP/6-31G(d)': -37.843920, 'M062X/def2TZVP': -37.840150})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('H2')
tmp_mole.setDescription('gas-phase H2, charge: 0, multiplicity: 1')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
tmp_mole.setFormationH(0)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -1.166083, 'B3LYP/6-31G(d)': -1.165337, 'M062X/def2TZVP': -1.158161})
tmp_mole.setRefH298({'CBS-QB3': -1.162778, 'B3LYP/6-31G(d)': -1.162033, 'M062X/def2TZVP': -1.154857})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('O2')
tmp_mole.setDescription('gas-phase O2, charge: 0, multiplicity: 3')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
tmp_mole.setFormationH(0)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -150.164604, 'B3LYP/6-31G(d)': -150.316263, 'M062X/def2TZVP': -150.323158})
tmp_mole.setRefH298({'CBS-QB3': -150.161296, 'B3LYP/6-31G(d)': -150.312956, 'M062X/def2TZVP': -150.319852})
moleBase[tmp_mole.label] = tmp_mole

def useThermoData(species):
	if species not in moleBase.keys():
		print 'Error! The species to be used is not in the thermodynamic database!', species
		return None
	else:
		return moleBase[species]

# unit: refEnthalpy0: a.u.
#		H298mH0: cal/mol
#		formationH: kcal/mol
# assume the formula is CxHyOz
# return the standard enthalpy of formation at 298.15 K 
def getFormationH(formula, refQMMethod, refEnthalpy0, H298mH0):
	pattern_element = re.compile('([A-Z][a-z]?)([0-9]*)')
	x = 0
	y = 0
	z = 0

	allElements = pattern_element.findall(formula)
	for tmp_element in allElements:
		if tmp_element[0] == 'C':
			if tmp_element[1] != '':
				x = int(tmp_element[1])
			else:
				x = 1
		elif tmp_element[0] == 'H':
			if tmp_element[1] != '':
				y = int(tmp_element[1])
			else:
				y = 1
		elif tmp_element[0] == 'O':
			if tmp_element[1] != '':
				z = int(tmp_element[1])
			else:
				z = 1
		else:
			print 'Error! The elements are more than C H and O!'
	if x+y+z==0:
		print 'Error! x+y+z can not be 0!'
	formationH = phys1.hartreeTokcalmol(refEnthalpy0 - x*moleBase['C'].refH298[refQMMethod] - y/2.0*moleBase['H2'].refH298[refQMMethod] - z/2.0*moleBase['O2'].refH298[refQMMethod]) + H298mH0/1000.0 + x*moleBase['C'].formationH 
	return formationH

# unit: NIST data: [cal][mol][k]
#		formationH298: kcal/mol
# assume the formula is CxHyOz
def NSSAH298Correction(NASACoeff, formationH298):
	NASA_lines = NASACoeff.split('\n')
	tmp_num = float(NASA_lines[2][0:15]) + formationH298*1000.0/phys1.JoulTocal(phys1.R)
	tmp_num = '%.7e' % tmp_num
	tmp_num = ' '*(15-len(tmp_num)) + tmp_num
	NASA_lines[2] = tmp_num + NASA_lines[2][15:]

	tmp_num = float(NASA_lines[3][30:45]) + formationH298*1000.0/phys1.JoulTocal(phys1.R)
	tmp_num = '%.7e' % tmp_num
	tmp_num = ' '*(15-len(tmp_num)) + tmp_num

	NASA_lines[3] = ''.join([NASA_lines[3][0:30], tmp_num, NASA_lines[3][45:60], ' '*15, NASA_lines[3][75:]]) 
	NASACoeff = '\n'.join(NASA_lines)
	return NASACoeff



