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
R=1.987
cal=4.184

#definition of parameters
speciesNum=0
speciesDict = {}
temperature=[]
enthalpy=[]
cv=[]
entropy=[]
cp=[]


# symbol indicating the position
pattern_name = re.compile('^.*_1_therm$')
pattern_temperature0 = re.compile('^ # b3lyp/cbsb7 freq.*$')
pattern_temperature = re.compile('^ # b3lyp/cbsb7 freq temperature=([0-9]+\.[0-9]+) geom=allcheck.*$')
pattern_enthalpy = re.compile('^.*Sum of electronic and thermal Enthalpies= *(-?[0-9]+\.[0-9]+).*$')
pattern_cv = re.compile('^.*Total *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')

#flags
temperature_done = 0
enthalpy_done = 0
cv_done = 0

# temporary variables
tmp_row = 0

# pwd = os.getcwd()
# tmp_fileLists = os.listdir(pwd)
# wb_template = open_workbook('thermodynamicDataTemplate.xlsx')
# sh = wb_template.sheet_by_index(0)
# speciesNum = sh.nrows-1
# for i in range(1,speciesNum+1):
# 	speciesDict[sh.cell_value(i,0)] = sh.cell_value(i,3)

# wb=copy(wb_template)
# sh = wb.get_sheet(0)

# fw = file('RMG.txt','w')
# fw.write(
# ''' 2,6-DMH
#  SPECIES       Hf       S    Cp 300     400     500     600     800     1000     1500     DATE        ELEMENTS
# ''')
# fw.close()
# for tmp_file in tmp_fileLists:
# 	print tmp_file
# 	temperature=[]
# 	enthalpy=[]
# 	cv=[]
# 	entropy=[]
# 	cp=[]

# 	temperature_done = 0
# 	enthalpy_done = 1
# 	cv_done = 1

# 	if re.search('.log',tmp_file):
# 		tmp_m = pattern_name.match(tmp_file[0:-4])
# 		if tmp_m:
# 			fr = file(tmp_file,'r')
# 			lines=fr.readlines()
# 			for tmp_line in lines:
# 				if temperature_done	!= 1:
# 					tmp_m = pattern_temperature0.match(tmp_line)
# 					if tmp_m:
# 						temperature.append(298.15)
# 						temperature_done = 1
# 						enthalpy_done = 0
# 				if enthalpy_done != 1:
# 					tmp_m = pattern_enthalpy.match(tmp_line)
# 					if tmp_m:
# 						enthalpy.append(float(tmp_m.group(1))) 
# 						enthalpy_done = 1
# 						cv_done = 0
# 				if cv_done != 1:
# 					tmp_m = pattern_cv.match(tmp_line)
# 					if tmp_m:
# 						cv.append(float(tmp_m.group(2)))
# 						entropy.append(float(tmp_m.group(3)))
# 						cp.append(float(cv[-1])+R)
# 						cv_done = 1
# 						temperature_done = 0
# 						break

# 			for tmp_line in lines:
# 				if temperature_done != 1:
# 					tmp_m = pattern_temperature.match(tmp_line)
# 					if tmp_m:
# 						temperature.append(float(tmp_m.group(1)))
# 						temperature_done = 1
# 						enthalpy_done = 0
# 				if enthalpy_done != 1:
# 					tmp_m = pattern_enthalpy.match(tmp_line)
# 					if tmp_m:
# 						enthalpy.append(float(tmp_m.group(1)))
# 						enthalpy_done = 1
# 						cv_done = 0
# 				if cv_done != 1:
# 					tmp_m = pattern_cv.match(tmp_line)
# 					if tmp_m:
# 						cv.append(float(tmp_m.group(2)))
# 						entropy.append(float(tmp_m.group(3)))
# 						cp.append(cv[-1]+R)
# 						cv_done = 1
# 						temperature_done = 0
# 			fr.close()
			
# 			tmp_row = speciesDict[tmp_file[0:-12]]
# 			#sh.write(tmp_row,4,enthalpy[0])
# 			sh.write(tmp_row,5,entropy[0])
# 			sh.write(tmp_row,6,cp[1])
# 			sh.write(tmp_row,7,cp[2])
# 			sh.write(tmp_row,8,cp[3])
# 			sh.write(tmp_row,9,cp[4])
# 			sh.write(tmp_row,10,cp[5])
# 			sh.write(tmp_row,11,cp[6])
# 			sh.write(tmp_row,12,cp[7])

# 			# if len(tmp_file) > 21:
# 			# 	print 'hello'
# 			# 	fw.write(tmp_file[-21:-12]+'\t'+str(enthalpy[0])+'\t'+str(entropy[0])+'\t'+str(cp[1])+'\t'+str(cp[2])+'\t'+str(cp[3])+'\t'+str(cp[4])+'\t'+str(cp[5])+'\t'+str(cp[6])+'\t'+str(cp[7])+'\t5/29/14 THERM   C   9 H  20     0     0 G 8')
# 			# else:
# 			# 	print 'hi'
# 			# 	fw.write(tmp_file[0:-12]+'\t'+str(enthalpy[0])+'\t'+str(entropy[0])+'\t'+str(cp[1])+'\t'+str(cp[2])+'\t'+str(cp[3])+'\t'+str(cp[4])+'\t'+str(cp[5])+'\t'+str(cp[6])+'\t'+str(cp[7])+'\t5/29/14 THERM   C   9 H  20     0     0 G 8')
# 			# fw.write('temperature\t\tenthalpy\t\tentropy\t\tcp\n')
# 			# fw = file('thermoOut.txt','a')
# 			# for i in range(0,len(temperature)):
# 				# fw.write(str(temperature[i]) + '\t\t\t' + str(enthalpy[i]) + '\t\t' + str(entropy[i]) + '\t\t' + str(cv[i]) + '\t\t' + str(cp[i]) + '\n')
# 			# fw.close()

# wb.save('thermodynamicData.xls')

wb = open_workbook('thermodynamicData.xls')
sh = wb.sheet_by_index(0)
speciesNum = sh.nrows-1
fw = file('RMG.LST','w')
fw.write(
''' 2,6-DMH
 SPECIES       Hf       S    Cp 300     400     500     600     800     1000     1500     DATE        ELEMENTS
''')
fw.close()
for i in range(1,speciesNum+1):
	print sh.cell_value(i,4)
	if sh.cell_value(i,4) == '':
		continue
	fw = file('RMG.LST','a')	
	print sh.cell_value(i,16)
	if int(sh.cell_value(i,16)) != 0:
		print 'hi1'
		fw.write(' %-9s %7.2f   %6.2f   %6.2f  %6.2f  %6.2f  %6.2f  %6.2f  %6.2f  %6.2f   %s THERM   c  %2d h  %2d o   %d     0 G %d\n'%(sh.cell_value(i,1),\
			sh.cell_value(i,4),sh.cell_value(i,5),sh.cell_value(i,6),sh.cell_value(i,7),\
			sh.cell_value(i,8),sh.cell_value(i,9),sh.cell_value(i,10),sh.cell_value(i,11),\
			sh.cell_value(i,12),sh.cell_value(i,13),sh.cell_value(i,14),sh.cell_value(i,15),\
			sh.cell_value(i,16),int(sh.cell_value(i,17))))
	else:
		print 'hi2'
		fw.write(' %-9s %7.2f   %6.2f   %6.2f  %6.2f  %6.2f  %6.2f  %6.2f  %6.2f  %6.2f   %s THERM   c  %2d h  %2d     0     0 G %d\n'%(sh.cell_value(i,1),\
			sh.cell_value(i,4),sh.cell_value(i,5),sh.cell_value(i,6),sh.cell_value(i,7),\
			sh.cell_value(i,8),sh.cell_value(i,9),sh.cell_value(i,10),sh.cell_value(i,11),\
			sh.cell_value(i,12),sh.cell_value(i,13),sh.cell_value(i,14),sh.cell_value(i,15),\
			int(sh.cell_value(i,17))))

	fw.close()

print 'thermodynamic data generated successfully!'

# THE END


