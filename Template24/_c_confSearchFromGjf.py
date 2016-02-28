# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil
import cluster
import chem


#input
# cluster could be set as cce or Tsinghua100
# the path where the jobs would lie should be announced
clusterName = 'cce'
clusterPath = '/home/hetanjin/newGroupAdditivityFrog2/CnH2n_5'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)
cluster1.setJmolPath('jmol-14.2.15_2015.07.09')

# definetion of comparing pattern

#variables
gjfFiles = []

#flags

# temporary variables

if os.path.exists('_c_confSearch_Balloon'):
	shutil.rmtree('_c_confSearch_Balloon')
shutil.copytree('_c_confSearch', '_c_confSearch_Balloon')
os.chdir('_c_confSearch_Balloon')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)

for tmp_file in tmp_fileLists:
	if re.search('\.gjf', tmp_file):
		gjfFiles.append(tmp_file)
			
cluster1.genBalloonInputFromGjf(gjfFiles)
os.chdir('../')

if os.path.exists('_c_confSearch_Frog'):
	shutil.rmtree('_c_confSearch_Frog')
shutil.copytree('_c_confSearch', '_c_confSearch_Frog')
os.chdir('_c_confSearch_Frog')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)

for tmp_file in tmp_fileLists:
	if re.search('\.gjf', tmp_file):
		gjfFiles.append(tmp_file)
			
cluster1.genFrogInputFromGjf(gjfFiles)
os.chdir('../')

print 'Jobs generated successfully!'

# THE END


