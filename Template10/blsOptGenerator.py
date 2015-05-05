# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from xlwt import *
from xlutils.copy import copy
from re import *
import re
import os
import shutil

from geometryExtractor import *

#input
frozen_num1 = 14
frozen_num2 = 15
name = 'RO2_beta_20_opt_b3D3cbsb7'

#definition of parameters
multi = 0

# symbol indicating the position
pattern_name = re.compile('^.*_scan.*$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$')
# pattern_standard = re.compile('^.*Standard orientation:.*$')
pattern_standard = re.compile('^.*Input orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_distance = re.compile('^.*R\(' + str(frozen_num1) + ',' + str(frozen_num2) + '\).*(-?[0-9]+\.[0-9]+).*-DE/DX.*$')

#variables
distance=[]
geom=[]

#flags
multi_done = 0
optimized_done = 0
standard_done = 0
skip_line = 0
coordinate_done = 0
distance_done = 0
geom_start = 0
geom_end = 0

# temporary variables
tmp_m = []

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	multi_done = 0
	optimized_done = 0
	standard_done = 0
	skip_line = 0
	coordinate_done = 0
	distance_done = 0
	geom_start = 0
	geom_end = 0

	distance = []
	geom = []

	if re.search('.log',tmp_file):
		tmp_m = pattern_name.match(tmp_file[0:-4])
		if tmp_m:
			print tmp_file
			fr = file(tmp_file,'r')
			lines = fr.readlines()
			for i in range(0,len(lines)):
				tmp_line = lines[i]
				if multi_done != 1:
					tmp_m = pattern_multi.match(tmp_line)
					if tmp_m:
						multi = tmp_m.group(1)
						multi_done = 1
				elif standard_done != 1 or coordinate_done != 1 or optimized_done != 1:
					tmp_m = pattern_standard.match(tmp_line)
					if tmp_m:
						geom_start = i + 5
						standard_done = 1
					tmp_m = pattern_endline.match(tmp_line)
					if tmp_m:
						if i>geom_start:
							geom_end = i
							coordinate_done = 1	
					tmp_m = pattern_optimized.match(tmp_line)
					if tmp_m:
						distance_done = 0
						optimized_done = 1
				elif distance_done != 1:
					tmp_m = pattern_distance.match(tmp_line)
					if tmp_m:
						distance.append(float(tmp_m.group(1)))
						geom.append(geometryExtractor(lines[geom_start:geom_end]))
						standard_done = 0
						coordinate_done = 0
						optimized_done = 0
						distance_done = 1

			for i in distance:
				tmp_R = str(int(round(i*100)))
				if os.path.exists(os.getcwd() + '/' + name + '_' + tmp_R):
					shutil.rmtree(name + '_' + tmp_R)
				os.mkdir(name + '_' + tmp_R)
				fw = file(name + '_' + tmp_R + '/' + name + '_' + tmp_R + '.gjf','w')
				fw.write(
# gaussian input template
'''%mem=28GB
%nprocshared=12
%chk=''' + name + '_' + tmp_R + '''.chk
#p ub3lyp/cbsb7 opt=modredundant freq scf=xqc EmpiricalDispersion=GD3

''' + name + ''' using cbs-qb3 to calculate energy

0 ''' + multi + '\n' + geom.pop(0) + '\nB ' + str(frozen_num1) + ' ' + str(frozen_num2) + ' F\n\n\n\n\n\n\n') 

# molpro input template	
# '''***,C3H7O2
# memory,300,M
# print,basis,orbitals
# gthresh,energy=1.0d-10,orbital=1.0d-10
# angstrom
# geometry={
# ''' + geom.pop(0) + '''              
# }
# basis=vdz
# {uhf
# }
# {casscf
# closed,17
# occ,22
# wf,41,1,1
# print,civector
# }
# rs2
# {optg
# method,slrf
# constraint,''' + ('%.2f' %i) + ''',ang,bond,atoms=[''' + str(frozen_num1) + ',' + str(frozen_num2) + ''']               
# }

# ---



# ''')

				fw.close()
				os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

				fw = file(name + '_' + tmp_R + '/' + name + '_' + tmp_R + '.job','w')
				fw.write(
# gaussian input template
# '''#BSUB -J ''' + name + '_' + tmp_R + '''
# #BSUB -q hpc_linux
# #BSUB -R "select[mem>42000]"
# #BSUB -n 12
# #BSUB -R "span[hosts=1]"
# #BSUB -o /work2/hexin_work/barrierless/C3H7O2/''' + name + '_' + tmp_R + '''/output.%J
# #BSUB -e /work2/hexin_work/barrierless/C3H7O2/''' + name + '_' + tmp_R + '''/error.%J

# cd /work2/hexin_work/barrierless/C3H7O2/''' + name + '_' + tmp_R + '''
# g09 ''' + name + '_' + tmp_R + '''.gjf ''' + name + '_' + tmp_R + '''.log
# formchk ''' + name + '_' + tmp_R + '''.chk



# ''')
# G09 A.01
# '''#!/bin/csh
# #
# #$ -cwd
# #$ -j y
# #$ -S /bin/csh
# #
# setenv GAUSS_SCRDIR /state/partition1
# setenv g09root /share/apps
# source $g09root/g09/bsd/g09.login

# cd /home/hetanjin/isobutanol/barrierless/RO2_beta/''' +  name + '_' + tmp_R + '''
# /share/apps/g09/g09 ''' +  name + '_' + tmp_R + '''.gjf
# /share/apps/g09/formchk ''' +  name + '_' + tmp_R + '''.chk




# ''')
# G09 D.01
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /home/hetanjin/apps/g09D01
source $g09root/g09/bsd/g09.login

cd /home/hetanjin/isobutanol/barrierless/RO2_beta/''' +  name + '_' + tmp_R + '''
$g09root/g09/g09 ''' +  name + '_' + tmp_R + '''.gjf
$g09root/g09/formchk ''' +  name + '_' + tmp_R + '''.chk




''')

# molpro input template
# '''#!/bin/csh
# #
# #$ -cwd
# #$ -j y
# #$ -S /bin/csh
# #

# cd /home/hetanjin/molpro/BDE/''' + name + '_' + tmp_R + '''
# /share/apps/molpro/molprop_2012_1_Linux_x86_64_i8/bin/molpro -d /state/partition1 -W /state/partition1/wfu -n 12 ''' + name + '_' + tmp_R + '''.gjf



# ''')


				fw.close()
				os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

print 'input scripts generated successfully!'

# THE END


