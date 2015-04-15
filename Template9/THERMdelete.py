# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os
import shutil
from collections import Counter

#definition of constants

#definition of parameters


# symbol indicating the position
pattern_name = re.compile('^.*deleted.*$')

#variables
speciesBase=[]

#constants


#flags


# temporary variables
tmp_line = ''
tmp_name = ''
tmp_num = 0

wb = open_workbook('thermodynamicCompute_farnesane_delete.xlsx')
sh = wb.sheet_by_index(2)

rows=sh.nrows

for i in range(1,rows):
	# print sh.cell_value(i,2)
	tmp_num = int(sh.cell_value(i,2))
	for j in range(0,tmp_num):
		speciesBase.append(sh.cell_value(i,3+j))
# print speciesBase
print len(speciesBase)
# print Counter(speciesBase)
speciesBase=set(speciesBase)
print len(speciesBase)

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.DAT',tmp_file):
		tmp_m = pattern_name.match(tmp_file[0:-4])
		if tmp_m:
			print tmp_file
			fr = file(tmp_file,'r')
			lines=fr.readlines()
			fr.close()
			# tmp_num = len(lines) - 1
			# while tmp_num >=0:
			# 	if lines[tmp_num][79]=='1':
			# 		if not lines[tmp_num][0:18].strip() in speciesBase:
			# 			del lines[tmp_num:tmp_num+4]
			# 		tmp_num -= 4
			# 	else:
			# 		tmp_num -= 1

			while tmp_num<len(lines):
				if lines[tmp_num][79]=='1':
					tmp_name = lines[tmp_num][0:18].strip()
					if not tmp_name in speciesBase:
						del lines[tmp_num:tmp_num+4]
					else:
						speciesBase.remove(tmp_name)
						tmp_num += 4
				else:
					tmp_num += 1

			fw = file(tmp_file,'w')
			fw.writelines(lines)
			fw.close()

print len(speciesBase)
print speciesBase
print 'NASA thermodynamic data renamed successfully!'

# THE END


