# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
from xlwt import *
import pyExcelerator
from xlutils.copy import copy
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
clusterPath = '/home/hetanjin/Frog/CnH2n_3'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)

# definetion of comparing pattern

#variables
gjfFiles = []

#flags

# temporary variables

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)

for tmp_file in tmp_fileLists:
	if re.search('\.gjf', tmp_file):
		gjfFiles.append(tmp_file)
			
cluster1.genFrogInputFromGjf(gjfFiles)

print 'Jobs generated successfully!'

# THE END


