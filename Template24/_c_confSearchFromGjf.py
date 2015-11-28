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
clusterPath = '/home/hetanjin/newGroupAdditivityFrog2/CnH2n+2_6'

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

os.chdir('_c_confSearch')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)

for tmp_file in tmp_fileLists:
	if re.search('\.gjf', tmp_file):
		gjfFiles.append(tmp_file)
			
cluster1.genFrogInputFromGjf(gjfFiles)
os.chdir('../')

print 'Jobs generated successfully!'

# THE END


