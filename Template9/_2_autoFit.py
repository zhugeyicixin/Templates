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
outFileName='COMBINED'


if os.path.exists(outFileName + '.doc'):
	os.remove(outFileName + '.doc')
if os.path.exists(outFileName + '.dat'):
	os.remove(outFileName + '.dat')



cmd = ['therm.exe']
# cmd = [sys.executable,'test_out.py']



p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print p.poll()

THERMcalc.start(p)


# THERMcalc.mainWindow(p)


THERMcalc.thermFit(p,outFileName)
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

print 'AutoFit end successfully!'
