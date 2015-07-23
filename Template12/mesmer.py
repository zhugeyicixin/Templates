# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import numpy as np
from lxml import etree
import visual
import fourier
import phys
import matplotlib.pyplot as plt
from scipy import stats
from collections import OrderedDict

import chem

phys1 = phys.phys()

# units: 
# grainSize: cm-1
# energyAboveTheTopHill: kT
class mesmer:
	location = ''
	nsmap = {None: 'http://www.xml-cml.org/schema','me': 'http://www.chem.leeds.ac.uk/mesmer', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
	grainSize = 100
	eAboveTop = 100.0

	rotPotentCheckFigs=[]
	rotPotentCheckFIG_ROW = 6
	rotPotentCheckFIG_COL = 5
	rotPotentCheckFig_index = 0

	pattern_xmlCanRate = re.compile('^.*Canonical rate coefficients.*$')
	pattern_TSTRate_f = re.compile('^.*Canonical.*first order forward rate constant.*= *([\-\.\+eE0-9]+).*\(([\-\.\+eE0-9]+) *K\).*$')
	pattern_TSTRate_r = re.compile('^.*Canonical.*first order backward rate constant.*= *([\-\.\+eE0-9]+).*\(([\-\.\+eE0-9]+) *K\).*$')
	pattern_thermoBegin = re.compile('^.*thermodynamic data based on qtot begin: *([\_A-Za-z0-9]+).*$')
	pattern_testThermo = re.compile('^.*temperature Q, H\(T\)-H\(0\), S, and Cp.*: *([\-\.\+eE0-9]+) *([\-\.\+eE0-9]+) *([\-\.\+eE0-9]+) *([\-\.\+eE0-9]+) *([\-\.\+eE0-9]+).*$')
	pattern_thermoEnd = re.compile('^.*thermodynamic data based on qtot end: *([A-Za-z0-9_]+).*$')
	pattern_testNASA1 = re.compile('^.*[0-9]+\.[0-9]* *[0-9]+\.[0-9]* *[0-9]+\.[0-9]*.*1$')
	pattern_testNASA2 = re.compile('^.*[\-\.\+eE0-9]+ *[\-\.\+eE0-9]+ *[\-\.\+eE0-9]+ *[\-\.\+eE0-9]+ *[\-\.\+eE0-9]+ *2$')

	def __init__(self, location=''):
		self.location = location
		self.nsmap = OrderedDict(zip([None, 'me', 'xsi'], ['http://www.xml-cml.org/schema', 'http://www.chem.leeds.ac.uk/mesmer', 'http://www.w3.org/2001/XMLSchema-instance']))
		self.grainSize = 50
		self.eAboveTop = 200.0

	def setGrainSize(self, grainSize):
		self.grainSize = grainSize

	def setEAboveTop(self, eAboveTop):
		self.eAboveTop = eAboveTop

	def angleDependPotentCheck(self, angles, energies, description=''):
		dihedral = np.array(angles)
		dihedral_rad = phys1.degreeTorad(dihedral)
		dihedral_rad = dihedral_rad - dihedral_rad[0]

		energy_cmm1 = np.array(energies)
		energy_cmm1 = energy_cmm1- energy_cmm1[0]

		step_length = dihedral_rad[1] - dihedral_rad[0]
		cycle_size = 2.0 * np.pi / step_length
		useFittedData = False

		if (round(cycle_size) > len(dihedral_rad)):
			print 'Error! Hindered rotation check in mesmer! Input data is shorter than a whole cycle!'
		if abs(cycle_size - round(cycle_size)) > 1e-2:
			print 'Error! Hindered rotation check in mesmer! A cycle 360 degree is not a integral multiple of the step length!'

		cycle_size = int(round(cycle_size))
		refined_angles = angles[0: cycle_size]
		refined_energies = energies[0: cycle_size]

		if abs(dihedral_rad[cycle_size-1] - dihedral_rad[0] - 2*np.pi*35.0/36.0) > 1e-2:
			print 'Warning! Hindered rotation check in mesmer! Fitted data used!'
			print 'There are possibly some pointes missing in a cycle! x[round(cycle_size)-1] - x[0] != 2*np.pi!'
			print cycle_size, abs(dihedral_rad[cycle_size-1] - dihedral_rad[0] - 2*np.pi)
	
			useFittedData = True		
			
			
			coeff_V, deviation_V = fourier.fit_fourier_noGuess(dihedral_rad, energy_cmm1, threshold=np.std(energy_cmm1)/1e1)

			mesmer.rotPotentCheckFig_index += 1
			if mesmer.rotPotentCheckFig_index > mesmer.rotPotentCheckFIG_ROW * mesmer.rotPotentCheckFIG_COL:
				mesmer.rotPotentCheckFig_index = 1
			if mesmer.rotPotentCheckFig_index == 1:
				tmp_fig = plt.figure(figsize=(22, 12))
				mesmer.rotPotentCheckFigs.append(tmp_fig)
			tmp_fig = mesmer.rotPotentCheckFigs[-1]
			tmp_ax = tmp_fig.add_subplot(mesmer.rotPotentCheckFIG_ROW, mesmer.rotPotentCheckFIG_COL, mesmer.rotPotentCheckFig_index)
			tmp_fig.subplots_adjust(left=0.04,bottom=0.04,right=0.98,top=0.96,wspace=0.2,hspace=0.4)
			tmp_ax.plot(dihedral_rad, energy_cmm1, 'b*', dihedral_rad, fourier.func_fourier(dihedral_rad,*coeff_V),'r-')
			tmp_ax.set_title(description)
			tmp_fig.savefig('HRUseFittedData_' + str(len(mesmer.rotPotentCheckFigs)) + '.png', dpi=300)
			plt.close(tmp_fig)

			det_dihedral = dihedral[1:] - dihedral[0:-1]
			det_dihedral = np.round(det_dihedral)
			step_length = stats.mode(det_dihedral)
			step_length = step_length[0][0]
			cycle_size = 360.0 / step_length
			cycle_size = int(round(cycle_size))
			refined_angles = np.array(range(cycle_size)) * step_length
			dihedral_rad = phys1.degreeTorad(refined_angles)
			refined_energies = fourier.func_fourier(dihedral_rad,*coeff_V)
			refined_energies = refined_energies - refined_energies[0]

		return refined_angles, refined_energies, useFittedData


	def genInput(self, reactSys):
		allMolecule = []

		if self.location != '':
			tmpnode_href1 = etree.ProcessingInstruction('xml-stylesheet', 'type=\'text/xsl\' href=\'file:///' + self.location + '/mesmer1.xsl\' media=\'screen\'')
			tmpnode_href2 = etree.ProcessingInstruction('xml-stylesheet', 'type=\'text/xsl\' href=\'file:///' + self.location + '/mesmer2.xsl\' media=\'other\'')
		else:
			tmpnode_href1 = etree.ProcessingInstruction('xml-stylesheet', 'type=\'text/xsl\' href=\'../../mesmer1.xsl\' media=\'screen\'')
			tmpnode_href2 = etree.ProcessingInstruction('xml-stylesheet', 'type=\'text/xsl\' href=\'../../mesmer2.xsl\' media=\'other\'')
		root_mesmer = etree.Element('{%s}mesmer' % self.nsmap['me'], nsmap = self.nsmap)
		inputFile = etree.ElementTree(root_mesmer)
		root_mesmer.addprevious(tmpnode_href2)
		root_mesmer.addprevious(tmpnode_href1)
		
		node_moleculeList = meEtree.orderedSubElement(root_mesmer, 'moleculeList')
		
		for reaction in reactSys.reactions:
			for tmp_molecule in reaction.reactants + reaction.TSs + reaction.products:
				if tmp_molecule.label in allMolecule:
					continue
				else:
					allMolecule.append(tmp_molecule.label)

				if reactSys._thermodynamic == False:
					tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id','description'], [tmp_molecule.label, tmp_molecule.description])
				elif tmp_molecule.role == 'transitionState':
					tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id', 'role', 'description'], [tmp_molecule.label, 'transitionState', tmp_molecule.description])
				else:
					tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id', 'role','description'], [tmp_molecule.label, 'forThermo', tmp_molecule.description])
				
				tmpnode_atom = meEtree.orderedSubElement(tmpnode_mole, 'atomArray')
				for tmp_atom in tmp_molecule.atoms:
					meEtree.orderedSubElement(tmpnode_atom, 'atom', ['id', 'elementType', 'x3', 'y3', 'z3'], [tmp_atom.symbol+str(tmp_atom.label), tmp_atom.symbol, str(tmp_atom.coordinate[0]), str(tmp_atom.coordinate[1]), str(tmp_atom.coordinate[2])])
				
				tmpnode_bond = meEtree.orderedSubElement(tmpnode_mole, 'bondArray')
				for (index, tmp_bond) in enumerate(tmp_molecule.bonds):
					meEtree.orderedSubElement(tmpnode_bond, 'bond', ['id', 'atomRefs2', 'order'], ['b'+str(index+1), ''.join([tmp_bond.atom1.symbol, str(tmp_bond.atom1.label), ' ', tmp_bond.atom2.symbol, str(tmp_bond.atom2.label)]), str(tmp_bond.bondOrder)])
				
				tmpnode_propertyList = meEtree.orderedSubElement(tmpnode_mole, 'propertyList')
				
				if reactSys._thermodynamic == False:
					tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:ZPE'])
					tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['kcal/mol'])
					tmpnode_scalar.text = str(tmp_molecule.ZPE)
				else:
					tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:Hf298'])
					tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units', 'convention'], ['kcal/mol', 'thermodynamic298K'])
					tmpnode_scalar.text = '0.0'

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:rotConsts'])
				tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
				tmpnode_array.text = ''.join([str(x) + ' ' for x in tmp_molecule.rotConsts])
				
				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:symmetryNumber'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text = str(tmp_molecule.symmetryNumber)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:frequenciesScaleFactor'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text	= str(reactSys.freqScaleFactor)

				if abs(tmp_molecule.imfreq) > 1e-2:
					tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:imFreqs'])
					tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['cm-1'])
					tmpnode_scalar.text = str(tmp_molecule.imfreq)

				if len(tmp_molecule.atoms) > 2:
					tmpnode_property = meEtree.orderedElement('property', ['dictRef'], ['me:vibFreqs'])
					tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
					tmpnode_array.text = ''.join([str(x) + ' ' for x in tmp_molecule.frequencies])
					tmpnode_comment = etree.Comment(etree.tostring(tmpnode_property, pretty_print=True))
					tmpnode_propertyList.append(tmpnode_comment)

					tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['title', 'dictRef'], ['Hessian', 'me:hessian'])
					tmpnode_matrix = meEtree.orderedSubElement(tmpnode_property, 'matrix', ['rows', 'matrixType', 'units'], [str(tmp_molecule.getAtomsNum()*3), 'squareSymmetricLT', 'Hartree/Bohr2'])
					tmpnode_matrix.text = ''.join([str(x) + ' ' for x in tmp_molecule.hessian])
				else:
					tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:vibFreqs'])
					tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
					tmpnode_array.text = ''.join([str(x) + ' ' for x in tmp_molecule.frequencies])

					tmpnode_property = meEtree.orderedElement('property', ['title', 'dictRef'], ['Hessian', 'me:hessian'])
					tmpnode_matrix = meEtree.orderedSubElement(tmpnode_property, 'matrix', ['rows', 'matrixType', 'units'], [str(tmp_molecule.getAtomsNum()*3), 'squareSymmetricLT', 'Hartree/Bohr2'])
					tmpnode_matrix.text = ''.join([str(x) + ' ' for x in tmp_molecule.hessian])
					tmpnode_comment = etree.Comment(etree.tostring(tmpnode_property, pretty_print=True))
					tmpnode_propertyList.append(tmpnode_comment)


				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:MW'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['amu'])
				tmpnode_scalar.text = str(tmp_molecule.getWeight())

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:spinMultiplicity'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text	= str(tmp_molecule.spinMultiplicity)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:epsilon'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text = str(tmp_molecule.epsilon)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:sigma'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text = str(tmp_molecule.sigma)

				tmpnode_energyTrans = meEtree.orderedSubElement(tmpnode_mole, '{%s}energyTransferModel' % self.nsmap['me'], ['{%s}type' % self.nsmap['xsi']], ['me:ExponentialDown'])
				tmpnode_deltaE = meEtree.orderedSubElement(tmpnode_energyTrans, '{%s}deltaEDown' % self.nsmap['me'], ['units'], ['cm-1'])
				tmpnode_deltaE.text = str(tmp_molecule.exponentialDown)

				tmpnode_DOSCMethod = meEtree.orderedSubElement(tmpnode_mole, '{%s}tmpnode_DOSCMethod' % self.nsmap['me'], ['name'], ['ClassicalRotors'])

				if reactSys._hinderedRotation == True:
					for tmp_hinderRotor in tmp_molecule.hinderedRotorQM1D:
						tmpnode_ExtraDOSC = meEtree.orderedSubElement(tmpnode_mole, '{%s}ExtraDOSCMethod' % self.nsmap['me'], ['{%s}type' % self.nsmap['xsi']], ['HinderedRotorQM1D'])
						tmpnode_bond = meEtree.orderedSubElement(tmpnode_ExtraDOSC, '{%s}bondRef' % self.nsmap['me'])
						tmpnode_bond.text = 'b'+str(tmp_molecule.bonds.index(tmp_hinderRotor.rotBondAxis)+1)
						tmpnode_potential = meEtree.orderedSubElement(tmpnode_ExtraDOSC, '{%s}HinderedRotorPotential' % self.nsmap['me'], ['format', 'units', 'expansionSize', 'UseSineTerms', 'scale'], ['numerical', 'cm-1', '9', 'yes', '1'])
						
						tmp_angles, tmp_energies, tmp_refined = self.angleDependPotentCheck(tmp_hinderRotor.angles, tmp_hinderRotor.energies, description=''.join([tmp_molecule.label, '[' , str(tmp_hinderRotor.rotBondAxis.atom1.label), ',', str(tmp_hinderRotor.rotBondAxis.atom2.label), ']']))
						if tmp_refined:
							print 'Warning! Fitted data used in mesmer hindered rotation input!', tmp_molecule.label, '[' , str(tmp_hinderRotor.rotBondAxis.atom1.label), ',', str(tmp_hinderRotor.rotBondAxis.atom2.label), ']'
						for (index, tmp_angle) in enumerate(tmp_angles):
							tmpnode_point = meEtree.orderedSubElement(tmpnode_potential, '{%s}PotentialPoint' % self.nsmap['me'], ['angle', 'potential'], [str(tmp_angle), str(tmp_energies[index])])

						if tmp_hinderRotor.period != 1:
							tmpnode_period = meEtree.orderedSubElement(tmpnode_ExtraDOSC, '{%s}periodicity' % self.nsmap['me'])
							tmpnode_period.text = str(tmp_hinderRotor.period)
						tmpnode_calcMOI = meEtree.orderedSubElement(tmpnode_ExtraDOSC, '{%s}CalculateInternalRotorInertia' % self.nsmap['me'], ['phaseDifference'], ['0.0'])


			if len(reaction.products) > 1 and reactSys._thermodynamic == False:
				tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id','description'],[(''.join([x.label + '+' for x in reaction.products]))[0:-1], 'a mix of all products to deal with the case that the number of products is larger than 1'])
								
				tmpnode_propertyList = meEtree.orderedSubElement(tmpnode_mole, 'propertyList')
				
				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:ZPE'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['kcal/mol'])
				tmpnode_scalar.text = str(sum([x.ZPE for x in reaction.products]))

				tmpnode_comment = etree.Comment('Note that the rotational constants come form the first product because it would not be used in the calculation')
				tmpnode_propertyList.append(tmpnode_comment)
				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:rotConsts'])
				tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
				tmpnode_array.text = ''.join([str(x) + ' ' for x in reaction.products[0].rotConsts])

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:frequenciesScaleFactor'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text	= str(reactSys.freqScaleFactor)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:vibFreqs'])
				tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
				tmp_array = []
				for tmp_molecule in reaction.products:
					tmp_array += tmp_molecule.frequencies
				tmpnode_array.text = ''.join([str(x) + ' ' for x  in tmp_array])

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:MW'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['amu'])
				tmpnode_scalar.text = str(sum([x.getWeight() for x in reaction.products]))

		if reactSys._thermodynamic == False:
			for tmp_bathGas in reactSys.bathGas:
				tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id'], [tmp_bathGas.label])
				tmpnode_atom = meEtree.orderedSubElement(tmpnode_mole, 'atomArray')
				for tmp_atom in tmp_bathGas.atoms:
					meEtree.orderedSubElement(tmpnode_atom, 'atom', ['id', 'elementType'], [tmp_atom.symbol+str(tmp_atom.label), tmp_atom.symbol])

				if len(tmp_bathGas.bonds) > 0:
					tmpnode_bond = meEtree.orderedSubElement(tmpnode_mole, 'bondArray')
					for tmp_bond in tmp_bathGas.bonds:
						meEtree.orderedSubElement(tmpnode_bond, 'bond', ['atomRefs2', 'order'], [''.join([tmp_bond.atom1.symbol, str(tmp_bond.atom1.label), ' ', tmp_bond.atom2.symbol, str(tmp_bond.atom2.label)]), str(tmp_bond.order)])

				tmpnode_propertyList = meEtree.orderedSubElement(tmpnode_mole, 'propertyList')
				
				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:epsilon'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text = str(tmp_bathGas.epsilon)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:sigma'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar')
				tmpnode_scalar.text = str(tmp_bathGas.sigma)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:MW'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['amu'])
				tmpnode_scalar.text = str(tmp_bathGas.getWeight())

		if reactSys._thermodynamic == False:
			node_reactionList = meEtree.orderedSubElement(root_mesmer, 'reactionList')

			for (index, reaction) in enumerate(reactSys.reactions):
				tmpnode_reaction = meEtree.orderedSubElement(node_reactionList, 'reaction', ['id'], ['R'+str(index+1)])

				for tmp_reactant in reaction.reactants:
					tmpnode_reactant = meEtree.orderedSubElement(tmpnode_reaction, 'reactant')
					tmpnode_molecule = meEtree.orderedSubElement(tmpnode_reactant, 'molecule', ['ref', 'role'], [tmp_reactant.label, tmp_reactant.role])

				if len(reaction.products) > 1:
					tmpnode_product = meEtree.orderedSubElement(tmpnode_reaction, 'product')
					tmpnode_molecule = meEtree.orderedSubElement(tmpnode_product, 'molecule', ['ref', 'role'], [(''.join([x.label + '+' for x in reaction.products]))[0:-1],'sink'])
				for tmp_product in reaction.products:
					if len(reaction.products) > 1:
						tmpnode_product = meEtree.orderedElement('product')
						tmpnode_molecule = meEtree.orderedSubElement(tmpnode_product, 'molecule', ['ref', 'role'], [tmp_product.label, tmp_product.role])
						tmpnode_comment = etree.Comment(etree.tostring(tmpnode_product, pretty_print=True))
						tmpnode_reaction.append(tmpnode_comment)
					else:
						tmpnode_product = meEtree.orderedSubElement(tmpnode_reaction, 'product')
						tmpnode_molecule = meEtree.orderedSubElement(tmpnode_product, 'molecule', ['ref', 'role'], [tmp_product.label, tmp_product.role])

				if len(reaction.TSs) != 1:
					print 'Error! The number of TS is not 1!', ''.join([str(x)+' ' for x in reaction.TSs]) 
				for tmp_TS in reaction.TSs:
					tmpnode_TS = meEtree.orderedSubElement(tmpnode_reaction, '{%s}transitionState' % self.nsmap['me'])
					tmpnode_molecule = meEtree.orderedSubElement(tmpnode_TS, 'molecule', ['ref', 'role'], [tmp_TS.label, tmp_TS.role])

				meEtree.orderedSubElement(tmpnode_reaction, '{%s}MCRCMethod' % self.nsmap['me'], ['name'], ['SimpleRRKM'])
				if abs(reaction.TSs[0].imfreq) > 1e-2:
					meEtree.orderedSubElement(tmpnode_reaction, '{%s}tunneling' % self.nsmap['me'], ['name'], ['Eckart'])
				else:
					tmpnode_tunneling = meEtree.orderedElement('tunneling', ['name'], ['Eckart'])
					tmpnode_comment = etree.Comment(etree.tostring(tmpnode_tunneling, pretty_print=True).replace('tunneling','me:tunneling'))
					tmpnode_reaction.append(tmpnode_comment)

		if reactSys._thermodynamic == False:
			node_conditions = meEtree.orderedSubElement(root_mesmer, '{%s}conditions' % self.nsmap['me'])

			if len(reactSys.bathGas) != 1:
				print 'Error! The number of bath gas is not 1', ''.join([str(x)+' ' for x in reactSys.bathGas])
			for tmp_bathGas in reactSys.bathGas:
				tmpnode_bathGas = meEtree.orderedSubElement(node_conditions, '{%s}bathGas' % self.nsmap['me'])
				tmpnode_bathGas.text = tmp_bathGas.label

			tmpnode_PTs = meEtree.orderedSubElement(node_conditions, '{%s}PTs' % self.nsmap['me'])
			for tmp_PT in reactSys.PTpairs:
				meEtree.orderedSubElement(tmpnode_PTs, '{%s}PTpair' % self.nsmap['me'], ['units', 'P', 'T'], ['atm', str(tmp_PT[0]), str(tmp_PT[1])])

		node_modelParameters = meEtree.orderedSubElement(root_mesmer, '{%s}modelParameters' % self.nsmap['me'])

		tmpnode_grainSize = meEtree.orderedSubElement(node_modelParameters, '{%s}grainSize' % self.nsmap['me'], ['units'], ['cm-1'])
		tmpnode_grainSize.text = str(self.grainSize)

		tmpnode_eAboveTop = meEtree.orderedSubElement(node_modelParameters, '{%s}energyAboveTheTopHill' % self.nsmap['me'])
		tmpnode_eAboveTop.text = str(self.eAboveTop)

		node_control = meEtree.orderedSubElement(root_mesmer, '{%s}control' % self.nsmap['me'])

		if reactSys._thermodynamic == False:
			meEtree.orderedSubElement(node_control, '{%s}testMicroRates' % self.nsmap['me'])
			meEtree.orderedSubElement(node_control, '{%s}testRateConstants' % self.nsmap['me'])
		else:
			tmpnode_calcMethod = meEtree.orderedSubElement(node_control, '{%s}calcMethod' % self.nsmap['me'], ['units', '{%s}type' % self.nsmap['xsi']], ['kJ/mol','me:thermodynamicTable'])
			tmpnode_Tmin = meEtree.orderedSubElement(tmpnode_calcMethod, '{%s}Tmin' % self.nsmap['me'])
			tmpnode_Tmin.text = '300'
			tmpnode_Tmid = meEtree.orderedSubElement(tmpnode_calcMethod, '{%s}Tmid' % self.nsmap['me'])
			tmpnode_Tmid.text = '1000'
			tmpnode_Tmax = meEtree.orderedSubElement(tmpnode_calcMethod, '{%s}Tmax' % self.nsmap['me'])
			tmpnode_Tmax.text = '2500'
			tmpnode_Tstep = meEtree.orderedSubElement(tmpnode_calcMethod, '{%s}Tstep' % self.nsmap['me'])
			tmpnode_Tstep.text = '100'
			tmpnode_comment = etree.Comment('Note that the unit must be \'kJ/mol\' because of the limitation of code for NASA format fitting')
			tmpnode_calcMethod.append(tmpnode_comment)

		inputFile.write(reaction.TSs[0].label + '.xml', encoding='utf-8', xml_declaration=	True, pretty_print=True)

	def run(self, fileName):
		if self.location == '':
			os.system('mesmer ' + fileName + ' -o out_' + fileName[0:-4] + '.xml -N')
		else:
			os.system(self.location+'/mesmer ' + fileName + ' -o out_' + fileName[0:-4] + '.xml -N')

	def readOutXml(self, fileName):
		canoRate = []
		phenoRate = []

		outFile = etree.ElementTree(file = fileName)
		root_mesmer = outFile.getroot()
		
		tmp_T = []
		tmp_val = []
		tmp_rev = []
		tmp_Keq = []
		for tmpnode_canRateList in root_mesmer.iter('{%s}canonicalRateList' % self.nsmap['me']):
			if self.pattern_xmlCanRate.match(tmpnode_canRateList[0].text):
				for tmpnode_kinf in tmpnode_canRateList.iter('{%s}kinf' % self.nsmap['me']):
					tmp_T.append(float(tmpnode_kinf[0].text))
					tmp_val.append(float(tmpnode_kinf[1].text))
					if len(tmpnode_kinf)>2:
						tmp_rev.append(float(tmpnode_kinf[2].text))
					if len(tmpnode_kinf)>3:
						tmp_Keq.append(float(tmpnode_kinf[3].text))
		if tmp_rev == []:
			canoRate = [np.array(tmp_T), np.array(tmp_val)]
		else:
			canoRate = [np.array(tmp_T), np.array(tmp_val), np.array(tmp_rev), np.array(tmp_Keq)]

		tmp_T = []
		tmp_rate_f = []
		tmp_rate_r = []
		for tmpnode_analysis in root_mesmer.iter('{%s}analysis' % self.nsmap['me']):
			if tmpnode_analysis[0].text == 'All calculations shown':
				for tmpnode_rate in tmpnode_analysis.iter('{%s}rateList' % self.nsmap['me']):
					tmp_T.append(float(tmpnode_rate.attrib['T']))
					# the reverse rate is output firstly? this need to be verified 
					tmp_m = len(tmpnode_rate.getchildren())
					if tmp_m <= 3:
						tmp_rate_f.append(float(tmpnode_rate[tmp_m-1].text))
					elif tmp_m<=5:
						tmp_rate_f.append(float(tmpnode_rate[tmp_m-1].text))
						tmp_rate_r.append(float(tmpnode_rate[tmp_m-2].text))
					else:
						print 'Unexcepted Error! The length of tmpnode_rate is larger than 5!'
		if tmp_rate_r == []:
			phenoRate = [np.array(tmp_T), np.array(tmp_rate_f)]
		else:
			phenoRate = [np.array(tmp_T), np.array(tmp_rate_f), np.array(tmp_rate_r)]

		return canoRate, phenoRate

	def readOutTest(self, fileName, thermodynamic = False):
		if thermodynamic == False:
			TSTRate = []

			tmp_T = []
			tmp_rate_f = []
			tmp_rate_r = []

			fr = file(fileName, 'r')
			tmp_lines = fr.readlines()
			for tmp_line in tmp_lines:
				tmp_m = self.pattern_TSTRate_f.match(tmp_line)
				if tmp_m:
					tmp_T.append(float(tmp_m.group(2)))
					tmp_rate_f.append(float(tmp_m.group(1)))
				tmp_m = self.pattern_TSTRate_r.match(tmp_line)
				if tmp_m:
					if (float(tmp_m.group(2)) - tmp_T[-1]) < 1E-2:
						tmp_rate_r.append(float(tmp_m.group(1)))
					else:
						print 'Error! The forward and reverse TST rate in the Mesmer test file is not in pairs!', fileName
			if tmp_rate_r == []:
				TSTRate = [np.array(tmp_T), np.array(tmp_rate_f)]
			else:
				TSTRate = [np.array(tmp_T), np.array(tmp_rate_f), np.array(tmp_rate_r)]
			return TSTRate
		else:
			tmp_names = []
			tmp_temperatures = []
			tmp_thermos = []
			tmp_NASAs = []

			begin_done = -1
			thermo_done = -1
			NASA_done = -1

			totLineNum = 0

			tmp_temperature = []
			tmp_thermo = []

			fr = file(fileName, 'r')
			tmp_lines = fr.readlines()
			for (index, tmp_line) in enumerate(tmp_lines):
				totLineNum = len(tmp_lines)
				if begin_done != 1:
					tmp_m = self.pattern_thermoBegin.match(tmp_line)
					if tmp_m:
						tmp_names.append(tmp_m.group(1))
						thermo_done = -1
						tmp_temperature = []
						tmp_Q = []
						tmp_H = []
						tmp_S = []
						tmp_Cp = []
						NASA_done = -1
						begin_done = 1
				elif thermo_done != 1:
					tmp_m = self.pattern_testThermo.match(tmp_line)
					if tmp_m:					
						tmp_temperature.append(float(tmp_m.group(1)))
						tmp_Q.append(float(tmp_m.group(2)))
						tmp_H.append(float(tmp_m.group(3)))
						tmp_S.append(float(tmp_m.group(4)))
						tmp_Cp.append(float(tmp_m.group(5)))
					tmp_m = self.pattern_thermoEnd.match(tmp_line)
					if tmp_m:
						if tmp_m.group(1) == tmp_names[-1]:
							tmp_temperatures.append(tmp_temperature)
							tmp_thermos.append([tmp_Q, tmp_H, tmp_S, tmp_Cp])
							thermo_done = 1
						else:
							print 'Error! The thermodynamic data of ' + tmp_names[-1] + ' does not end normally!'
				elif NASA_done != 1:
					if index > totLineNum-2:
						tmp_NASAs.append('')
						begin_done = -1
						NASA_done = 1
					tmp_m = self.pattern_thermoBegin.match(tmp_lines[index+1])
					if tmp_m:
						tmp_NASAs.append('')
						begin_done = -1
						NASA_done = 1
					tmp_m = self.pattern_testNASA1.match(tmp_line.strip())
					if tmp_m:
						tmp2_m = self.pattern_testNASA2.match(tmp_lines[index+1].strip())
						if tmp2_m:
							tmp_NASAs.append(''.join(tmp_lines[index: index+4]).strip())
							begin_done = -1
							NASA_done = 1
			return tmp_names, tmp_temperatures, tmp_thermos, tmp_NASAs

	def calcSysTunnelling(self, reactSys):
		if len(reactSys.reactions) > 1:
			print 'Error! Tunnelling effect calculation of more than 1 reaction is not supported yet!'
		for reaction in reactSys.reactions:
			EZ_reactant = 0.0
			EZ_TS = 0.0
			EZ_product = 0.0
			ZPVE_reactant = 0.0
			ZPVE_TS = 0.0
			ZPVE_product = 0.0
			for tmp_reactant in reaction.reactants:
				EZ_reactant += tmp_reactant.ZPE
				ZPVE_reactant += np.sum(tmp_reactant.frequencies)
			if len(reaction.TSs) != 1:
				print 'Error! The number of TS is not 1!', ''.join([str(x)+' ' for x in reaction.TSs]) 
			for tmp_TS in reaction.TSs:
				EZ_TS += tmp_TS.ZPE
				ZPVE_TS += np.sum(tmp_TS.frequencies)
				v_img = tmp_TS.imfreq
			for tmp_product in reaction.products:
				EZ_product += tmp_product.ZPE
				ZPVE_product += np.sum(tmp_product.frequencies)
			ZPVE_reactant = phys1.cmm1Tokcalmol(ZPVE_reactant)/2.0
			ZPVE_TS = phys1.cmm1Tokcalmol(ZPVE_TS)/2.0
			ZPVE_product = phys1.cmm1Tokcalmol(ZPVE_product)/2.0
			VZ1 = EZ_TS - EZ_reactant
			VZ2 = EZ_TS - EZ_product
			VC1 = VZ1 - (ZPVE_TS - ZPVE_reactant)
			VC2 = VZ2 - (ZPVE_TS - ZPVE_product)
		temperature = sorted(set([tmp_PT[1] for tmp_PT in reactSys.PTpairs]))
		return self.calcTunnelling(VZ1, VZ2, VC1, VC2, v_img, temperature, step=1.0/100.0, E_max=10.0)
		
	# this script is used to calculate Eckart tunnelling factor
	# unit: VZ1 VZ2 VC1 VC2 [kcal/mol]
	# v_img [cm^-1]
	# VZ is the barrier with ZPE correction
	# VC is the classic barrier without ZPE correction
	# the default setting is the same as Mesmer
	# if setting VC the same as VZ, than the method is the same as MultiWell
	def calcTunnelling(self, VZ1, VZ2, VC1, VC2, v_img, temperature, step = 1.0/100.0, E_max = 10.0):
		# all energy unit would be transformed as cm^-1
		VZ1 = phys1.kcalmolTocmm1(VZ1)
		VZ2 = phys1.kcalmolTocmm1(VZ2)
		VC1 = phys1.kcalmolTocmm1(VC1)
		VC2 = phys1.kcalmolTocmm1(VC2)
		k = phys1.JoulTocmm1(phys1.k)
		tunnellingCoeff = []

		A = VC1 - VC2
		B = (np.sqrt(VC1) + np.sqrt(VC2)) ** 2
		cc = (A-B) * (A+B) / 2.0 / v_img / B**1.5
		avg = 4*B*cc**2 - 1
		dd = np.pi * np.sqrt(abs(avg))
		if VZ1 <= VZ2:
		    E_0 = 0
		else:
		    E_0 = VZ1 - VZ2

		for tmp_T in temperature:
			dE = k * tmp_T * step
			E = np.array(range(int(E_max/step + np.ceil(VZ1/dE))))
			E = dE*E + E_0
			tmp_E = E + VC1 - VZ1
			tmp_E[tmp_E < 0]=0.0
			aa = 2 * np.pi * cc * np.sqrt(tmp_E)
			tmp_E = E + VC2 - VZ1
			tmp_E[tmp_E < 0] = 0.0
			bb = 2 * np.pi * cc * np.sqrt(tmp_E)
			if avg > 0:
			    K = 2 * np.sinh(aa) * np.sinh(bb) / (np.cosh(aa+bb) + np.cosh(dd))
			else:
			    K = 2 * np.sinh(aa) * np.sinh(bb) / (np.cosh(aa+bb) + np.cos(dd))
			kT_m1 = 1 / k / tmp_T
			Q = np.sum(K*np.exp(-E*kT_m1)) * step
			tau = np.exp(VZ1*kT_m1) * Q
			tunnellingCoeff.append(tau)

		return tunnellingCoeff


class meEtree:
	@classmethod
	def orderedSubElement(self,parentNode, subNode_tag, keys=[], values=[]):
		if len(keys) == 0:
			return etree.SubElement(parentNode, subNode_tag)
		else:
			return etree.SubElement(parentNode, subNode_tag, attrib=OrderedDict(zip(keys, values)))

	@classmethod
	def orderedElement(self, node_tag, keys=[], values=[]):
		if len(keys) == 0:
			return etree.Element(node_tag)
		else:
			return etree.Element(node_tag, attrib=OrderedDict(zip(keys, values)))



