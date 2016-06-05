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

#definition of constants

#definition of parameters


# symbol indicating the position
pattern_name = re.compile('^.*formatted.*$')

#constants
space=('',' ','  ','   ','    ','     ','      ','       ','        ','         ','          ','           ')

#flags


# temporary variables
tmp_line = ''
tmp_name = ''

wb = open_workbook('thermodynamicCompute_farnesane.xlsx')
sh = wb.sheet_by_index(0)
speciesNum = sh.nrows-1

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
			for i in range(0,speciesNum):
				tmp_line = lines[i*4+2]
				tmp_name = sh.cell_value(i+1,2)
				if len(tmp_name)<9:
					tmp_name = tmp_name + space[9-len(tmp_name)]
				if tmp_name[0:9].lower()==tmp_line[0:9].lower():
					tmp_name = sh.cell_value(i+1,1)
					tmp_line = tmp_line[0:9] + '         1010  ' + tmp_line[24:77] + '  1\n'
					tmp_line = tmp_name + tmp_line[len(tmp_name):]
					lines[i*4+2] = tmp_line
				else:
					print 'Error! Not the same species!\t' + str(i) + '\t' + tmp_name + '\t' + tmp_line[0:9]
					break
			fw = file(tmp_file,'w')
			fw.writelines(lines)
			fw.close()

print 'NASA thermodynamic data reformated successfully!'

# THE END


