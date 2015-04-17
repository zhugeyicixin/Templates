import os
import shutil
import re

pwd = os.getcwd()

if os.path.exists(pwd + '/thermoInputATM'):
	shutil.rmtree(pwd + '/thermoInputATM')
os.mkdir('thermoInputATM')
if os.path.exists(pwd + '/thermoReverseInputATM'):
	shutil.rmtree(pwd + '/thermoReverseInputATM')
os.mkdir('thermoReverseInputATM')

# transfer MCC to ATM and save
pwd = os.getcwd()
tmp_pwd = pwd + '/thermoInput'
tmp_fileLists = os.listdir(tmp_pwd)
for tmp_file in tmp_fileLists:
	if re.search('.dat',tmp_file):
		fr = file(tmp_pwd + '/' + tmp_file, 'r')
		tmp_lines = fr.readlines()
		fr.close()
		tmp_lines[0]='KCAL  ATM\n'
		fw = file('thermoInputATM/' + tmp_file,'w')
		fw.writelines(tmp_lines)
		fw.close()

tmp_pwd = pwd + '/thermoReverseInput'
tmp_fileLists = os.listdir(tmp_pwd)
for tmp_file in tmp_fileLists:
	if re.search('.dat',tmp_file):
		fr = file(tmp_pwd + '/' + tmp_file, 'r')
		tmp_lines = fr.readlines()
		fr.close()
		tmp_lines[0]='KCAL  ATM\n'
		fw = file('thermoReverseInputATM/' + tmp_file,'w')
		fw.writelines(tmp_lines)
		fw.close()

print 'save Thermo ATM files successfully!\n'
		


