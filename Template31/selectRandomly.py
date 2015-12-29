import re
import random
import shutil
import os

# variables
carbonDict = {}

# constants
pattern_folder = re.compile('^C([0-9]+)H[0-9]+_.*gjf$')

# temporary variables
carbonNum = 0

if os.path.exists('testCases'):
	shutil.rmtree('testCases')
os.mkdir('testCases')

pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)

for tmp_file in tmp_fileList:
	tmp_m = pattern_folder.match(tmp_file)
	if tmp_m:
		carbonNum = int(tmp_m.group(1))
		if carbonNum not in carbonDict.keys():
			carbonDict[carbonNum] = []
		carbonDict[carbonNum].append(tmp_file)

for tmp_item in carbonDict.items():
	selectedFile = []
	print 'C ' + str(tmp_item[0]) + ':'
	while len(selectedFile) < 20:
		tmp_num = random.randrange(0, len(tmp_item[1]))
		tmp_file = tmp_item[1][tmp_num]
		if tmp_file in selectedFile:
			continue
		else:
			selectedFile.append(tmp_file)
			print tmp_file
			shutil.copy(tmp_file, os.path.join('testCases', tmp_file))



