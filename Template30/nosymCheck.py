# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil


pattern_command = re.compile('^.*#p.*$',re.I)
pattern_nosym = re.compile('^.*#p.*nosym.*|.*#p.*sym.*$',re.I)
pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')
pattern_freq = re.compile('^.*Frequencies -- *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)? *(-?[0-9]+\.[0-9]+)?$')

error_file_num = 0
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if os.path.isfile(tmp_file):
		continue

	# print tmp_file
	if os.path.exists(os.path.join(tmp_file, tmp_file+'.log')):
		fr = file(os.path.join(tmp_file, tmp_file+'.log'), 'r')
		tmp_lines = fr.readlines()
		tmp_m = pattern_end.match(tmp_lines[-1])
		if tmp_m:
			command_done = -1
			totalLineNum = len(tmp_lines)
			for (index_line, tmp_line) in enumerate(tmp_lines):
				if command_done != 1:
					if index_line < totalLineNum:
						tmp_twoLine = tmp_line.strip() + tmp_lines[index_line+1].strip()
					else:
						tmp_twoLine = tmp_line
					tmp2_m = pattern_command.match(tmp_line)
					if tmp2_m:
						# print tmp_twoLine
						tmp3_m = pattern_nosym.match(tmp_twoLine)
						if tmp3_m:
							print 'Attention! The keyword NOSYM is used! ', tmp_file
							print tmp_twoLine
						command_done = 1
						break
		else:
			print 'Error1! ' + 'File did not end normally! ' + tmp_file
			error_file_num += 1				
	else:
		print 'Error! Log file not found! ', tmp_file
		error_file_num += 1		

print 'error_file_num: ', error_file_num

# THE END




