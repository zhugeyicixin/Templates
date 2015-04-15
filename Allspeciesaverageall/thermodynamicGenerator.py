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
import subprocess
import time
import msvcrt

pwd = os.getcwd()
wb = open_workbook('averageEnthalpyofFormation.xlsx')
sh = wb.sheet_by_index(0)
enthalpyDict = {}
for i in range(0,sh.ncols):
# for i in range(0,1):
	name = sh.cell_value(0,i)
	if os.path.exists(pwd + '/' + name):
		shutil.rmtree(pwd + '/' + name)
	os.mkdir(pwd + '/' + name)
	os.chdir(name)
	tmp_file = file('fort.15','w')
	tmp_file.write(
sh.cell_value(1,i) + '''         N        (N for nonlinear, L for linear)
''' + str(int(sh.cell_value(2,i))) + ' ' + str(sh.cell_value(3,i))	+ 	'''          Number of atoms, molecular weight
''' + str(sh.cell_value(4,i)) + '''				Enthalpy of formation at the standard state!kcal
''' + str(sh.cell_value(5,i)) + ''' 1    Rotational constat (cm-1), symmetry number
1         Statistical weight
0         Number of internal rotor, Br, sigma, dim, vr 
''')
	j = 7
	while j < sh.nrows and sh.cell_value(j,i) != '':
		tmp_file.write(str(sh.cell_value(j,i))+'\n')
		j += 1

	enthalpyDict[sh.cell_value(0,i)] = sh.cell_value(1,i)
	tmp_file.close()
	print name
	shutil.copyfile('../stherm.exe','stherm.exe')
	p = subprocess.Popen("stherm.exe", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
	p.stdin.write('1\n')
	p.wait()
	shutil.copyfile('fort.16', '../out_' + name + '.txt')
	shutil.copyfile('fort.26', '../NASA_' + name + '.txt')
	tmp_file = file('fort.26')
	lines = tmp_file.readlines()
	tmp_file.close()
	tmp_file = file('../NASA_ALL.txt','a')
	tmp_file.write(name + '\n')
	tmp_file.writelines(lines)
	os.chdir('../')

print 'stherm input scripts generated successfully!'

# THE END


