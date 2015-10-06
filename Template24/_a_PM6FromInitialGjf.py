# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
import re
import os
import shutil
import cluster
import time

#input
# cluster could be set as cce or Tsinghua100
# the path where the jobs would lie should be announced
clusterName = 'cce'
clusterPath = '/home/hetanjin/newGroupAdditivityFrog2/CnH2n+2_2'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)

# definetion of comparing pattern

#variables

#flags

# temporary variables

if os.path.exists('_b_PM6PreOptimization'):
	shutil.rmtree('_b_PM6PreOptimization')
os.mkdir('_b_PM6PreOptimization')

tmp_fileList = os.listdir('_a_initialGeomGjf')
for tmp_file in tmp_fileList:
	shutil.copy(os.path.join('_a_initialGeomGjf', tmp_file), os.path.join('_b_PM6PreOptimization', tmp_file))
time.sleep(10)

os.chdir('_b_PM6PreOptimization')
pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)

for tmp_file in tmp_fileList:
	if re.search('\.gjf', tmp_file):
		if re.search('[Tt][sS]', tmp_file):
			cluster1.setTS(True)
		else:
			cluster1.setTS(False)
		cluster1.generateJobFromGjf(tmp_file, method='PM6', freq=False)

print 'Jobs generated successfully!'

# THE END


