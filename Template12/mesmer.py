# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import numpy as np
from lxml import etree
import visual
from collections import OrderedDict

import chem

# units: 
# grainSize: cm-1
# energyAboveTheTopHill: kT
class mesmer:
	location = ''
	nsmap = {None: 'http://www.xml-cml.org/schema','me': 'http://www.chem.leeds.ac.uk/mesmer', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
	grainSize = 100
	eAboveTop = 100.0

	pattern_TSTRate_f = re.compile('^.*Canonical.*first order forward rate constant.*= *([\-\.\+eE0-9]+).*\(([\-\.\+eE0-9]+) *K\).*$')
	pattern_TSTRate_r = re.compile('^.*Canonical.*first order backward rate constant.*= *([\-\.\+eE0-9]+).*\(([\-\.\+eE0-9]+) *K\).*$')

	def __init__(self, location=''):
		self.location = location
		self.nsmap = OrderedDict(zip([None, 'me', 'xsi'], ['http://www.xml-cml.org/schema', 'http://www.chem.leeds.ac.uk/mesmer', 'http://www.w3.org/2001/XMLSchema-instance']))
		self.grainSize = 50
		self.eAboveTop = 200.0

	def setGrainSize(self, grainSize):
		self.grainSize = grainSize

	def setEAboveTop(self, eAboveTop):
		self.eAboveTop = eAboveTop

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

				tmpnode_mole = meEtree.orderedSubElement(node_moleculeList, 'molecule', ['id','description'],[tmp_molecule.label, tmp_molecule.description])
				
				tmpnode_atom = meEtree.orderedSubElement(tmpnode_mole, 'atomArray')
				for tmp_atom in tmp_molecule.atoms:
					meEtree.orderedSubElement(tmpnode_atom, 'atom', ['id', 'elementType', 'x3', 'y3', 'z3'], [tmp_atom.symbol+str(tmp_atom.label), tmp_atom.symbol, str(tmp_atom.coordinate[0]), str(tmp_atom.coordinate[1]), str(tmp_atom.coordinate[2])])
				
				tmpnode_bond = meEtree.orderedSubElement(tmpnode_mole, 'bondArray')
				for (index, tmp_bond) in enumerate(tmp_molecule.bonds):
					meEtree.orderedSubElement(tmpnode_bond, 'bond', ['id', 'atomRefs2', 'order'], ['b'+str(index+1), ''.join([tmp_bond.atom1.symbol, str(tmp_bond.atom1.label), ' ', tmp_bond.atom2.symbol, str(tmp_bond.atom2.label)]), str(tmp_bond.bondOrder)])
				
				tmpnode_propertyList = meEtree.orderedSubElement(tmpnode_mole, 'propertyList')
				
				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['dictRef'], ['me:ZPE'])
				tmpnode_scalar = meEtree.orderedSubElement(tmpnode_property, 'scalar', ['units'], ['kcal/mol'])
				tmpnode_scalar.text = str(tmp_molecule.ZPE)


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

				tmpnode_property = meEtree.orderedElement('property', ['dictRef'], ['me:vibFreqs'])
				tmpnode_array = meEtree.orderedSubElement(tmpnode_property, 'array', ['units'], ['cm-1'])
				tmpnode_array.text = ''.join([str(x) + ' ' for x in tmp_molecule.frequencies])
				tmpnode_comment = etree.Comment(etree.tostring(tmpnode_property, pretty_print=True))
				tmpnode_propertyList.append(tmpnode_comment)

				tmpnode_property = meEtree.orderedSubElement(tmpnode_propertyList, 'property', ['title', 'dictRef'], ['Hessian', 'me:hessian'])
				tmpnode_matrix = meEtree.orderedSubElement(tmpnode_property, 'matrix', ['rows', 'matrixType', 'units'], [str(tmp_molecule.getAtomsNum()*3), 'squareSymmetricLT', 'Hartree/Bohr2'])
				tmpnode_matrix.text = ''.join([str(x) + ' ' for x in tmp_molecule.hessian])

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
						for (index, tmp_angle) in enumerate(tmp_hinderRotor.angles):
							tmpnode_point = meEtree.orderedSubElement(tmpnode_potential, '{%s}PotentialPoint' % self.nsmap['me'], ['angle', 'potential'], [str(tmp_angle), str(tmp_hinderRotor.energies[index])])


			if len(reaction.products) > 1:
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
			meEtree.orderedSubElement(tmpnode_reaction, '{%s}tunneling' % self.nsmap['me'], ['name'], ['Eckart'])

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

		meEtree.orderedSubElement(node_control, '{%s}testMicroRates' % self.nsmap['me'])
		meEtree.orderedSubElement(node_control, '{%s}testRateConstants' % self.nsmap['me'])

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
		for tmpnode_microRateList in root_mesmer.iter('{%s}microRateList' % self.nsmap['me']):
			if tmpnode_microRateList[0].text == 'Microcanonical rate coefficients':
				for tmpnode_microRate in tmpnode_microRateList.iter('{%s}microRate' % self.nsmap['me']):
					tmp_T.append(float(tmpnode_microRate[0].text))
					tmp_val.append(float(tmpnode_microRate[1].text))
		canoRate = [np.array(tmp_T), np.array(tmp_val)]

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

	def readOutTest(self, fileName):
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



