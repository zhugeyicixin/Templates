# this is used to generate database for group additivity method
from xlwt import *
import os
import re

import textExtractor
import chem

###########################################
# extract geometry and energy form log file
###########################################
# get commands from .name file
__energy__ = 'b3lyp'
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[3].strip(' \n')
		if tmp_line == 'cbs':
			__energy__ = 'cbs'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs freq and energy are used in this calculation\n-------------------------------------\n'
		elif re.match('b3lyp', (tmp_line.strip()).lower()) != None:
			__energy__ = 'b3lyp'
			print '\n-------------------------------------\nb3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'cbsb3lyp':
			__energy__ = 'cbsb3lyp'
			print '\n-------------------------------------\ncbs verified and b3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'M062X/def2TZVP//B3LYP/6-31G(d)':
			__energy__ = 'M062X/def2TZVP//B3LYP/6-31G(d)'
			print '\n-------------------------------------\nM062X energy and b3lyp geom are used in this calculation\n-------------------------------------\n'	
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'
		fr.close()	


#definition of goal parameters
name = []
multi = []
geom = []
formula = []
atomsNum = []

#definetion of comparing pattern
pattern_gjfFile = re.compile('^(C[0-9]*H[0-9OH]*_*[0-9]*).*\.gjf$')
pattern_gjfCommand = re.compile('^.*#p?.*$')
pattern_gjfMulti = re.compile('^.*([0-9]+) +([0-9]+).*$')
pattern_blankLine = re.compile('^ *$')

#definition of counter
speciesNum = 0		#	this is the total number of species in the database

#definition of flags
gjfCommand_done = -1
gjfMulti_done = -1
geomDone = -1

#definition of temporary variables
tmp_m = []		#match result 
lineStart = 0
lineEnd = 0

#extract info
pwd = os.getcwd()
tmp_fileLists = os.listdir(os.path.join(pwd, 'Gjfs'))

for tmp_file in tmp_fileLists:
	print tmp_file
	tmp_m = pattern_gjfFile.match(tmp_file)
	if tmp_m:
		tmp_name = tmp_m.group(1)
		gjfFile = file(os.path.join('Gjfs', tmp_file), 'r')

		#reset all variables		
		gjfCommand_done = -1
		gjfMulti_done = -1
		geomDone = -1

		lineStart = 0
		lineEnd = 0

		tmp_lines = gjfFile.readlines()
		for (lineNum, tmp_line) in enumerate(tmp_lines):
			if gjfCommand_done != 1:
				tmp_m = pattern_gjfCommand.match(tmp_line)
				if tmp_m:
					gjfCommand_done = 1
			elif gjfMulti_done != 1:
				tmp_m = pattern_gjfMulti.match(tmp_line)
				if tmp_m:
					lineStart = lineNum
					multi.append(int(tmp_m.group(2)))
					geomDone = 0
					gjfMulti_done = 1
			elif geomDone != 1:
				tmp_m = pattern_blankLine.match(tmp_line)
				if tmp_m:
					lineEnd = lineNum
					geom.append(tmp_lines[lineStart+1: lineEnd])
					geomDone = 1


				
		gjfFile.close()


		tmp_mole = chem.molecule()
		tmp_mole.getGjfGeom(geom[-1])
		tmp_mole.calcFormula()
		formula.append(tmp_mole.formula)
		atomsNum.append(tmp_mole.getAtomsNum())

		name.append(tmp_name)
		speciesNum += 1

###########################################
# write info to excel
###########################################
wb = Workbook()
sh = wb.add_sheet('speciesInfo')
sh.cell_overwrite_ok = True

tmp_row = 0
tmp_col = 0

sh.write(tmp_row, tmp_col, 'Name Abbreviation')
sh.write(tmp_row, tmp_col+1, 'Name')
sh.write(tmp_row, tmp_col+2, 'Formula')
sh.write(tmp_row, tmp_col+3, 'Atoms Number')
sh.write(tmp_row, tmp_col+4, 'SCF Energy in freq')
sh.write(tmp_row, tmp_col+5, 'ZPE Energy in freq')
sh.write(tmp_row, tmp_col+6, 'Enthalpy in freq')
sh.write(tmp_row, tmp_col+7, 'SP Energy in energy')
sh.write(tmp_row, tmp_col+8, 'SP Energy (0 K) in energy corrected with freq scaling factor')
sh.write(tmp_row, tmp_col+9, 'SP Enthalpy (298.15 K) in energy corrected with freq scaling factor')
sh.write(tmp_row, tmp_col+10, 'Multiplicity')
sh.write(tmp_row, tmp_col+11, 'External Symmetry Number')
sh.write(tmp_row, tmp_col+12, 'Geometry')

tmp_row = 1
tmp_col = 0
for i in xrange(speciesNum):
	sh.write(tmp_row, tmp_col, name[i])
	sh.write(tmp_row, tmp_col+1, name[i])
	sh.write(tmp_row, tmp_col+2, formula[i])
	sh.write(tmp_row, tmp_col+3, atomsNum[i])
	sh.write(tmp_row, tmp_col+4, 0.0)
	sh.write(tmp_row, tmp_col+5, 0.0)
	sh.write(tmp_row, tmp_col+6, 0.0)
	sh.write(tmp_row, tmp_col+7, 0.0)
	# ZPE scaling factor from Truhlar used here
	sh.write(tmp_row, tmp_col+8, 0.0)
	sh.write(tmp_row, tmp_col+9, 0.0)
	sh.write(tmp_row, tmp_col+10, multi[i])
	sh.write(tmp_row, tmp_col+11, 0)
	sh.write(tmp_row, tmp_col+12, geom[i])
	tmp_row += 1

wb.save('database.xls')

