import sys
import subprocess
import os
from xlrd import *
from xlwt import *
import signal
import time

import THERMcalc

#variables
name = ''
site = ''
composition = ''
rotor = ''
symNum = ''
groupNum = ''
groupVariety = ''
groupID = []
groupQuantity = []
species = []

#flag
first_done = 0
step = 0
begin = 1
end = 1

#temporary variables
tmpNum = 0

# input area
# when using thermodynamicCompute_farnesane, the species with cd/co group should be noticed
# because cd/co is not found in THERM group lib
inputFileName='thermodynamicCompute_farnesane.xlsx'
outFileName='autoOut'


if os.path.exists(outFileName + '.lst'):
	os.remove(outFileName + '.lst')
if os.path.exists(outFileName + '.doc'):
	os.remove(outFileName + '.doc')
if os.path.exists(outFileName + '.dat'):
	os.remove(outFileName + '.dat')

wb = open_workbook(inputFileName)
sh = wb.sheet_by_index(0)
length = sh.nrows
width = sh.ncols

cmd = ['therm.exe']
# cmd = [sys.executable,'test_out.py']

print length
print width
step = length
while not end>length:
	first_done = 0

	begin = end
	if (end+length)>length:
		end = length
	else:
		end = end+length

	
	end = 1061

	if begin == end:
		break
	
	begin = 1053

	p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	print p.poll()

	THERMcalc.start(p)

	for i in range(begin,end):

		name = ''
		site = ''
		composition = ''
		rotor = ''
		symNum = ''
		groupNum = ''
		groupVariety = ''
		groupID = []
		groupQuantity = []
		species = []

		for j in range(0,width):
			print str(i) +'\t' + str(j) +':\t' + str(sh.cell_value(i,j)) + '\n'

		if not (int(sh.cell_value(i,0))==0 or int(sh.cell_value(i,0))==1):
			print 'beginning checking error in line ' + str(i) + ' in excel'
			break
		name = sh.cell_value(i,2)
		composition = sh.cell_value(i,5)
		rotor = str(int(sh.cell_value(i,6)))
		symNum = str(int(sh.cell_value(i,7)))
			
		# time.sleep(0.01)
		if sh.cell_value(i,3) == 'm':
			groupNum = str(int(sh.cell_value(i,8)))
			groupVariety = str(int(sh.cell_value(i,9)))
			tmpNum = int(groupVariety)
			for j in range(0,tmpNum):
				groupID.append(sh.cell_value(i,10+j*2))
				groupQuantity.append(str(int(sh.cell_value(i,11+j*2))))
			tmpNum = 0
			for item in groupQuantity:
				tmpNum += int(item)
			if not tmpNum == int(groupNum):
				print 'error! group number unequal to sum of groupVarieties! in line ' + str(i) + ' in excel'
			species=['\n', name+'\n', composition+'\n', '\n', groupNum+'\n', groupVariety+'\n', rotor+'\n']
			for index, item in enumerate(groupID):
				species.append(item+' '+groupQuantity[index]+'\n')
			if first_done != 1:
				# species += [symNum+'\n','\n','f\n',outFileName+str(end)+'\n','\n','\n',outFileName+str(end)+'\n']
				if step == length:
					species += [symNum+'\n','\n','f\n',outFileName+'\n','\n','\n',outFileName+'\n']
				else:
					if os.path.exists(str(end) + '.lst'):
						os.remove(str(end) + '.lst')
					if os.path.exists(str(end) + '.doc'):
						os.remove(str(end) + '.doc')
					if os.path.exists(str(end) + '.dat'):
						os.remove(str(end) + '.dat')				
					species += [symNum+'\n','\n','f\n',str(end)+'\n','\n','\n',str(end)+'\n']
				
				THERMcalc.firstMolecule(p,species)
				first_done = 1
			else:
				species += [symNum+'\n','\n','f\n']
				THERMcalc.molecule(p,species)
		elif sh.cell_value(i,3) == 'r':
			site = sh.cell_value(i,4)
			species=['r\n',site+'\n',symNum+'\n',name+'\n',composition+'\n','\n',rotor+'\n','\n','f\n']
			# if i==17:
			# 	print 'hi' + str(species)
			# 	# procName.stdin.write(''.join(species))
			# 	p.stdin.write('r\n')
			# 	print 'input:\tr\\n'
			# 	print 'output:'
			# 	THERMcalc.readOut(p,1)
			# 	# THERMcalc.readOut(p,1)
			# 	break
			THERMcalc.radical(p,species)
		else:
			print 'error! molecule or radical? in line ' + str(i) + ' in excel'

	print 'here 1'
	THERMcalc.mainWindow(p)
	print 'here 2'

	if step == length:
		THERMcalc.thermFit(p,outFileName)
	else:
		THERMcalc.thermFit(p,str(end))
	print p.poll()
	print 'This round ends!'
	# if step == length:
		# p.kill()
	# else:
	THERMcalc.kill(p)
	p.poll()
	print 'pid:\t' + str(p.pid) + '\n'
	# p.kill()
	
	# os.kill(p.pid,9)
	# time.sleep(3)
	# os.kill(p.pid)
	# print p.poll()



# species=['\n','c2h6\n','c2h6\n','\n','2\n','1\n','1\n','c/c/h3 2\n','18\n','\n','f\n','autoOut\n','\n','\n','autoOut\n']
# species2=['r\n','p\n','6\n','c2h5\n','c2h5\n','\n','1\n','\n','f\n']

# THERMcalc.molecule(p,species)
# THERMcalc.radical(p,species2)
# THERMcalc.molecule(p,species)
# THERMcalc.molecule(p,species)
# THERMcalc.mainWindow(p)
# THERMcalc.thermFit(p,outFileName)

print 'AutoTherm end successfully!'
