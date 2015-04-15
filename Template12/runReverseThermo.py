import os
import re
import shutil
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy

name = ''
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
os.chdir('thermoReverseInput')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.out',tmp_file):
		os.remove(tmp_file)
	else:
		os.system('thermo ' + tmp_file)
tmp_fileLists = os.listdir(pwd)
tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('.out',tmp_file)]
os.chdir('..')

if os.path.exists(os.getcwd()+'/thermoReverseOutput'):
	shutil.rmtree('thermoReverseOutput')
os.mkdir('thermoReverseOutput')
	
for tmp_file in tmp_fileLists:
	shutil.move('thermoReverseInput/'+tmp_file,'thermoReverseOutput')

wb=open_workbook(name + '.xls')
wb_new = copy(wb)
sh=wb_new.get_sheet(3)				#if overwrite to use cell_overwrite_ok=True
sh.cell_overwrite_ok = True
tmp_row = 2
for tmp_file in tmp_fileLists:
	sh.write(tmp_row,0,tmp_file[7:-4])
	fd=file('thermoReverseOutput/'+tmp_file,'r')
	lastlines = fd.readlines()[-29:]
	for tmp_line in lastlines:
		tmp_line.rstrip()
		tmp_line = tmp_line.split()
		for i in range(len(tmp_line)):
			sh.write(tmp_row,i+1,float(tmp_line[i]))
		tmp_row += 1
	fd.close()
	tmp_row += 1

wb_new.save(name + '.xls')

print 'run Reverse Thermo successfully!'
		


