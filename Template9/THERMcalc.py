import subprocess
import sys
import time

endLine=chr(32)+chr(13)+chr(10)

def readOut(procName,times):
	print '------------------------Start Line--------------------------------------'
	i=0
	endless=0
	while True:
		out = procName.stdout.readline()
		if out=='':
			endless+=1
			if endless>10:
				print 'Endless loop!'
				kill(procName)
				break
		else:
			endless = 0
		print out[0:-2]+'---'
		if out==endLine:
			print '*****************' + str(i)
			if not (i+1)<times:
				# print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
				break
			else:
				i += 1
	print '-------------------------End Line---------------------------------------\n'
	return

def start(procName):
	procName.stdin.write('\n')
	print 'input:\t\\n'
	print 'output:'
	readOut(procName,6)
	return

def firstMolecule(procName,species):
	procName.stdin.write(''.join(species))
	print 'input:\t'+str(species)
	print 'output:'
	readOut(procName,32)
	return

def molecule(procName,species):
	procName.stdin.write(''.join(species))
	print 'input:\t'+str(species)
	print 'output:'
	readOut(procName,30)
	return

def radical(procName,species):
	procName.stdin.write(''.join(species))
	print 'input:\t'+str(species)
	print 'output:'
	readOut(procName,28)
	return

def mainWindow(procName):
	procName.stdin.write('Q\n')
	print 'input:\tQ\\n'
	print 'output:'
	readOut(procName,3)
	return

def thermFit(procName,fileName):
	procName.stdin.write('8\n' + fileName + '\n' + fileName + '\n')
	print 'input:\t8\\n' + fileName + '\\n' + fileName + '\\n'
	print 'output:'
	readOut(procName,6)
	return

def kill(procName):
	procName.stdin.write('x\n')
	print 'input:\tx\\n'
	time.sleep(2)
	if procName.poll()==None:
		procName.stdin.write('q\nx\n')
		print 'input:\tq\\nx\\n'
		time.sleep(2)

	return
	
