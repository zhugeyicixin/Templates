# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import shutil
import textExtractor

# definetion of comparing pattern
pattern_multi = re.compile('^.*spinMultiplicity: *([0-9]+).*$')
pattern_atom = re.compile('^.*[A-Z] *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
pattern_rotation = re.compile('^ *([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+).*$')

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

	_g09D01 = False
	_dispersionD3 = False
	_scratchStrategy = True
	_TS = False

	def __init__(self, name, clusterPath):
		self.name = name
		self.jobLocation = clusterPath

		self._g09D01 = False
		self._dispersionD3 = False
		self._scratchStrategy = True
		self._TS = False

	def setJobLocation(self, clusterPath):
		self.jobLocation = clusterPath

	def setG09D01(self, useG09D01):
		self._g09D01 = useG09D01

	def setDispersionD3(self, useDispersionD3):
		self._dispersionD3 = useDispersionD3

	def setScratchStractegy(self, useScratchStrategy):
		self._scratchStrategy = useScratchStrategy		

	def setTS(self, isTS):
		self._TS = isTS		

	def generateRotScanJobs(self, pathway=''):
		# variables
		rotations = []

		# flags
		multi_done = -1
		atom_begin = -1
		atom_done = -1
		rotation_done = -1

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

						rotations = []

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
							fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
							if self.name == 'Tsinghua100' and self._scratchStrategy == True:
								fw.write('/scratch/')
							if self._dispersionD3 == False:
								fw.write(tmp_dir + '.chk\n')
							if self._TS == False:
								fw.write('#p ub3lyp/6-31g(d) opt=modredundant nosym')
							else:
								fw.write('#p ub3lyp/6-31g(d) opt=(TS, calcfc,modredundant,noeigentest) nosym')
							if self._dispersionD3 == False:
								fw.write('\n')
							else:
								fw.write(' EmpiricalDispersion=GD3\n')
							fw.write(
'''
using ub3lyp/6-31G(d) to scan

0 ''')
							fw.write(''.join([str(multi), '\n'] + tmp_lines[atom_begin: atom_done] + ['\n', \
								'D ', tmp_rotation[0], ' ', tmp_rotation[1], ' ', tmp_rotation[2], ' ', tmp_rotation[3], ' ', 'S 40 10.0\n\n\n\n\n\n']))
							fw.close()
							os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)
							
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
							fw.close()
							os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)
						if self.name == 'cce':
							if os.path.exists('submit12.sh'):
								shutil.copy('submit12.sh', os.path.join(pathway, tmp_file))
							if os.path.exists('submit24.sh'):
								shutil.copy('submit24.sh', os.path.join(pathway, tmp_file))								
						elif self.name == 'Tsinghua100':
							if os.path.exists('submit.sh'):
								shutil.copy('submit.sh', os.path.join(pathway, tmp_file))

	def generateJobFromGjf(self, fileName, path='', jobName=''):
		gjfCommand_done = -1
		gjfMulti_done = -1
		geomDone = -1

		lineStart = 0
		lineEnd = 0

		if jobName == '':
			tmp_dir = fileName[0:-4] + '_1_opt_631gd'
		else:
			tmp_dir = jobName
		if path == '':			
			tmp_dir_path = tmp_dir
			fr = file(fileName, 'r')
		else:
			tmp_dir_path = os.path.join(path, tmp_dir)
			fr = file(os.path.join(path, fileName), 'r')

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
		fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
		if self.name == 'Tsinghua100' and self._scratchStrategy == True:
			fw.write('/scratch/')
		fw.write(tmp_dir+'.chk\n')
		if self._TS == False:
			fw.write('#p ub3lyp/cbsb7 opt freq')
		else:
			fw.write('#p ub3lyp/cbsb7 opt=(TS, calcfc) freq')
		if self._dispersionD3 == False:
			fw.write('\n')
		else:
			fw.write(' EmpiricalDispersion=GD3\n')
		fw.write('''
using ub3lyp/6-31G(d) to scan

''')
		fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

		fw.close()
		os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)
		
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
source $g09root/g09/bsd/g09.profile''')

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
$g09root/g09/formchk /scratch/''' + tmp_dir + '''.chk



''')
		fw.close()
		os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

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
		fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''')
		if self.name == 'Tsinghua100' and self._scratchStrategy == True:
			fw.write('/scratch/')
		if self._dispersionD3 == False:
			fw.write(tmp_dir + '''.chk
#p cbs-qb3

using ub3lyp/6-31G(d) to scan

0 ''')
			fw.write(''.join([str(multi), '\n', tmp_geom]) + '\n\n\n\n\n')
		else:
			fw.write(tmp_dir + '''.chk
#p cbs-qb3 EmpiricalDispersion=GD3

using ub3lyp/6-31G(d) to scan

''')
			fw.write(''.join([str(multi), '\n', tmp_geom]) + '\n\n\n\n\n')

		fw.close()
		os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)
		
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
source $g09root/g09/bsd/g09.profile''')

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
$g09root/g09/formchk /scratch/''' + tmp_dir + '''.chk



''')
		fw.close()
		os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)







