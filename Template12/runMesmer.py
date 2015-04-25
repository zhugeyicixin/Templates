import os
import re
import shutil
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from lxml import etree

import mesmer

name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[7].strip(' \n')
		temperature = map(float, tmp_line.split())
		fr.close()			

if os.path.exists(os.getcwd()+'/mesmerOutput'):
	shutil.rmtree('mesmerOutput')
shutil.copytree('mesmerInput', 'mesmerOutput')

# constants
mesmer1 = mesmer.mesmer()

# run thermo
os.chdir('mesmerOutput')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	print tmp_file
	if re.search('.test',tmp_file):
		os.remove(tmp_file)
		continue
	if re.search('.log',tmp_file):
		os.remove(tmp_file)
		continue		
	if re.search('out_',tmp_file):
		os.remove(tmp_file)
	elif re.search('.xml', tmp_file):
		mesmer1.run(tmp_file)
	else:
		pass
os.chdir('..')

print '\nrun Mesmer successfully!\n'
		


