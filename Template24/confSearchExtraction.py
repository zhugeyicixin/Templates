# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
from xlwt import *
import pyExcelerator
from xlutils.copy import copy

import re
import os
import shutil
import cluster
import chem
import Frog

#input
# cluster could be set as cce or Tsinghua100
# the path where the jobs would lie should be announced
clusterName = 'cce'
clusterPath = '/home/hetanjin/newGroupAdditivityFrog/CnH2n_3'

# symbol indicating the position
pattern_name = re.compile('^(C[0-9]*H[0-9]*_[0-9]*)_minimized\.mol2$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)
Frog1 = Frog.Frog()

# definetion of comparing pattern

#variables
moles = []
gjfFiles = []

#flags

# temporary variables
tmp_name = ''

pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)
if os.path.exists('ConformerGJFs'):
	shutil.rmtree('ConformerGJFs')
os.mkdir('ConformerGJFs')
for tmp_file in tmp_fileList:
	tmp_m = pattern_name.match(tmp_file)
	if tmp_m:
		tmp_name = tmp_m.group(1)
		print tmp_name
		moles = Frog1.readConformers(tmp_file)
		if len(moles) < 5:
			tmp_num = len(moles)
		else:
			tmp_num = 5
			for i in xrange(5, len(moles)):
				if (moles[i].ZPE - moles[0].ZPE) > 6:
					tmp_num = i
					break
		for i in xrange(tmp_num):
			if i > 99:
				print 'Error! The number of comformers is more than 99!'
			fw = file(os.path.join(pwd, 'ConformerGJFs', tmp_name + '_' + '%02d' % i + '.gjf'), 'w')
			fw.write(
'''#p b3lyp/6-31g(d) opt freq

this is the .gjf file generated from Forg output which is used to save the coordinate of different coformers

0 1
''')
			for tmp_atom in moles[i].atoms:
				fw.write(tmp_atom.symbol + '    ' + str(tmp_atom.coordinate[0]) + '    ' + str(tmp_atom.coordinate[1]) + '    ' + str(tmp_atom.coordinate[2]) + '\n')
			fw.write('\n\n\n\n\n\n')
			fw.close()

os.chdir('ConformerGJFs')
pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)
for tmp_file in tmp_fileList:
	if re.search('\.gjf', tmp_file):
		if re.search('[Tt][sS]', tmp_file):
			cluster1.setTS(True)
		else:
			cluster1.setTS(False)
		cluster1.generateJobFromGjf(tmp_file)
os.chdir('../')
print 'Jobs generated successfully!'

# THE END


