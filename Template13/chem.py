# this is a class of chemistry 
# it can be used to deal with infomation of atoms and molecules

# if the bond in a ring is not allowed, set this value as true. Otherwise, set it as False
__RingBanned__ = False

import visual

import numpy as np
# constants
elementDict={1:'H',6
:'C',7:'N',8:'O',
'1':'H','6':'C','7':'N','8':'O'
}

eleWeightDict={'H': 1.008, 'C': 12.01, 'O': 16.00, 'N': 14.01}

eleColorDict={'H': visual.color.white, 'C': visual.color.yellow, 'O': visual.color.red, 'N': visual.color.green}

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
bondDisDict={
'H': {'H': [0.6350], 'C': [1.5], 'O': [1.5]},
'C': {'H': [1.5], 'C': [1.24740, 1.3860, 1.4475, 1.6324], 'O': [1.15829, 1.287, 1.34419, 2.16]},
'O': {'H': [1.5], 'C': [1.15829, 1.287, 1.34419, 2.16], 'O': [1.0692, 1.18800, 1.2408, 1.9]}
}

bondOrderDict={
'H': {'H': [1.0], 'C': [1.0], 'O': [1.0]},
'C': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]},
'O': {'H': [1.0], 'C': [3.0, 2.0, 1.5, 1.0], 'O': [3.0, 2.0, 1.5, 1.0]}
}

class molecule:
	atoms = []
	label = ''
	
	def __init__(self, geom='', connect='', atomsNum=0, inputAtoms=[]):
		self.label = ''
		if inputAtoms == []:
			self.atoms = []
			if atomsNum == 0:
				atomsNum = len(geom)
			if len(geom) == atomsNum:
				for i in range(0, atomsNum):
					tmp_line = geom[i]
					tmp_line.strip()
					tmp_line = tmp_line.split()
					tmp_atom = atom(tmp_line[0],i+1,map(float, tmp_line[1:4]))
					self.atoms.append(tmp_atom)
			else:
				print 'Error! Wrong geom input in molecule initiation!'	

			if len(connect) == atomsNum:
				for i in range(0, atomsNum):
					tmp_line = connect[i]
					tmp_line.strip()
					tmp_line = tmp_line.split()
					for j in range(1, len(tmp_line), 2):
						tmp_bond = bond(self.atoms[i], self.atoms[int(tmp_line[j]) - 1], float(tmp_line[j+1]))
						self.atoms[i].addBond(tmp_bond)
						self.atoms[int(tmp_line[j]) - 1].addBond(tmp_bond)
			elif connect != '':
				print 'Error! Worng coonectivity in molecule initiation!'					
		else:
			self.atoms = inputAtoms

	def getLogGeom(self, geom):
		self.atoms = []
		for tmp_line in geom:
			tmp_line.strip()
			tmp_line = tmp_line.split()
			tmp_atom = atom(elementDict[tmp_line[1]] , int(tmp_line[0]), map(float, tmp_line[3:6]))
			self.atoms.append(tmp_atom)

	def changeLabel(self, label):
		self.label = label

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
				if __RingBanned__ == True and tmp_result == 0:
					# print 'Warning! The bond between ' + str(tmp_atom.label) + ' and ' + str(tmp_atom2.label) + ' is in a ring! Now it is not added in the MomInert input file.' 
					pass
				else:
					tmp_rotation = rotation(tmp_atom.bonds[index], tmp_group1, tmp_group2)
					rotations.append(tmp_rotation)
		return rotations

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

	def getAtomsNum(self):
		return len(self.atoms)

	def displayBonds(self):
		print 'all bonds for ' + self.label
		for tmp_atom in self.atoms:
			print tmp_atom.label, tmp_atom.symbol
			for tmp_bond in tmp_atom.bonds:
				print '[', tmp_bond.atom1.label, tmp_bond.atom2.label, ']', tmp_bond.bondOrder

	def clearBonds(self):
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

	def distance(self, atom2):
		tmp = np.array(self.coordinate)-np.array(atom2.coordinate)
		tmp = (sum(tmp**2))**0.5
		return tmp		

class bond:
	atom1 = atom()
	atom2 = atom()
	bondOrder = 0.0

	def __init__(self, inputAtom1=atom(), inputAtom2=atom(), inputBondOrder=0.0):
		self.atom1 = inputAtom1
		self.atom2 = inputAtom2
		self.bondOrder = inputBondOrder


class rotation:
	rotBondAxis = bond()
	atomGroup1 = []
	atomGroup2 = []

	def __init__(self, rotBondAxis=bond(), atomGroup1=[], atomGroup2=[]):
		self.rotBondAxis = rotBondAxis
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




