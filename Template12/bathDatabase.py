# This is a database for bath gas and usual molecules
# it should be write to a .xml file in the future if the database is much larger
import chem

moleBase = {}

tmp_mole = chem.molecule()
tmp_mole.setLabel('N2')
tmp_mole.addAtom(chem.atom('N',1))
tmp_mole.addAtom(chem.atom('N',2))
tmp_mole.addBond2(tmp_mole.atoms[0], tmp_mole.atoms[1], 3.0)
tmp_mole.setEpsilon(48.0)
tmp_mole.setSigma(3.90)
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('He')
tmp_mole.addAtom(chem.atom('He',1))
tmp_mole.setEpsilon(10.2)
tmp_mole.setSigma(2.55)
moleBase[tmp_mole.label] = tmp_mole

def useBathGas(bathGas):
	if bathGas not in moleBase.keys():
		print 'Error! The bath gas to be used is not in the database!', bathGas
		return None
	else:
		return moleBase[bathGas]

