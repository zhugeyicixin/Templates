# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os

# definetion of comparing pattern
pattern_multi = re.compile('^.*spinMultiplicity: *([0-9]+).*$')
pattern_atom = re.compile('^.*[A-Z] *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
pattern_rotation = re.compile('^ *([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+).*$')
pattern_freqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')

class cluster:
	name = ''
	jobLocation = ''

	_g09D01 = False
	_dispersionD3 = False
	_scratchStrategy = True


	def __init__(self, name, clusterPath):
		self.name = name
		self.jobLocation = clusterPath

	def setJobLocation(self, clusterPath):
		self.jobLocation = clusterPath

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
								fw.write(tmp_dir + '''.chk
#p ub3lyp/6-31g(d) opt=modredundant nosym

using ub3lyp/6-31G(d) to scan

0 ''')
							else:
								fw.write(tmp_dir + '''.chk
#p ub3lyp/6-31g(d) opt=modredundant nosym EmpiricalDispersion=GD3

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






