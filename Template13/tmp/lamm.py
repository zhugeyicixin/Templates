# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import visual

import chem
import mathematics

class lamm:
	location = ''

	# constants
	pattern_outStart = re.compile('^ *INDEX *ANG\(DEG\) *ANG\(RAD\) *E\(cm-1\) *I\(amu.*2\) *B\(cm-1\)$')
	pattern_out = re.compile('^ *([0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
	pattern_point = re.compile('^ *([0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')	

	def __init__(self, location=''):
		self.location = location

	def genInput(self, geoms, dihedral = [], energy_cmm1=[]):
		fw = file('lamm.dat', 'w')
		fw.write(geoms[0].label + '\n')
		fw.write(
'''Calculated at [      ] level of theory      

''' + str(geoms[0].getAtomsNum()) + '''               !Number of atoms in the molecule

0, ''' + str(len(geoms)) + ''', 10       ! Minumum angle, No. of Points and Stepsize (in degrees)

''')
		for tmp_atom in geoms[0].atoms:
			fw.write(str(tmp_atom.mass) + '\n')
		fw.write('\n')
		for tmp_mole in geoms:
			for tmp_atom in tmp_mole.atoms:
				fw.write(''.join(str(x) + ' ' for x in tmp_atom.coordinate) + '\n')
			fw.write('\n')
		fw.write(
''''WARNING: The zero of the relative energy is arbitrary minimum'

''')
		if abs(dihedral[1] - dihedral[0] - 10) > 1e-2:
			print 'Error! The step is not 10 degree!'
		if len(dihedral) < 37:
			print 'Error! The scan points is less than 37!'
		for i in range(0, len(dihedral)):
			fw.write(str(10*i) + '\t' + str(energy_cmm1[i]) + '\n')
		fw.write('\n\n\n\n\n\n')
		fw.close()

		# visual.display(title=geoms[0].label, width=500, height=500)
		# i = 0
		# visual.dt = 0.5
		# ball = []
		# ball_label = []
		# for tmp_atom in geoms[i].atoms:
		# 	ball.append(visual.sphere(pos=tmp_atom.coordinate, radius=0.5, color=tmp_atom.color))
		# 	ball_label.append(visual.label(pos=ball[-1].pos, text=str(tmp_atom.label), xoffset=0, yoffset=0,height=20,font='sans'))
		# # ball = visual.sphere(pos=geoms[i].atoms[0].coordinate, radius=0.5, color=visual.color.red)
		# ball[2].trail = visual.curve(color=ball[2].color)

		# while True:
		# 	visual.rate(1/visual.dt)
		# 	i += 1	
		# 	if not i < len(geoms):
		# 		# continue
		# 		i = 0 
		# 	print i
		# 	for (index, tmp_atom) in enumerate(geoms[i].atoms):
		# 		ball[index].pos = tmp_atom.coordinate
		# 		ball_label[index].pos = ball[index].pos
		# 	ball[2].trail.append(pos=ball[2].pos, color=(1,0,0))

	def run(self, directory='', fileName=''):
		if directory != '':
			os.chdir(directory)
		os.system('lamm ' + fileName)

	def extractOutput(self, directory='', fileName=''):
		outStart_done = 0
		dihedral = []
		inertias = []
		rotConsts = []
		step = 10/180*np.pi
		part_inertias = {}
		part_rotConsts = {}
		interpolationNum = {}

		missNum = 0
		points = 0

		if fileName == '':
			fileName = 'lamm.out'
		if directory != '':
			fr = file(directory + '/' + fileName, 'r')
		else:
			fr = file(fileName, 'r')
		tmp_lines = fr.readlines()
		for tmp_line in tmp_lines:
			if outStart_done != 1:
				tmp_m = self.pattern_outStart.match(tmp_line)
				if tmp_m:
					outStart_done = 1
			else:
				tmp_m = self.pattern_point.match(tmp_line)
				if tmp_m:
					points += 1
				tmp_m = self.pattern_out.match(tmp_line)
				if tmp_m:
					if missNum > 0:
						interpolationNum[len(inertias)] = missNum
						missNum = 0
					part_inertias[int(tmp_m.group(1))] = float(tmp_m.group(5))
					part_rotConsts[int(tmp_m.group(1))] = float(tmp_m.group(6))
					dihedral.append(float(tmp_m.group(3)))
					inertias.append(float(tmp_m.group(5)))
					rotConsts.append(float(tmp_m.group(6)))
				else:
					missNum += 1
		
		# inertias = mathematics.interpolation(inertias, interpolationNum)
		# rotConsts = mathematics.interpolation(rotConsts, interpolationNum)

		# inertias = mathematics.interpolation2(part_inertias, points)
		# rotConsts = mathematics.interpolation2(part_rotConsts, points)
		# dihedral = np.array(range(0,10*points,10))/180.0*np.pi

		# plt.figure()
		# plt.plot(dihedral, inertias,'*')
		# plt.show()

		return dihedral, inertias, rotConsts

	# directory is where the original file 'lamm.dat/.out' exsits and reFileName is the name after renaming of the renamed file 
	def rename(self, directory='', reFileName=''):
		if directory == '':
			print reFileName
			os.rename('lamm.dat', reFileName + '.dat')
			os.rename('lamm.out', reFileName + '.out')
		else:
			os.rename(directory + '/' + 'lamm.dat', directory + '/' + reFileName + '.dat')
			os.rename(directory + '/' + 'lamm.out', directory + '/' + reFileName + '.out')



