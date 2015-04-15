# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os

import geometryExtractor
import chem

# if __OOSYSTEM__ == True then OO are all connected if the distance is shorter than 2.0 Ang
__OOSYSTEM__ = True	

class MomInert:
	location = ''

	# constants
	pattern_multi = re.compile('^(-?[0-9]+) (-?[0-9]+).*$')
	pattern_atom = re.compile('^ *[A-Z] *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
	pattern_connnect = re.compile('^ *([0-9]+).*$')
	pattern_inertia = re.compile('^ *  REDUCED MOMENT OF INERTIA ABOUT *([0-9]+)-- *([0-9]+) *BOND: *(-?[0-9]+\.[0-9]+) *amu.*$')
	pattern_rotConst = re.compile('^ *Rotational constant:  B = *(-?[0-9]+\.[0-9]+) *cm-1.*$')

	def __init__(self, location=''):
		self.location = location

	def gjfTodat(self, directory, fileName):
		atomsNum = 0
		lineNum = -1
		atom_start = 0
		connect_start = 0
		geom = ''

		multi_done = 0
		atom_done = 0
		connect_done = 0

		fr = file(directory + '/' + fileName, 'r')
		tmp_lines = fr.readlines()		
		for tmp_line in tmp_lines:
			lineNum += 1
			if multi_done != 1:
				tmp_m = self.pattern_multi.match(tmp_line)
				if tmp_m:
					atom_start = lineNum + 1
					multi_done = 1
			elif atom_done != 1:
				tmp_m = self.pattern_atom.match(tmp_line)
				if tmp_m:
					atomsNum += 1
				else:
					atom_done = 1
			elif connect_done != 1:
				tmp_m = self.pattern_connnect.match(tmp_line)
				if tmp_m:
					tmp_num = int(tmp_m.group(1))
					if (connect_done + tmp_num) == 1:
						connect_done -= 1
						if tmp_num == 1:
							connect_start = lineNum
						if tmp_num == atomsNum:
							connect_done = 1		
					else:
						connect_done = 0

		if connect_start != 0:
			# print 'connectivity info extracted successfully!'
			pass
		else:
			print 'connectivity info extracted not successfully!'
		geom = geometryExtractor.mominertGeometryExtractor(tmp_lines[atom_start: atom_start + atomsNum])

		molecule1 = chem.molecule(geom=tmp_lines[atom_start: atom_start + atomsNum], connect=tmp_lines[connect_start: connect_start + atomsNum], atomsNum=atomsNum)
		if __OOSYSTEM__ == True:
			molecule1.fulfillBonds()
			# molecule1.displayBonds()	
		rotations = molecule1.getRotations()
		fr.close()
		fw = file(directory + '/' + fileName[7:-4] + '.dat', 'w')
		fw.write(fileName[7:-4] + '\n' + 'ANGS\n' + str(atomsNum) + '\n' + geom)
		fw.write(''.join(tmp_rot.singleGroupInfo() for tmp_rot in rotations))
		# for tmp_rot in rotations:
			# fw.write(tmp_rot.group1Info())
		fw.write('0 0\n\n\n\n\n\n\n')
		fw.close()
		return fileName[7:-4] + '.dat'

	def run(self, directory='', fileName=''):
		if directory != '':
			os.chdir(directory)
		os.system('mominert ' + fileName)

	def extractOutput(self, directory, fileName):
		bonds = []
		I0s = []
		B0s = []
		fr = file(directory + '/' + fileName, 'r')
		tmp_lines = fr.readlines()
		for tmp_line in tmp_lines:
			tmp_m = self.pattern_inertia.match(tmp_line)
			if tmp_m:
				bonds.append(map(int, tmp_m.group(1,2)))
				I0s.append(float(tmp_m.group(3)))
			tmp_m = self.pattern_rotConst.match(tmp_line)
			if tmp_m:
				B0s.append(float(tmp_m.group(1)))
		return bonds, I0s, B0s

