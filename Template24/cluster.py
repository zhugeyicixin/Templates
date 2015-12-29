# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import shutil
import textExtractor
import chem

# definetion of comparing pattern
pattern_multi = re.compile('^.*spinMultiplicity: *([0-9]+).*$')
pattern_atom = re.compile('^.*[A-Z] *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
pattern_rotation = re.compile('^ *([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+).*$')
pattern_fixBond = re.compile('^ *([0-9]+) ([0-9]+).*$')

pattern_gjfCommand = re.compile('^.*#p?.*$')
pattern_gjfMulti = re.compile('^.*([0-9]+) +([0-9]+).*$')
pattern_blankLine = re.compile('^ *$')

pattern_logMulti = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_logFreqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
pattern_logStandard = re.compile('^.*Standard orientation:.*$') 
pattern_logInput = re.compile('^.*Input orientation:.*$') 
pattern_logEndline = re.compile('^.*---------------------------------------------------------------------.*$')


class cluster:
	name = ''
	jobLocation = ''
	JmolPath = ''

	_g09D01 = False
	_dispersionD3 = False
	_scratchStrategy = False
	_TS = False

	def __init__(self, name, clusterPath):
		self.name = name
		self.jobLocation = clusterPath
		self.JmolPath = ''

		self._g09D01 = False
		self._dispersionD3 = False
		self._scratchStrategy = False
		self._TS = False

	def setJobLocation(self, clusterPath):
		self.jobLocation = clusterPath

	def setJmolPath(self, JmolProgPath):
		self.JmolPath = JmolProgPath

	def setG09D01(self, useG09D01):
		self._g09D01 = useG09D01

	def setDispersionD3(self, useDispersionD3):
		self._dispersionD3 = useDispersionD3

	def setScratchStractegy(self, useScratchStrategy):
		self._scratchStrategy = useScratchStrategy		

	def setTS(self, isTS):
		self._TS = isTS		

	def generateRotScanJobs(self, pathway='',barrierless=False):
		# variables
		rotations = []
		fixedBond = []

		# flags
		multi_done = -1
		atom_begin = -1
		atom_done = -1
		rotation_done = -1
		if barrierless == True:
			fixBond_done = -1
		else: 
			fixBond_done = 1


		if pathway == '':
			pathway = os.getcwd()

		tmp_fileLists = os.listdir(pathway)
		for tmp_file in tmp_fileLists:
			if os.path.isdir(os.path.join(pathway, tmp_file)):
				tmp2_fileLists = os.listdir(os.path.join(pathway, tmp_file))
				for tmp2_file in tmp2_fileLists:
					if re.search('\.rot', tmp2_file):
						multi_done = -1
						atom_begin = -1
						atom_done = -1
						rotation_done = -1
						if barrierless == True:
							fixBond_done = -1
						else:
							fixBond_done = 1

						rotations = []
						fixedBond = []

						fr = file(os.path.join(pathway, tmp_file, tmp2_file), 'r')
						tmp_lines = fr.readlines()
						for (lineNum,tmp_line) in enumerate(tmp_lines):
							if multi_done != 1:
								tmp_m = pattern_multi.match(tmp_line)
								if tmp_m:
									multi = int(tmp_m.group(1))
									multi_done = 1
							elif atom_begin < 0:
								tmp_m = pattern_atom.match(tmp_line)
								if tmp_m:
									atom_begin = lineNum
							elif atom_done < 0:
								tmp_m = pattern_atom.match(tmp_line)
								if not tmp_m:
									atom_done = lineNum
							elif rotation_done != 1:
								tmp_m = pattern_rotation.match(tmp_line)
								if tmp_m:
									rotations.append(tmp_m.groups())
									rotation_done = 0
								elif rotation_done == 0:
									rotation_done =1
							elif fixBond_done != 1:
								tmp_m = pattern_fixBond.match(tmp_line)
								if tmp_m:
									fixedBond = [int(tmp_m.group(1)), int(tmp_m.group(2))]
									fixBond_done = 1
						fr.close()

						for tmp_rotation in rotations:

							tmp_num = 1
							tmp_dir = ''.join([tmp2_file[0:-4], '_', tmp_rotation[1], '_', tmp_rotation[2], '_', str(tmp_num), '_scan_b3631gd'])
							tmp_dir_path = os.path.join(pathway, tmp_file, tmp_dir)
							while os.path.exists(tmp_dir_path):
								tmp_num += 1
								tmp_dir = ''.join([tmp2_file[0:-4], '_', tmp_rotation[1], '_', tmp_rotation[2], '_', str(tmp_num), '_scan_b3631gd'])
								tmp_dir_path = os.path.join(pathway, tmp_file, tmp_dir)
							os.mkdir(tmp_dir_path)
							fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
							if self.name == 'Tianhe' or self.name == 'Tianhe2':
								fw.write(
'''%mem=16GB
%nprocshared=12
%chk=''')
							else:
								fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
							if self.name == 'Tsinghua100' and self._scratchStrategy == True:
								fw.write('/scratch/')
							if self._dispersionD3 == False:
								fw.write(tmp_dir + '.chk\n')
							if self._TS == False:
								if multi != 1:
									fw.write('#p ub3lyp/6-31g(d) opt=modredundant nosym')
								else:
									fw.write('#p b3lyp/6-31g(d) opt=modredundant nosym')
							else:
								if multi != 1:
									fw.write('#p ub3lyp/6-31g(d) opt=(TS, calcfc,modredundant,noeigentest) nosym')
								else:
									fw.write('#p b3lyp/6-31g(d) opt=(TS, calcfc,modredundant,noeigentest) nosym')
							if self._dispersionD3 == False:
								fw.write('\n')
							else:
								fw.write(' EmpiricalDispersion=GD3\n')
							fw.write(
'''
using ub3lyp/6-31G(d) to scan

0 ''')
							fw.write(''.join([str(multi), '\n'] + tmp_lines[atom_begin: atom_done] + ['\n', \
								'D ', tmp_rotation[0], ' ', tmp_rotation[1], ' ', tmp_rotation[2], ' ', tmp_rotation[3], ' ', 'S 40 10.0\n']))
							if barrierless == True:
								fw.write(''.join(['B ', str(fixedBond[0]),' ', str(fixedBond[1]), ' F\n']))
							fw.write('\n\n\n\n\n')
							fw.close()
							os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
							
							fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
							if self.name == 'cce':
								if self._g09D01 == False:
									fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /share/apps
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
								else:
									fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /home/hetanjin/apps/g09D01
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
							elif self.name == 'Tsinghua100':
								fw.write(
# Tsinghua100 cluster
'''#BSUB -J ''' + tmp_dir + '''
#BSUB -q hpc_linux
#BSUB -R "select[mem>30000]"
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -o ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''/output.%J
#BSUB -e ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''/error.%J

export g09root=/home/hexin/gaussian
export GAUSS_SCRDIR=/scratch
source $g09root/g09/bsd/g09.profile

''')

								if self._scratchStrategy == True:
									fw.write(
'''rm /scratch/*
cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk /scratch/''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.chk ''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.fchk ''' + tmp_dir + '''.fchk
rm /scratch/*



''')
								else:
									fw.write(
'''cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
							elif self.name == 'Tianhe':
								if self._g09D01 == False:
									fw.write(
# Tianhe cluster
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you/g09/g09 ''' + tmp_dir + '''.gjf



''')
								else:
									fw.write(
# Tianhe cluster
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you/scratch
export g09root=/vol-th/home/you/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')
							elif self.name == 'Tianhe2':
								if self._g09D01 == False:
									fw.write(
# Tianhe cluster you1
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you1/g09/g09 ''' + tmp_dir + '''.gjf



''')
								else:
									fw.write(
# Tianhe cluster you1
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you1/scratch
export g09root=/vol-th/home/you1/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_file + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')									
							fw.close()
							os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
						if self.name == 'cce':
							if os.path.exists('submit12.sh'):
								shutil.copy('submit12.sh', os.path.join(pathway, tmp_file))
							if os.path.exists('submit24.sh'):
								shutil.copy('submit24.sh', os.path.join(pathway, tmp_file))								
						elif self.name == 'Tsinghua100':
							if os.path.exists('submit.sh'):
								shutil.copy('submit.sh', os.path.join(pathway, tmp_file))
						elif self.name == 'Tianhe' or self.name == 'Tianhe2':
							if os.path.exists('submitTH.sh'):
								shutil.copy('submitTH.sh', os.path.join(pathway, tmp_file))


	def generateJobFromGjf(self, fileName, path='', jobName='', method='', freq=True, command=''):
		QMmethod = 'B3LYP/6-31G(d)'

		gjfCommand_done = -1
		gjfMulti_done = -1
		geomDone = -1

		lineStart = 0
		lineEnd = 0

		if method != '':
			QMmethod = method

		if jobName == '':
			tmp_dir = fileName[0:-4] + '_1_opt_' + QMmethod[0:3]
		else:
			tmp_dir = jobName
		if path == '':			
			tmp_dir_path = tmp_dir
			fr = file(fileName, 'r')
		else:
			tmp_dir_path = os.path.join(path, tmp_dir)
			fr = file(os.path.join(path, fileName), 'r')

		if self.name == 'Tianhe' or self.name == 'Tianhe2':
			print 'sh submitTH.sh ' + tmp_dir + '''
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
			'''
		else:
			print 'sh submit12.sh ' + tmp_dir
			print 'sleep 5'

		tmp_lines = fr.readlines()
		for (lineNum, tmp_line) in  enumerate(tmp_lines):
			if gjfCommand_done != 1:
				tmp_m = pattern_gjfCommand.match(tmp_line)
				if tmp_m:
					gjfCommand_done = 1
			elif gjfMulti_done != 1:
				tmp_m = pattern_gjfMulti.match(tmp_line)
				if tmp_m:
					lineStart = lineNum
					multi = int(tmp_m.group(2))
					geomDone = 0
					gjfMulti_done = 1
			elif geomDone != 1:
				tmp_m = pattern_blankLine.match(tmp_line)
				if tmp_m:
					lineEnd = lineNum
					geomDone = 1

		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)					

		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
		if self.name == 'Tianhe' or self.name == 'Tianhe2':
			fw.write(
'''%mem=16GB
%nprocshared=12
''')
		else:
			fw.write(
'''%mem=28GB
%nprocshared=12
''')
# %chk=''')
		# if self.name == 'Tsinghua100' and self._scratchStrategy == True:
		# 	fw.write('/scratch/')
		# fw.write(tmp_dir+'.chk\n')
		if command == '':
			fw.write('#p ')
			if multi != 1:
				fw.write('u')
			fw.write(QMmethod)
			if self._TS == False:
				fw.write(' opt ')
				if freq == True:
					fw.write('freq')
			else:
				fw.write(' opt=(TS, calcfc) freq')
			if self._dispersionD3 == False:
				fw.write('\n')
			else:
				fw.write(' EmpiricalDispersion=GD3\n')
		else:
			fw.write(command+'\n')
		fw.write('''
using ''' + QMmethod + ''' to do opt and freq calc.

''')
		fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
		
		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
		if self.name == 'cce':
			if self._g09D01 == False:
				fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /share/apps
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf




''')
# $g09root/g09/formchk ''' + tmp_dir + '''.chk				
			else:
				fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /home/hetanjin/apps/g09D01
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')
# $g09root/g09/formchk ''' + tmp_dir + '''.chk
		elif self.name == 'Tsinghua100':
			fw.write(
# Tsinghua100 cluster
'''#BSUB -J ''' + tmp_dir + '''
#BSUB -q hpc_linux
#BSUB -R "select[mem>30000]"
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -o ''' + self.jobLocation + '/' + tmp_dir + '''/output.%J
#BSUB -e ''' + self.jobLocation + '/' + tmp_dir + '''/error.%J

export g09root=/home/hexin/gaussian
export GAUSS_SCRDIR=/scratch
source $g09root/g09/bsd/g09.profile

''')

			if self._scratchStrategy == True:
				fw.write(
'''rm /scratch/*
cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk /scratch/''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.chk ''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.fchk ''' + tmp_dir + '''.fchk
rm /scratch/*



''')
			else:
				fw.write(
'''cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
		elif self.name == 'Tianhe':
			if self._g09D01 == False:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you/g09/g09 ''' + tmp_dir + '''.gjf



''')
			else:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you/scratch
export g09root=/vol-th/home/you/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')
		elif self.name == 'Tianhe2':
			if self._g09D01 == False:
				fw.write(
# Tianhe cluster you1
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you1/g09/g09 ''' + tmp_dir + '''.gjf



''')
			else:
				fw.write(
# Tianhe cluster you1
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you1/scratch
export g09root=/vol-th/home/you1/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')				
		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

	def generateJobFromLog(self, fileName, path='', nosym=False, jobName=''):
		#variables
		multi = 1

		#flags
		multi_done = -1
		freqCom_done = -1
		standard_done = -1
		coordinate_done = -1

		# temporary variables
		tmp_m = []
		tmp_num = 0
				
		if jobName == '':
			tmp_dir = fileName[0:-4] + '_2_cbs'
		else:
			tmp_dir = jobName
		if path == '':			
			tmp_dir_path = tmp_dir
			fr = file(fileName, 'r')
		else:
			tmp_dir_path = os.path.join(path, tmp_dir)
			fr = file(os.path.join(path, fileName), 'r')

		tmp_lines = fr.readlines()		
		for (lineNum, tmp_line) in enumerate(tmp_lines):
			if multi_done != 1:
				tmp_m = pattern_logMulti.match(tmp_line)
				if tmp_m:
					multi = int(tmp_m.group(1))
					multi_done = 1
			elif freqCom_done != 1:
				if lineNum < len(tmp_lines) - 1:
					tmp2_line = tmp_lines[lineNum].strip() + tmp_lines[lineNum+1].strip()
					tmp_m = pattern_logFreqCom.match(tmp2_line)
					if tmp_m:
						freqCom_done = 1
			elif standard_done != 1:
				if nosym == False:
					tmp_m = pattern_logStandard.match(tmp_line)
				else:
					tmp_m = pattern_logInput.match(tmp_line)
				if tmp_m:
					tmp_num = lineNum + 5
					standard_done = 1
			elif coordinate_done != 1:
				tmp_m = pattern_logEndline.match(tmp_line)
				if tmp_m:
					if lineNum > tmp_num:
						tmp_geom = textExtractor.geometryExtractor(tmp_lines[tmp_num: lineNum])
						coordinate_done = 1

		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)					

		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
		if self.name == 'Tianhe' or self.name == 'Tianhe2':
			fw.write(
'''%mem=16GB
%nprocshared=12
%chk=''')
		else:
			fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
		if self.name == 'Tsinghua100' and self._scratchStrategy == True:
			fw.write('/scratch/')
		fw.write(tmp_dir+'.chk\n')
		if self._TS == False:
			fw.write('#p cbs-qb3')
		else:
			fw.write('#p cbs-qb3 opt=(TS, calcfc) freq')
		if self._dispersionD3 == False:
			fw.write('\n')
		else:
			print 'Warning! It should be verified whether D3 could be used in CBS-QB3 calculation!'
			fw.write(' EmpiricalDispersion=GD3\n')
		fw.write('''
using ub3lyp/6-31G(d) to scan

0 ''')
		fw.write(''.join([str(multi), '\n', tmp_geom]) + '\n\n\n\n\n')

		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
		
		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
		if self.name == 'cce':
			if self._g09D01 == False:
				fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /share/apps
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
			else:
				fw.write(
# cce cluster
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /home/hetanjin/apps/g09D01
source $g09root/g09/bsd/g09.login

cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
		elif self.name == 'Tsinghua100':
			fw.write(
# Tsinghua100 cluster
'''#BSUB -J ''' + tmp_dir + '''
#BSUB -q hpc_linux
#BSUB -R "select[mem>30000]"
#BSUB -n 12
#BSUB -R "span[hosts=1]"
#BSUB -o ''' + self.jobLocation + '/' + tmp_dir + '''/output.%J
#BSUB -e ''' + self.jobLocation + '/' + tmp_dir + '''/error.%J

export g09root=/home/hexin/gaussian
export GAUSS_SCRDIR=/scratch
source $g09root/g09/bsd/g09.profile

''')

			if self._scratchStrategy == True:
				fw.write(
'''rm /scratch/*
cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk /scratch/''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.chk ''' + tmp_dir + '''.chk
cp /scratch/''' + tmp_dir + '''.fchk ''' + tmp_dir + '''.fchk
rm /scratch/*



''')
			else:
				fw.write(
'''cd ''' + self.jobLocation + '/' + tmp_dir + '''
$g09root/g09/g09 ''' + tmp_dir + '''.gjf ''' + tmp_dir + '''.log
$g09root/g09/formchk ''' + tmp_dir + '''.chk



''')
		elif self.name == 'Tianhe':
			if self._g09D01 == False:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you/g09/g09 ''' + tmp_dir + '''.gjf



''')
			else:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you/scratch
export g09root=/vol-th/home/you/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')
		elif self.name == 'Tianhe2':
			if self._g09D01 == False:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

cd  ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 /vol-th/home/you1/g09/g09 ''' + tmp_dir + '''.gjf



''')
			else:
				fw.write(
# Tianhe cluster
'''#!/bin/bash

export GAUSS_SCRDIR=/vol-th/home/you1/scratch
export g09root=/vol-th/home/you1/softwares/gaussian/g09D01

source $g09root/g09/bsd/g09.profile

cd ''' + self.jobLocation + '/' + tmp_dir + '''
yhrun -pTH_NET -c12 $g09root/g09/g09 ''' + tmp_dir + '''.gjf



''')				
		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

	# this function is used to convert gjf to sdf format for conformer searching
	# the parameter path should be left as ''
	# the supporting for other directory is not important currently
	# if needed, only the path in jmol script should be adjusted according to the parameter path 
	# the parameter is used only when one gjf file is processed 
	def genFrogInputFromGjf(self, fileList, path='', jobName=''):
		for tmp_file in fileList:
			gjfCommand_done = -1
			gjfMulti_done = -1
			geomDone = -1

			lineStart = 0
			lineEnd = 0

			if re.search('[Tt][sS]', tmp_file):
				self.setTS(True)
			else:
				self.setTS(False)

			if jobName == '':
				tmp_dir = tmp_file[0:-4] + '_1_confSearch'
			else:
				tmp_dir = jobName
			if path == '':			
				tmp_dir_path = tmp_dir
				fr = file(tmp_file, 'r')
			else:
				tmp_dir_path = os.path.join(path, tmp_dir)
				fr = file(os.path.join(path, tmp_file), 'r')

			tmp_lines = fr.readlines()
			for (lineNum, tmp_line) in  enumerate(tmp_lines):
				if gjfCommand_done != 1:
					tmp_m = pattern_gjfCommand.match(tmp_line)
					if tmp_m:
						gjfCommand_done = 1
				elif gjfMulti_done != 1:
					tmp_m = pattern_gjfMulti.match(tmp_line)
					if tmp_m:
						lineStart = lineNum
						multi = int(tmp_m.group(2))
						geomDone = 0
						gjfMulti_done = 1
				elif geomDone != 1:
					tmp_m = pattern_blankLine.match(tmp_line)
					if tmp_m:
						lineEnd = lineNum
						geomDone = 1

			if os.path.exists(tmp_dir):
				shutil.rmtree(tmp_dir)
			os.mkdir(tmp_dir)					

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
			if self.name == 'Tianhe' or self.name == 'Tianhe2':
				fw.write(
'''%mem=16GB
%nprocshared=12
%chk=''')					
			else:
				fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
			if self.name == 'Tsinghua100' and self._scratchStrategy == True:
				fw.write('/scratch/')
			fw.write(tmp_dir+'.chk\n')
			if self._TS == False:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt freq')
			else:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt=(TS, calcfc) freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt=(TS, calcfc) freq')				
			if self._dispersionD3 == False:
				fw.write('\n')
			else:
				fw.write(' EmpiricalDispersion=GD3\n')
			fw.write('''
using ub3lyp/6-31G(d) to scan

''')
			fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.xyz'), 'w')
			fw.write(str(lineEnd - lineStart - 1) + '\n')
			fw.write(tmp_file[0:-4] + '\n')
			fw.write(''.join(tmp_lines[lineStart+1: lineEnd]) + '\n\n\n\n\n')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			os.system('E:\\hetanjin\\softwares\\OpenBabel-2.3.72\\babel.exe -ixyz ' + os.path.join(tmp_dir_path, tmp_dir+'.xyz') + ' -osdf ' + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')
			
			fr = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'r')
			tmp2_lines = fr.readlines()
			fr.close()
			tmp_num = map(int, tmp2_lines[3].split()[0:2])
			tmp_molecule = chem.molecule(geom=tmp_lines[lineStart+1: lineEnd])
			tmp_molecule.fulfillBonds()
			if tmp_num[1] < len(tmp_molecule.bonds):
				print 'Warning! Open babel transformation bug! Chem used to regenerate the bonds!', tmp_dir
				fw = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'w')
				tmp2_lines[3] = ''.join([' ', '%2d'%tmp_num[0], ' ', '%2d'%(len(tmp_molecule.bonds)), tmp2_lines[3][6:]])
				fw.writelines(tmp2_lines[0:3+tmp_num[0]+1]) 
				for tmp_bond in tmp_molecule.bonds:
					fw.write(''.join([' ', '%2d'%tmp_bond.atom1.label, ' ', '%2d'%tmp_bond.atom2.label, ' ', '%2d'%tmp_bond.bondOrder, '  0  0  0  0\n']))
				fw.write(
'''M  END
$$$$

''')
				fw.close()
			elif tmp_num[1] > len(tmp_molecule.bonds):
				print 'Error! Open babel bond number > len(tmp_molecule.bonds)', tmp_dir
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
			fw.write(
# cce cluster
'''#!/bin/sh

cd ''' + self.jobLocation + '/' + tmp_dir + '''
python /home/hetanjin/apps/Frog2/www_iMolecule.py -osmi ''' + tmp_dir + '''.smiles -logFile ''' + tmp_dir + '''.log -ounsolved Unsolved.data -wrkPath . -eini 100.0 -mcsteps 100 -emax 50 -i3Dsdf ''' + tmp_dir + '''.sdf -osdf out_''' + tmp_dir + '''.sdf -unambiguate -mini -multi 250 &>> log_''' + tmp_dir + '''.txt


''')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

		# generate the script to run jmol 
		# fw = file('gjfToJmol.jmol', 'w')
		# for tmp_file in fileList:
		# 	if jobName == '':
		# 		tmp_dir = tmp_file[0:-4] + '_1_confSearch'
		# 	else:
		# 		tmp_dir = jobName		
		# 	if path == '':			
		# 		tmp_dir_path = tmp_dir
		# 	else:
		# 		tmp_dir_path = os.path.join(path, tmp_dir)
		# 	fw.write('load "..\\\\_c_confSearch\\\\' + tmp_dir + '\\\\' + tmp_dir+'.gjf' + '"\n')
		# 	fw.write('write "..\\\\_c_confSearch\\\\' + tmp_dir + '\\\\' + tmp_dir+'.sdf' + '"\n')
		# fw.write('quit\n')
		# fw.close()
		# pay attention that the Jmol program should lie in the directory Template24  
		# os.chdir('../' + self.JmolPath)
		# os.system('jmol -nios ..\\_c_confSearch\\gjfToJmol.jmol -x')
		# os.chdir('../_c_confSearch')
		# for tmp_file in fileList:
		# 	if jobName == '':
		# 		tmp_dir = tmp_file[0:-4] + '_1_confSearch'
		# 	else:
		# 		tmp_dir = jobName		
		# 	if path == '':			
		# 		tmp_dir_path = tmp_dir
		# 	else:
		# 		tmp_dir_path = os.path.join(path, tmp_dir)
		# 	fr = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'r')
		# 	tmp_lines = fr.readlines()
		# 	tmp_lines[0] = tmp_file[0:-4] + '\n'
		# 	fr.close()
		# 	fw = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'w')
		# 	fw.writelines(tmp_lines)
		# 	fw.close()
		# 	os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')