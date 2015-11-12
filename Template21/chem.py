# this is a class of chemistry 
# it can be used to deal with infomation of atoms and molecules
import visual
import os

import numpy as np
import copy

# constants
elementDict={1:'H', 2:'He', 6:'C', 7:'N', 8:'O',
'1':'H', '2':'He', '6':'C', '7':'N', '8':'O'
}

eleWeightDict={'H': 1.008, 'He': 4.0026, 'C': 12.011, 'O': 15.999, 'N': 14.007}

eleColorDict={'H': visual.color.white, 'He': visual.color.cyan, 'C': visual.color.yellow, 'O': visual.color.red, 'N': visual.color.green}

# gaussian default bond length threshold parameters
# bondDisDict={
# 'H': {'H': [0.6350], 'C': [1.1342], 'O': [1.01760]},
# 'C': {'H': [1.1342], 'C': [1.24740, 1.3860, 1.4475, 1.6324], 'O': [1.15829, 1.287, 1.34419, 1.5158]},
# 'O': {'H': [1.01760], 'C': [1.15829, 1.287, 1.34419, 1.5158], 'O': [1.0692, 1.18800, 1.2408, 1.39919]}
# }

# self-defined parameters
# version 1.0 used for ROO->QOOH (best)
# bondDisDict={
# 'H': {'H': [0.6350], 'C': [1.5], 'O': [1.5]},
# 'C': {'H': [1.5], 'C': [1.24740, 1.3860, 1.4475, 1.6324], 'O': [1.15829, 1.287, 1.34419, 1.5158]},
# 'O': {'H': [1.5], 'C': [1.15829, 1.287, 1.34419, 1.5158], 'O': [1.0692, 1.18800, 1.2408, 1.5]}
# }

# version 1.1 used for RO2->QOOH and QOOH->cyclic ether + OH (best)
# bondDisDict={
# 'H': {'H': [0.6350], 'C': [1.5], 'O': [1.5]},
# 'C': {'H': [1.5], 'C': [1.24740, 1.3860, 1.4475, 1.6324], 'O': [1.15829, 1.287, 1.34419, 2.16]},
# 'O': {'H': [1.5], 'C': [1.15829, 1.287, 1.34419, 2.16], 'O': [1.0692, 1.18800, 1.2408, 1.9]}
# }

# bondOrderDict={
# 'H': {'H': [1.0], 'C': [1.0], 'O': [1.0]},
# 'C': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]},
# 'O': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]}
# }

# # version 1.2 used for QOOH decomposition (carbonyl + alkene + OH)
# bondDisDict={
# 'H': {'H': [0.6350], 'C': [1.5], 'O': [1.5]},
# 'C': {'H': [1.5], 'C': [1.24740, 1.3860, 1.4475, 2.1], 'O': [1.15829, 1.287, 1.34419, 2.27]},
# 'O': {'H': [1.5], 'C': [1.15829, 1.287, 1.34419, 2.27], 'O': [1.0692, 1.18800, 1.2408, 1.9]}
# }

# bondOrderDict={
# 'H': {'H': [1.0], 'C': [1.0], 'O': [1.0]},
# 'C': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]},
# 'O': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]}
# }

# version 1.3 used for new group additivity
bondDisDict={
'H': {'H': [0.6350], 'C': [1.5], 'O': [1.5]},
'C': {'H': [1.5], 'C': [1.24740, 1.3785, 1.4475, 2.1], 'O': [1.15829, 1.287, 1.34419, 2.27]},
'O': {'H': [1.5], 'C': [1.15829, 1.287, 1.34419, 2.27], 'O': [1.0692, 1.18800, 1.2408, 1.9]}
}

bondOrderDict={
'H': {'H': [1.0], 'C': [1.0], 'O': [1.0]},
'C': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]},
'O': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]}
}

# units:
# P: atm
# T: K
class reactionSystem:
	freqScaleFactor = 1.0
	reactions = []
	bathGas = []
	PTpairs = []

	_hinderedRotation = True
	_thermodynamic = 'rate'

	def __init__(self):
		self.freqScaleFactor = 1.0
		self.reactions = []
		self.bathGas = []
		self.PTpairs = []

	def setFreqScale(self, freqScaleFactor):
		self.freqScaleFactor = freqScaleFactor

	def setPTpairs(self, PTpairs):
		self.PTpairs = PTpairs

	def addReaction(self, reaction):
		self.reactions.append(reaction)

	def addBathGas(self, bathGas):
		self.bathGas.append(bathGas)

	def addPTpair(self, PTpair):
		self.PTpairs.append(PTpair)

	def addPTpairs(self, PTpairs):
		self.PTpairs.extend(PTpairs)

	def hinderedRotationCorrection(self, HR):
		self._hinderedRotation = HR

	def thermodynamic(self, thermo):
		self._thermodynamic = thermo


class reaction:
	reactants = []
	TSs = []
	products = []

	def __init__(self, input_Rs, input_TSs, input_Ps):
		# self.reactants = copy.deepcopy(input_Rs)
		# self.TSs = copy.deepcopy(input_TSs)
		# self.products = copy.deepcopy(input_Ps)
		self.reactants = input_Rs
		self.TSs = input_TSs
		self.products = input_Ps
		if len(self.TSs) != 1:
			print 'Error! The number of TSs is not 1!'

# units:
# ZPE: kcal/mol
# rotConsts: cm-1
# frequency: cm-1
# hessian: Hartree/Bohr2
# MW: amu
# exponentialDown: cm-1
# hinderedRotorQM1D: angle: degree energy: cm-1
class molecule:
	atoms = []
	
	bonds = []
	label = ''
	ZPE = 0.0
	rotConsts = []
	symmetryNumber = 1
	# frequency scaling factor could be set for each molecule separately if the freq computational methods are different but all accurate 
	# currently the freq scaling factor used is the factor in reaction system, which is a uniformed number
	freqScaleFactor = 1.0
	imfreq = 0.0
	frequencies = []
	hessian = []
	spinMultiplicity = 1
	epsilon = 0.0
	sigma = 0.0
	exponentialDown = 0.0
	hinderedRotorQM1D = []
	description = ''
	role = ''
	formula = ''

	formationH = 0.0
	refH0 = {}
	refH298 = {}

	_RingBanned = False

	# the default geom and connectivity are from gjf file
	def __init__(self, geom=[], connect=[], inputAtoms=[]):
		self.bonds = []
		self.label = ''
		self.ZPE = 0.0
		self.rotConsts = []
		self.symmetryNumber = 1
		self.freqScaleFactor = 1.0
		self.imfreq = 0.0
		self.frequencies = []
		self.hessian = []
		self.spinMultiplicity = 1
		self.epsilon = 0.0
		self.sigma = 0.0
		self.exponentialDown = 0.0
		self.hinderedRotorQM1D = []
		self.description = ''
		self.role = ''
		self.formula = ''
		self.formationH = 0.0
		self.refH0 = {}
		self.refH298 = {}

		self._RingBanned = False

		if inputAtoms == []:
			self.atoms = []
			atomsNum = len(geom)
			for i in range(0, atomsNum):
				tmp_line = geom[i]
				tmp_line.strip()
				tmp_line = tmp_line.split()
				tmp_atom = atom(tmp_line[0],i+1,map(float, tmp_line[1:4]))
				self.atoms.append(tmp_atom)

			if len(connect) == atomsNum:
				for i in range(0, atomsNum):
					tmp_line = connect[i]
					tmp_line.strip()
					tmp_line = tmp_line.split()
					for j in range(1, len(tmp_line), 2):
						tmp_bond = bond(self.atoms[i], self.atoms[int(tmp_line[j]) - 1], float(tmp_line[j+1]))
						self.atoms[i].addBond(tmp_bond)
						self.atoms[int(tmp_line[j]) - 1].addBond(tmp_bond)
						self.bonds.append(tmp_bond)
			elif connect != []:
				print 'Error! Worng coonectivity in molecule initiation!'					
		else:
			self.atoms = copy.deepcopy(inputAtoms)

	def getLogGeom(self, geom):
		self.atoms = []
		for tmp_line in geom:
			tmp_line = tmp_line.strip()
			tmp_line = tmp_line.split()
			tmp_atom = atom(elementDict[tmp_line[1]] , int(tmp_line[0]), map(float, tmp_line[3:6]))
			self.atoms.append(tmp_atom)

	def getGjfGeom(self, geom):
		self.atoms = []
		for (i,tmp_line) in enumerate(geom):
			tmp_line = tmp_line.strip()
			tmp_line = tmp_line.split()
			tmp_atom = atom(tmp_line[0],i+1,map(float, tmp_line[1:4]))
			self.atoms.append(tmp_atom)

	def addAtom(self, atom):
		tmp_atom = copy.deepcopy(atom)
		tmp_atom.label = len(self.atoms)+1
		self.atoms.append(tmp_atom)


	# only a fresh virtual bond could be accepted as the parameter of this function 
	def addBond(self, freshBond):
		if not (freshBond.atom1 in self.atoms) and (freshBond.atom2 in self.atoms):
			print 'Error! The atoms to be bonded are not both in the atoms list!', freshBond.atom1.label, freshBond.atom2.label
		else:
			freshBond.atom1.addBond(freshBond)
			freshBond.atom2.addBond(freshBond)
			self.bonds.append(freshBond)

	# input parameters are the two atoms and the bond order
	def addBond2(self, atom1, atom2, bondOrder):
		if not (atom1 in self.atoms) and (atom2 in self.atoms):
			print 'Error! The atoms to be bonded are not both in the atoms list!', atom1.label, atom2.label
		else:
			tmp_bond = bond(atom1, atom2, bondOrder)
			self.addBond(tmp_bond)


	def setLabel(self, label):
		self.label = label

	def setZPE(self, ZPE):
		self.ZPE = ZPE

	def setRotConsts(self, rotConsts):
		self.rotConsts = rotConsts

	def setSymmetryNumber(self, symmetryNumber):
		self.symmetryNumber = symmetryNumber

	def setFreqScaleFactor(self, freqScaleFactor):
		self.freqScaleFactor = freqScaleFactor

	def setImfreq(self, imfreq):
		self.imfreq = imfreq

	def setFrequencies(self, frequencies):
		self.frequencies = frequencies

	def setHessian(self, hessian):
		self.hessian = hessian

	def setSpinMultiplicity(self, spinMultiplicity):
		self.spinMultiplicity = spinMultiplicity

	def setEpsilon(self, epsilon):
		self.epsilon = epsilon

	def setSigma(self, sigma):
		self.sigma = sigma

	def setExponentialDown(self, exponentialDown):
		self.exponentialDown = exponentialDown

	def setHinderedRotorQM1D(self, hinderedRotorQM1D):
		self.hinderedRotorQM1D = hinderedRotorQM1D

	def setDescription(self, description):
		self.description = description

	def setRole(self, role):
		self.role = role

	def serFormula(self, formula):
		self.formula = formula

	def setFormationH(self, formationEnthalpy):
		self.formationH = formationEnthalpy

	def setRefH0(self, refEnthalpy):
		self.refH0 = refEnthalpy
	
	def setRefH298(self, refEnthalpy):
		self.refH298 = refEnthalpy

	def setRingBanned(self, banned):
		self._RingBanned = banned

	def getWeight(self):
		weight = 0.0
		for tmp_atom in self.atoms:
			weight += tmp_atom.mass
		return	weight

	# get the bond between atom1 and atom2
	def getBond(self, atom1Label, atom2Label):
		tmp_children = self.atoms[atom1Label-1].children
		if self.atoms[atom2Label-1] in tmp_children:
			tmp_index = tmp_children.index(self.atoms[atom2Label-1])
			tmp_bond = self.atoms[atom1Label-1].bonds[tmp_index]
		else:
			print 'Error! This bond is not in current molecule', self.label, str(atom1Label), str(atom2Label)
			tmp_bond = None
		return tmp_bond

	# this function is used to get the two parts if a molecule is divided by a certain bond with the tabuAtom, 
	# this is the combination of atom.dividedGraph2 and a double check to guarantee the molecule is correctly divided into two parts. 
	# Only proper for a bond not in a ring. Safer to be used
	# if result==1, then end normally
	# if result==0, the bond is in a cycle
	# if result==-1, there are more than two groups
	def connectedGraph2(self, bond):
		result = 1
		tmp_group1 = bond.atom1.dividedGraph2([bond.atom2])
		# - is equal to .difference() for a set(), but freer parameters are allowed for .difference()
		comple_group1 = list(set(self.atoms) - set(tmp_group1))
		tmp_group2 = bond.atom2.dividedGraph2([bond.atom1])
		tmp_set = set(comple_group1) - set(tmp_group2)
		if len(tmp_set) > 0:
			print 'Error! There are some atoms with labels ' + str([x.label for x in tmp_set]) + ' neither connected with ' + str(bond.atom1.label) + ' nor ' + str(bond.atom2.label) + '!'
			result = -1
		tmp_set = set(tmp_group2) - set(comple_group1)
		if len(tmp_set) > 0:
			# print 'Error! There are some rings in the molecule! Ring members are labeled as ' + str([x.label for x in tmp_set]) + ' , certainly also including ' + str(bond.atom1.label) + ' and ' + str(bond.atom2.label) + '.'
			result = 0
		return tmp_group1, tmp_group2, result

	# get all rotations
	# return a list of rotations 
	def getRotations(self):
		rotations = []
		for tmp_atom in self.atoms:
			if tmp_atom.childrenNum() == 1:
				continue
			for (index, tmp_atom2) in enumerate(tmp_atom.children):
				if tmp_atom2.childrenNum() == 1:
					continue
				# do not rotate if this is a double bond
				if abs(tmp_atom.bonds[index].bondOrder - 1) > 1e-2:
					continue
				if tmp_atom.label > tmp_atom2.label:
					continue
				tmp_group1, tmp_group2, tmp_result = self.connectedGraph2(tmp_atom.bonds[index])
				# print str(tmp_atom.bonds[index].atom1.label) + ' ' + str(tmp_atom.bonds[index].atom2.label)
				# print [x.label for x in tmp_group1]
				# print [x.label for x in tmp_group2]
				if self._RingBanned == True and tmp_result == 0:
					# print 'Warning! The bond between ' + str(tmp_atom.label) + ' and ' + str(tmp_atom2.label) + ' is in a ring! Now it is not added in the MomInert input file.' 
					pass
				else:
					tmp_rotation = rotation(tmp_atom.bonds[index], tmp_group1, tmp_group2)
					rotations.append(tmp_rotation)
		return rotations

	# judge if ring structure exsits in the species
	def existRings(self):
		ringDetectResult = False
		for tmp_atom in self.atoms:
			if tmp_atom.childrenNum() == 1:
				continue
			for (index, tmp_atom2) in enumerate(tmp_atom.children):
				if tmp_atom2.childrenNum() == 1:
					continue
				if tmp_atom.label > tmp_atom2.label:
					continue
				tmp_group1, tmp_group2, tmp_result = self.connectedGraph2(tmp_atom.bonds[index])
				if tmp_result == 0:
					ringDetectResult = True
		return ringDetectResult

	# get the number of members in the ring structure if ring exists 
	# only used for single-ring structure
	def getRingSize(self):
		ringSize = 0

		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)

		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break
		
		# follow the depth ranking to find a ring
		visitedAtom = []
		trace = []
		for tmp_atom in atomList:
			visitedAtom.append(tmp_atom)
			trace.append(tmp_atom)
			tmp_num = 0
			for tmp2_atom in tmp_atom.children:
				if tmp2_atom.symbol != 'H':
					tmp_num += 1
			if tmp_num == 1:
				trace.pop(-1)
				while len(trace) > 0:
					tmp_list = []
					for tmp2_atom in trace[-1].children:
						if tmp2_atom.symbol != 'H':
							tmp_list.append(tmp2_atom)
					if set(tmp_list).issubset(set(visitedAtom)):
						trace.pop(-1)
					else:
						break
			else:
				for (index, tmp2_atom) in enumerate(trace[0:-2]):
					if tmp2_atom in tmp_atom.children:
						ringSize = len(trace) - index
						break
		return ringSize

	def getAtomsNum(self):
		return len(self.atoms)

	def displayBonds(self):
		print 'all bonds for ' + self.label
		for tmp_atom in self.atoms:
			print tmp_atom.label, tmp_atom.symbol
			for tmp_bond in tmp_atom.bonds:
				print '[', tmp_bond.atom1.label, tmp_bond.atom2.label, ']', tmp_bond.bondOrder

	def clearBonds(self):
		self.bonds = []
		for tmp_atom in self.atoms:
			tmp_atom.children = []
			tmp_atom.bonds = []

	# fulfill the bonds using distance infomation rather than connectivity
	def fulfillBonds(self):
		self.clearBonds()
		atomsNum = len(self.atoms)
		for i in range(0, atomsNum):
			for j in range(i+1, atomsNum):
				tmp_order = 0
				tmp_distance = self.atoms[i].distance(self.atoms[j])
				
				distances = bondDisDict[self.atoms[i].symbol][self.atoms[j].symbol]
				orders = bondOrderDict[self.atoms[i].symbol][self.atoms[j].symbol]

				for (index, distance) in enumerate(distances):
					if tmp_distance <= distance:
						tmp_order = orders[index]
					if tmp_order != 0: 
						break
				# if i==6 and j==26:
					# print self.atomsNum.label, self.atomsNum.label, tmp_order
				if tmp_order != 0:
					tmp_bond = bond(self.atoms[i], self.atoms[j], tmp_order)
					self.atoms[i].addBond(tmp_bond)
					self.atoms[j].addBond(tmp_bond)
					self.bonds.append(tmp_bond)


	def generateRotScanFile(self, fixedBond=[], rotCH3=True):
		elementRanking = {'C': 1, 'O':2, 'N':3, 'H':4}

		rotations = self.getRotations()

		if not os.path.exists(self.label):
			os.mkdir(self.label)
		fw = file(os.path.join(self.label, ''.join([self.label, '.rot'])), 'w')	
		fw.write('spinMultiplicity: '+str(self.spinMultiplicity)+'\n')
		fw.write('\ngeometry:\n')
		fw.write(''.join(['%s %.8f %.8f %.8f\n' % (x.symbol, x.coordinate[0], x.coordinate[1], x.coordinate[2]) for x in self.atoms]))
		fw.write('\nrotation information:\n')

		for tmp_rotation in rotations:
			if rotCH3 == False:
				tmp_3rdOrderGroup = tmp_rotation.rotBondAxis.get1stOrderGroup()
				if 'C/H3' in tmp_3rdOrderGroup.values():
					continue
			if tmp_rotation.rotBondAxis.atom1.label < tmp_rotation.rotBondAxis.atom2.label:
				tmp_atom1 = tmp_rotation.rotBondAxis.atom1
				tmp_atom2 = tmp_rotation.rotBondAxis.atom2
			else:
				tmp_atom1 = tmp_rotation.rotBondAxis.atom2
				tmp_atom2 = tmp_rotation.rotBondAxis.atom1

			neighbour1 = None
			neighbour2 = None

			# search the neighbour atom for atom1, ranking in the order of distance, then in the order of element symbol, C, O, N, H
			tmp_children = []
			for tmp_atom in tmp_atom1.children:
				if tmp_atom != tmp_atom2:
					tmp_children.append([tmp_atom.label, tmp_atom.symbol, tmp_atom1.distance(tmp_atom)])
			tmp_children = sorted(tmp_children, key=lambda tmp_list: tmp_list[2])
			tmp_children = sorted(tmp_children, key=lambda tmp_list: elementRanking[tmp_list[1]])
			neighbour1 = tmp_children[0][0]

			tmp_children = []
			for tmp_atom in tmp_atom2.children:
				if tmp_atom != tmp_atom1:
					tmp_children.append([tmp_atom.label, tmp_atom.symbol, tmp_atom2.distance(tmp_atom)])
			tmp_children = sorted(tmp_children, key=lambda tmp_list: tmp_list[2])
			tmp_children = sorted(tmp_children, key=lambda tmp_list: elementRanking[tmp_list[1]])
			neighbour2 = tmp_children[0][0]

			fw.write(''.join([str(neighbour1), ' ', str(tmp_atom1.label), ' ', str(tmp_atom2.label), ' ', str(neighbour2), '\n']))

		if fixedBond != []:
			fw.write('\nfixed bond information:\n')
			fw.write(str(fixedBond[0]) + ' ' + str(fixedBond[1]) + '\n')	

		fw.write('\n\n\n\n\n')
		fw.close()

	# get the formula of the molecule	
	def calcFormula(self):
		elementRanking = {'C':1, 'H':2, 'O':3, 'N':4}
		tmp_formula = ''

		atomList = [x.symbol for x in self.atoms]
		atomSet = set(atomList)
		atomSet = sorted(atomSet, key=elementRanking.__getitem__)
		for tmp_element in atomSet:
			tmp_formula += tmp_element
			tmp_num = atomList.count(tmp_element)
			if tmp_num > 1:
				tmp_formula += str(tmp_num)  

		self.formula = tmp_formula

	# the groups returned is in the order of atoms-ranking in atomList, which is self.atoms as default 
	def get1stOrderGroup(self, inputAtomList=[]):
		atomList = []
		if inputAtomList == []:
			for tmp_atom in self.atoms:
				if tmp_atom.symbol != 'H':
					atomList.append(tmp_atom) 
		else:
			atomList = inputAtomList
		tmp_groups = []
		for tmp_atom in  atomList:
			if tmp_atom.symbol == 'H':
				continue
			tmp_groups.append(tmp_atom.get1stOrderGroup())
		return tmp_groups 

	# return the group additivity vector in method 1
	# i.e. group A - group B 1.0/distance
	# the vector returned is a dict
	def getGroupVector1(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupSet = list(tmp_groupSet)
		N_group = len(tmp_groupSet)
		for i in xrange(N_group):
			for j in xrange(i, N_group):
				tmp_list = sorted([tmp_groupSet[i], tmp_groupSet[j]])
				tmp_text = tmp_list[0] + '-' + tmp_list[1]
				tmp_groupVector[tmp_text] = 0

		distances = self.getDistanceMatrix(atomList)
		# check the distance matrix
		# print [x.label for x in atomList]
		# for tmp in distances:
		# 	print tmp
		for i in xrange(n_nonH):
			for j in xrange(i+1, n_nonH):
				if not np.isnan(distances[i][j]):
					tmp_list = sorted([tmp_groups[i], tmp_groups[j]])
					tmp_text = tmp_list[0] + '-' + tmp_list[1]
					tmp_groupVector[tmp_text] += 1.0/distances[i][j]  		
  
		return tmp_groupVector

	# return the group additivity vector in method 2
	# i.e. group A - group B exp(-distance)
	# the vector returned is a dict
	def getGroupVector2(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupSet = list(tmp_groupSet)
		N_group = len(tmp_groupSet)
		for i in xrange(N_group):
			for j in xrange(i, N_group):
				tmp_list = sorted([tmp_groupSet[i], tmp_groupSet[j]])
				tmp_text = tmp_list[0] + '-' + tmp_list[1]
				tmp_groupVector[tmp_text] = 0

		distances = self.getDistanceMatrix(atomList)
		# check the distance matrix
		# print [x.label for x in atomList]
		# for tmp in distances:
		# 	print tmp
		for i in xrange(n_nonH):
			for j in xrange(i+1, n_nonH):
				if not np.isnan(distances[i][j]):
					tmp_list = sorted([tmp_groups[i], tmp_groups[j]])
					tmp_text = tmp_list[0] + '-' + tmp_list[1]
					tmp_groupVector[tmp_text] += np.exp(-distances[i][j])  		
  
		return tmp_groupVector

	# return the group additivity vector in method 3
	# i.e. group A - all other groups 1.0/distance
	# the vector returned is a dict
	def getGroupVector3(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupSet = list(tmp_groupSet)
		N_group = len(tmp_groupSet)
		for i in xrange(N_group):
			tmp_text = tmp_groupSet[i] + ' - other Groups'
			tmp_groupVector[tmp_text] = 0

		distances = self.getDistanceMatrix(atomList)
		# check the distance matrix
		# print [x.label for x in atomList]
		# for tmp in distances:
		# 	print tmp
		for i in xrange(n_nonH):
			tmp_text = tmp_groups[i] + ' - other Groups'
			for j in xrange(n_nonH):
				if not np.isnan(distances[i][j]):
					if tmp_groups[i] != tmp_groups[j]:
						tmp_groupVector[tmp_text] += 1.0/distances[i][j]
					else:
						tmp_groupVector[tmp_text] += 1.0/distances[i][j]/2.0

		return tmp_groupVector

	# return the group additivity vector in method 4
	# i.e. group A - all other groups exp(-distance)
	# the vector returned is a dict
	def getGroupVector4(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupSet = list(tmp_groupSet)
		N_group = len(tmp_groupSet)
		for i in xrange(N_group):
			tmp_text = tmp_groupSet[i] + ' - other Groups'
			tmp_groupVector[tmp_text] = 0

		distances = self.getDistanceMatrix(atomList)
		# check the distance matrix
		# print [x.label for x in atomList]
		# for tmp in distances:
		# 	print tmp
		for i in xrange(n_nonH):
			tmp_text = tmp_groups[i] + ' - other Groups'
			for j in xrange(n_nonH):
				if not np.isnan(distances[i][j]):
					if tmp_groups[i] != tmp_groups[j]:
						tmp_groupVector[tmp_text] += np.exp(-distances[i][j])
					else:
						tmp_groupVector[tmp_text] += np.exp(-distances[i][j])/2.0

		return tmp_groupVector

	# return the group additivity vector in method 5
	# i.e. group A - group B 1.0/distance for distances of all possible routes
	# the vector returned is a dict
	def getGroupVector5(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupSet = list(tmp_groupSet)
		N_group = len(tmp_groupSet)
		for i in xrange(N_group):
			for j in xrange(i, N_group):
				tmp_list = sorted([tmp_groupSet[i], tmp_groupSet[j]])
				tmp_text = tmp_list[0] + '-' + tmp_list[1]
				tmp_groupVector[tmp_text] = 0

		routes, distances = self.getAllRoutesMatrix(atomList)
		# check the distance matrix
		# print [x.label for x in atomList]
		# print '--------------------------------'
		# print self.label
		# for i in xrange(len(distances)):
		# 	for j in xrange(len(distances)):
		# 		print '(', atomList[i].label, ', ', atomList[j].label, ')', routes[i][j]
		# 		print '(', atomList[i].label, ', ', atomList[j].label, ')', distances[i][j]				
		# print ' '

		for i in xrange(n_nonH):
			for j in xrange(i+1, n_nonH):
				if len(distances[i][j]) > 0:
					tmp_list = sorted([tmp_groups[i], tmp_groups[j]])
					tmp_text = tmp_list[0] + '-' + tmp_list[1]
					# tmp_groupVector[tmp_text] += sum([1.0/x for x in distances[i][j]]) 
					tmp_groupVector[tmp_text] += sum([np.exp(-x) for x in distances[i][j]])   							  		
  
		return tmp_groupVector

	# return the conventioanl group additivity vector
	# i.e. groups, GAUCHE, 1-5 interaction
	# the vector returned is a dict
	def getConventionalGAVector(self):
		tmp_groupVector = {}
		n = len(self.atoms)
		# get all non-H atom list
		allAtoms = []
		for tmp_atom in self.atoms:
			if tmp_atom.symbol != 'H':
				allAtoms.append(tmp_atom)
		# get the atomList in depth first search ranking
		atomList = []
		atomList.append(allAtoms[0])
		allAtoms.remove(allAtoms[0])
		parentIndex = 0
		while allAtoms != []:
			for tmp_atom in atomList[parentIndex].children:
				if tmp_atom.symbol != 'H' and tmp_atom in allAtoms :
					atomList.insert(parentIndex+1, tmp_atom)
					allAtoms.remove(tmp_atom)
			parentIndex += 1
			if parentIndex == len(atomList):
				break

		# group info one by one
		tmp_groups = self.get1stOrderGroup(atomList)
		n_nonH = len(tmp_groups)		
		tmp_groupSet = set(tmp_groups)
		for tmp_group in tmp_groupSet:
			tmp_groupVector[tmp_group] = tmp_groups.count(tmp_group)
		
		# interaction between two groups
		tmp_groupVector['GAUCHE'] = 0
		tmp_groupVector['1-5_interaction'] = 0
		GAUCHETable = [
		[0, 0, 0, 0],
		[0, 0, 1, 2],
		[0, 1, 2, 4],
		[0, 2, 4, 6]
		]
		oneFiveIntTable=[
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 1],
		[0, 0, 1, 2]
		]
		for (index, tmp_atom) in enumerate(atomList):
			for tmp_child in tmp_atom.children:
				if tmp_child.symbol == 'H':
					continue
				if tmp_child not in atomList[index+1:]:
					pass
				else:
					tmp_groupVector['GAUCHE'] += GAUCHETable[tmp_atom.nonHChildrenNum()-1][tmp_child.nonHChildrenNum()-1]
				for tmp_grandson in tmp_child.children:
					if tmp_grandson.symbol == 'H':
						continue
					if tmp_grandson not in atomList[index+1:]:
						pass
					else:
						tmp_groupVector['1-5_interaction'] += oneFiveIntTable[tmp_atom.nonHChildrenNum()-1][tmp_grandson.nonHChildrenNum()-1]
		return tmp_groupVector


	# get the distance matrix describling the distance between different groups
	# this is not the same as a TSP (travel saleman problem) solver
	def getDistanceMatrix(self, atomList):
		n = len(atomList)
		if n > 1:
			tmp_distances = self.getDistanceMatrix(atomList[0:-1])
			adjacentAtoms = []
			for (index, tmp_atom) in enumerate(atomList[0: -1]):
				if tmp_atom in atomList[-1].children:
					tmp_distances[index].append(1.0)
					adjacentAtoms.append(tmp_atom)
				else:
					tmp_distances[index].append(np.nan)
			for (index, tmp_atom) in enumerate(atomList[0: -1]):
				if tmp_atom not in adjacentAtoms:
					tmp_disList = []
					for tmp_adjAtom in adjacentAtoms:
						tmp_distance = tmp_distances[index][atomList.index(tmp_adjAtom)]
						if not np.isnan(tmp_distance):
							tmp_disList.append(tmp_distance+1.0)
					if len(tmp_disList) > 0:
						tmp_distances[index][-1] = min(tmp_disList)
			for i in xrange(n-1):
				for j in xrange(i+1, n-1):
					tmp_distance = tmp_distances[i][-1] + tmp_distances[j][-1]
					if not np.isnan(tmp_distance):
						if tmp_distance < tmp_distances[i][j]:
							tmp_distances[i][j] = tmp_distance
							tmp_distances[j][i] = tmp_distance
			tmp_distances.append([])
			for i in xrange(n-1):
				tmp_distances[-1].append(tmp_distances[i][-1])
			tmp_distances[-1].append(np.nan)
		else:
			tmp_distances = [[np.nan]]
		return tmp_distances

	# get the distance matrix describling all the possible route and distance between different groups
	def getAllRoutesMatrix(self, atomList):
		n = len(atomList)
		if n > 1:
			tmp_routes, tmp_distances = self.getAllRoutesMatrix(atomList[0:-1])
			adjacentAtoms = []
			tmp_routes.append([])
			tmp_distances.append([])
			for (index, tmp_atom) in enumerate(atomList[0: -1]):
				if tmp_atom in atomList[-1].children:
					tmp_routes[-1].append([[tmp_atom.label]])
					tmp_distances[-1].append([1.0])
					adjacentAtoms.append(tmp_atom)
				else:
					tmp_routes[-1].append([])
					tmp_distances[-1].append([])
			for (index, tmp_atom) in enumerate(atomList[0: -1]): 
					tmp_routeList = []
					tmp_disList = []
					for tmp_adjAtom in adjacentAtoms:
						tmp_route = tmp_routes[atomList.index(tmp_adjAtom)][index]
						tmp_distance = tmp_distances[atomList.index(tmp_adjAtom)][index]
						if len(tmp_distance) > 0:
							tmp_routeList += [[tmp_adjAtom.label]+x for x  in tmp_route]
							tmp_disList += [x+1.0 for x in tmp_distance]
					if len(tmp_disList) > 0:
						tmp_routes[-1][index] += tmp_routeList
						tmp_distances[-1][index] += tmp_disList
			for i in xrange(n-1):
				tmp_routes[i].append([x[-2::-1]+[atomList[-1].label] for x in tmp_routes[-1][i]])
				tmp_distances[i].append(copy.deepcopy(tmp_distances[-1][i]))
			tmp_routes[-1].append([])
			tmp_distances[-1].append([])

			for i in xrange(n-1):
				for j in xrange(i+1, n-1):
					tmp_route = []
					tmp_distance = []
					for x in xrange(len(tmp_distances[-1][i])):
						for y in xrange(len(tmp_distances[-1][j])):
							tmp_list = tmp_routes[i][-1][x] + tmp_routes[-1][j][y]
							tmp_set = set([atomList[i].label] + tmp_list)
							if len(tmp_set) == (len(tmp_list)+1):
								tmp_routes[i][j] += [tmp_list]
								tmp_distances[i][j] += [tmp_distances[i][-1][x] + tmp_distances[-1][j][y]]
								# tmp_routes[j][i] += [tmp_list[-2::-1]+[atomList[i].label]]
								tmp_routes[j][i] += [tmp_routes[j][-1][y] + tmp_routes[-1][i][x]]
								tmp_distances[j][i] += [tmp_distances[j][-1][y] + tmp_distances[-1][i][x]]
		else:
			tmp_routes = [[[]]]
			tmp_distances = [[[]]]
		
		return tmp_routes, tmp_distances

   
class atom:
	symbol = ''
	label = 0
	mass = 0.0
	coordinate =[]
	children = []
	bonds = []
	color = (1,1,1)

	def __init__(self, inputSymbol='', inputLabel=0, inputCoordinate=[], inputBonds=[]):
		self.symbol = inputSymbol
		self.label = inputLabel
		if inputSymbol in eleWeightDict:
			self.mass = eleWeightDict[inputSymbol]
			self.color = eleColorDict[inputSymbol]
		else: 
			self.mass = 0.0
			self.color = (0,0,0)
		if inputCoordinate == []:
			self.coordinate = []
		else:
			self.coordinate = inputCoordinate
		self.children = []
		self.bonds = []
		for tmp_bond in inputBonds:
			self.addBond(tmp_bond)

	def addBond(self,bond): 
		# print 'atoms:\t' + str(bond.atom1.label) + '\t' + str(bond.atom2.label)
		if bond.atom1.label == self.label and bond.atom2.label != self.label:
			if bond.atom2 not in self.children:
				self.children.append(bond.atom2)
				self.bonds.append(bond)
			else:
				print 'this bond has been added!\t' + str(self.label) + ' ' + str(bond.atom2.label)
				pass
		elif bond.atom1.label != self.label and bond.atom2.label == self.label:
			if bond.atom1 not in self.children:
				self.children.append(bond.atom1)
				self.bonds.append(bond)
			else:
				print 'this bond has been added!\t' + str(self.label) + ' ' + str(bond.atom1.label)
				pass
		else:
			print 'Error! There is a wrong bond between ' + str(bond.atom1.label) + ' and ' + str(bond.atom2.label) + ' on atom ' + str(self.label) + '.'

	# this function is used to get the left connected part after prohibiting the route to tabuAtomPool, but without double check. 
	# It's unknown whether the left part is a part or not. It is also a arbitary division if there is a ring structure in the molecule.
	def dividedGraph2(self,tabuPool):
		connectedPool = [self]
		tabuPool.append(self)
		for tmp_atom in self.children:
			if tmp_atom not in tabuPool:
				connectedPool += tmp_atom.dividedGraph2(tabuPool)
				tabuPool += connectedPool
		return connectedPool

	def childrenNum(self):
		return len(self.children)

	def nonHChildrenNum(self):
		number = 0
		for tmp_child in self.children:
			if tmp_child.symbol != 'H':
				number += 1
		return number

	def distance(self, atom2):
		tmp = np.array(self.coordinate)-np.array(atom2.coordinate)
		tmp = (sum(tmp**2))**0.5
		return tmp

	def get1stOrderGroup(self):
		elementRanking = {'C':10, 'C1.5':11, 'C2.0':12, 'H':20, 'O':30, 'N':40}

		tmp_childrenSymbol = []
		for (index, tmp_atom) in enumerate(self.children):
			if (self.bonds[index].bondOrder - 1.0) < 1E-2:
				tmp_childrenSymbol.append(tmp_atom.symbol)
			else:
				tmp_childrenSymbol.append(tmp_atom.symbol + '%.1f' % self.bonds[index].bondOrder)	
		tmp_set = set(tmp_childrenSymbol)
		if not tmp_set.issubset(set(elementRanking.keys())):
			print 'Error! There is some new groups not in the ranking weight set', tmp_set-set(elementRanking.keys())
		tmp_set = sorted(tmp_set, key=elementRanking.__getitem__)
		groupStr = self.symbol
		for tmp_element in tmp_set:
			groupStr += '/' + tmp_element
			tmp_num = tmp_childrenSymbol.count(tmp_element)
			if tmp_num > 1:
				groupStr += str(tmp_num)		
		return groupStr
						

class bond:
	atom1 = atom()
	atom2 = atom()
	bondOrder = 0.0

	# this bond initialized is not a real bond
	# it would not be a real one until verified in a molecule level or added logically
	# we can call it a fresh virtual bond now
	def __init__(self, inputAtom1, inputAtom2, inputBondOrder=0.0):
		self.atom1 = inputAtom1
		self.atom2 = inputAtom2
		self.bondOrder = inputBondOrder

	def get1stOrderGroup(self):
		elementRanking = {'C':1, 'H':2, 'O':3, 'N':4}

		tmp_childrenSymbol = [x.symbol for x in self.atom1.children]
		tmp_childrenSymbol.remove(self.atom2.symbol)
		tmp_set = set(tmp_childrenSymbol)
		tmp_set = sorted(tmp_set, key=elementRanking.__getitem__)
		group1Str = self.atom1.symbol
		for tmp_element in tmp_set:
			group1Str += '/' + tmp_element
			tmp_num = tmp_childrenSymbol.count(tmp_element)
			if tmp_num > 1:
				group1Str += str(tmp_num)

		tmp_childrenSymbol = [x.symbol for x in self.atom2.children]
		tmp_childrenSymbol.remove(self.atom1.symbol)
		tmp_set = set(tmp_childrenSymbol)
		tmp_set = sorted(tmp_set, key=elementRanking.__getitem__)
		group2Str = self.atom2.symbol
		for tmp_element in tmp_set:
			group2Str += '/' + tmp_element
			tmp_num = tmp_childrenSymbol.count(tmp_element)
			if tmp_num > 1:
				group2Str += str(tmp_num)
		
		return {self.atom1.label : group1Str, self.atom2.label : group2Str}

	def get2ndOrderGroup(self):
		tmp_bonds = self.atom1.bonds
		tmp_groupStrs = []
		for tmp_bond in tmp_bonds:
			if tmp_bond == self:
				continue
			else:
				if tmp_bond.atom1.label == self.atom1.label:
					tmp_label = tmp_bond.atom2.label
				else:
					tmp_label = tmp_bond.atom1.label
				tmp_groupStr = tmp_bond.get1stOrderGroup()
				tmp_groupStrs.append(tmp_groupStr[tmp_label])
		tmp_set = set(tmp_groupStrs)
		tmp_set = sorted(tmp_set)
		group1Str = self.atom1.symbol
		for (index, tmp_Str) in enumerate(tmp_set):
			tmp_num = tmp_groupStrs.count(tmp_Str)
			if len(tmp_Str) > 1:
				group1Str += '/(' + tmp_Str + ')'
			else:
				group1Str += '/' + tmp_Str
			if tmp_num > 1:
				group1Str += str(tmp_num)

		tmp_bonds = self.atom2.bonds
		tmp_groupStrs = []
		for tmp_bond in tmp_bonds:
			if tmp_bond == self:
				continue
			else:
				if tmp_bond.atom1.label == self.atom2.label:
					tmp_label = tmp_bond.atom2.label
				else:
					tmp_label = tmp_bond.atom1.label
				tmp_groupStr = tmp_bond.get1stOrderGroup()
				tmp_groupStrs.append(tmp_groupStr[tmp_label])
		tmp_set = set(tmp_groupStrs)
		tmp_set = sorted(tmp_set)
		group2Str = self.atom2.symbol
		for (index, tmp_Str) in enumerate(tmp_set):
			tmp_num = tmp_groupStrs.count(tmp_Str)
			if len(tmp_Str) > 1:
				group2Str += '/(' + tmp_Str + ')'
			else:
				group2Str += '/' + tmp_Str
			if tmp_num > 1:
				group2Str += str(tmp_num)
		
		return {self.atom1.label: group1Str, self.atom2.label: group2Str}

	def get3rdOrderGroup(self):
		tmp_bonds = self.atom1.bonds
		tmp_groupStrs = []
		for tmp_bond in tmp_bonds:
			if tmp_bond == self:
				continue
			else:
				if tmp_bond.atom1.label == self.atom1.label:
					tmp_label = tmp_bond.atom2.label
				else:
					tmp_label = tmp_bond.atom1.label
				tmp_groupStr = tmp_bond.get2ndOrderGroup()
				tmp_groupStrs.append(tmp_groupStr[tmp_label])
		tmp_set = set(tmp_groupStrs)
		tmp_set = sorted(tmp_set)
		group1Str = self.atom1.symbol
		for (index, tmp_Str) in enumerate(tmp_set):
			tmp_num = tmp_groupStrs.count(tmp_Str)
			if len(tmp_Str) > 1:
				group1Str += '/(' + tmp_Str + ')'
			else:
				group1Str += '/' + tmp_Str
			if tmp_num > 1:
				group1Str += str(tmp_num)

		tmp_bonds = self.atom2.bonds
		tmp_groupStrs = []
		for tmp_bond in tmp_bonds:
			if tmp_bond == self:
				continue
			else:
				if tmp_bond.atom1.label == self.atom2.label:
					tmp_label = tmp_bond.atom2.label
				else:
					tmp_label = tmp_bond.atom1.label
				tmp_groupStr = tmp_bond.get2ndOrderGroup()
				tmp_groupStrs.append(tmp_groupStr[tmp_label])
		tmp_set = set(tmp_groupStrs)
		tmp_set = sorted(tmp_set)
		group2Str = self.atom2.symbol
		for (index, tmp_Str) in enumerate(tmp_set):
			tmp_num = tmp_groupStrs.count(tmp_Str)
			if len(tmp_Str) > 1:
				group2Str += '/(' + tmp_Str + ')'
			else:
				group2Str += '/' + tmp_Str
			if tmp_num > 1:
				group2Str += str(tmp_num)
		
		return {self.atom1.label: group1Str, self.atom2.label: group2Str}


class rotation:
	rotBondAxis = None
	atomGroup1 = []
	atomGroup2 = []
	angles = []
	energies = []
	period = 1

	# rotBondAxis is a bond instance
	def __init__(self, rotBondAxis, atomGroup1=[], atomGroup2=[]):
		self.rotBondAxis = rotBondAxis
		self.angles = []
		self.energies = []
		self.period = 1
		if atomGroup1 == []:
			self.atomGroup1	= []
		else:
			self.atomGroup1 = atomGroup1
		if atomGroup2 == []:
			self.atomGroup2 = []
		else:
			self.atomGroup2 = atomGroup2
	
	def group1Add(self,atom):
		self.atomGroup1.append(atom)	

	def group2Add(self,atom):
		self.atomGroup2.append(atom)

	def group1Labels(self):
		tmp_list = [x.label for x in self.atomGroup1]
		tmp_list.sort()
		return tmp_list

	def group2Labels(self):
		tmp_list = [x.label for x in self.atomGroup2]
		tmp_list.sort()
		return tmp_list

	def group1Num(self):
		return len(self.atomGroup1)

	def group2Num(self):
		return len(self.atomGroup2)

	def group1Info(self):
		info=str(self.rotBondAxis.atom1.label) + ' ' + str(self.rotBondAxis.atom2.label) + '\n'
		info += str(self.group1Num()) + '\n'
		info += ''.join(str(x) + ' ' for x in self.group1Labels()) + '\n'
		return info

	def group2Info(self):
		info=str(self.rotBondAxis.atom2.label) + ' ' + str(self.rotBondAxis.atom1.label) + '\n'
		info += str(self.group2Num()) + '\n'
		info += ''.join(str(x) + ' ' for x in self.group2Labels()) + '\n'
		return info

	def singleGroupInfo(self):
		if self.group1Num() <= self.group2Num():
			return self.group1Info()
		else:
			return self.group2Info()

	def setPotential(self, angles, energies):
		self.angles = angles
		self.energies = energies

	def setPeriod(self, periodicity):
		self.period = periodicity	

	# This function is used to detect the periodicity automatically 
	# it should be paid attention to that manually adjustment is needed for highly symmetric structure
	def detectPeriod(self):
		periodTable = {'C/H3': 3,
		'C/H2': 2,
		'C/(C/H3)2':2
		}
		# use 3rd order group to avoid recognition error form molecule and radical
		# if C atom exists in 2nd order, it would be important whether there are only H atoms connecting
		tmp_3rdOrderGroup = self.rotBondAxis.get3rdOrderGroup()
		for tmp_group in periodTable.keys():
			if tmp_group in tmp_3rdOrderGroup.values():
				# print tmp_group, tmp_3rdOrderGroup
				self.period = periodTable[tmp_group]
				break



