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
pattern_name = re.compile('^.*rename.*$')

#constants
space=('',' ','  ','   ','    ','     ','      ','       ','        ','         ','          ','           ','            ','             ','              ','               ','                ','                 ','                  ')

#flags


# temporary variables
tmp_line = ''
tmp_name = ''

wb = open_workbook('thermodynamicCompute_farnesane_rename.xlsx')
sh = wb.sheet_by_index(1)
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
				tmp_name = sh.cell_value(i+1,3)
				if len(tmp_name)<18:
					tmp_name = tmp_name + space[18-len(tmp_name)]
				if tmp_name[0:18].lower()==tmp_line[0:18].lower():
					if not sh.cell_value(i+1,2)=='':
						tmp_name = sh.cell_value(i+1,2)
						tmp_name = tmp_name + space[18-len(tmp_name)] + '1010'
						tmp_line = tmp_name + tmp_line[22:]
						lines[i*4+2] = tmp_line
						print tmp_name
				else:
					print 'Error! Not the same species!\t' + str(i) + '\t' + tmp_name + '\t' + tmp_line[0:18]
					break
			fw = file(tmp_file,'w')
			fw.writelines(lines)
			fw.close()

print 'NASA thermodynamic data renamed successfully!'

# THE END


