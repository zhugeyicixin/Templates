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
frozen_num1 = 22
frozen_num2 = 29
name = 'RO2_1_5_opt_ub3cbsb7'

#definition of parameters
multi = 0

# symbol indicating the position
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$')
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_ts = re.compile('^.*RO2.*$')

#variables
geom=[]

#flags
multi_done = 0
optimized_done = 0
standard_done = 0
skip_line = 0
coordinate_done = 0
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
	geom_start = 0
	geom_end = 0

	geom = []

	if re.search('.log',tmp_file):
		tmp_m = pattern_ts.match(tmp_file[0:-4])
		if tmp_m:
			if os.path.exists(pwd + '/' + name + '_' + tmp_file[-7:-4]):
				shutil.rmtree(name + '_' + tmp_file[-7:-4])
			os.mkdir(name + '_' + tmp_file[-7:-4])
			fr = file(tmp_file,'r')
			lines = fr.readlines()
			for i in range(0,len(lines)):
				tmp_line = lines[i]
				if multi_done != 1:
					tmp_m = pattern_multi.match(tmp_line)
					if tmp_m:
						multi = tmp_m.group(1)
						# fw.write(multi + '\n')
						multi_done = 1
				elif optimized_done != 1:
					tmp_m = pattern_optimized.match(tmp_line)
					if tmp_m:
						optimized_done = 1
				elif standard_done != 1:
					tmp_m = pattern_standard.match(tmp_line)
					if tmp_m:
						geom_start = i + 5
						standard_done = 1
				elif coordinate_done != 1:
					tmp_m = pattern_endline.match(tmp_line)
					if tmp_m:
						if i > geom_start:
							geom_end = i
							geom.append(geometryExtractor(lines[geom_start:geom_end]))
							coordinate_done = 1
			fr.close()
			
			fw = file(name + '_' + tmp_file[-7:-4] + '/' + name + '_' + tmp_file[-7:-4] + '.gjf','w')
			fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''' + name + '_' + tmp_file[-7:-4] + '''.chk
#p ub3lyp/cbsb7 opt=modredundant freq

''' + tmp_file[0:-4] +'''_13_mp2_vqz using cbs-qb3 to calculate energy

0 ''' + multi + '\n' + geom.pop(0)+'\nB ' + str(frozen_num1) + ' ' + str(frozen_num2) + ' F\n\n\n\n\n')	
			
			fw.close()
			os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

			fw = file(name + '_' + tmp_file[-7:-4] + '/' + name + '_' + tmp_file[-7:-4] + '.job','w')
			fw.write(
'''#!/bin/csh
#
#$ -cwd
#$ -j y
#$ -S /bin/csh
#
setenv GAUSS_SCRDIR /state/partition1
setenv g09root /share/apps
source $g09root/g09/bsd/g09.login

cd /home/hetanjin/DMH/barrierlessScale/C9H19O2_1_26/''' + name + '_' + tmp_file[-7:-4] + '''
/share/apps/g09/g09 ''' + name + '_' + tmp_file[-7:-4] + '''.gjf
/share/apps/g09/formchk ''' + name + '_' + tmp_file[-7:-4] + '''.chk


''')
# '''#BSUB -J ''' + tmp_file[0:-4] +'''_13_mp2_vqz
# #BSUB -q hpc_linux
# #BSUB -R "select[mem>30000]"
# #BSUB -n 12
# #BSUB -R "span[hosts=1]"
# #BSUB -o /work/hexin_work/isobutonal/barrierless/C2H4RO2/RO2_continued/''' + tmp_file[0:-4] +'''_13_mp2_vqz/output.%J
# #BSUB -e /work/hexin_work/isobutonal/barrierless/C2H4RO2/RO2_continued/''' + tmp_file[0:-4] +'''_13_mp2_vqz/error.%J

# cd /work/hexin_work/isobutonal/barrierless/C2H4RO2/RO2_continued/''' + name + '_' + tmp_file[-7:-4] + '''
# g09 ''' + tmp_file[0:-4] +'''_13_mp2_vqz.gjf ''' + tmp_file[0:-4] +'''_13_mp2_vqz.log
# formchk /scratch/''' + tmp_file[0:-4] +'''_13_mp2_vqz.chk
# cp /scratch/''' + tmp_file[0:-4] +'''_13_mp2_vqz.chk ''' + tmp_file[0:-4] +'''_13_mp2_vqz.chk
# cp /scratch/''' + tmp_file[0:-4] +'''_13_mp2_vqz.fchk ''' + tmp_file[0:-4] +'''_13_mp2_vqz.fchk
# rm /scratch/''' + tmp_file[0:-4] +'''_13_mp2_vqz.chk
# rm /scratch/''' + tmp_file[0:-4] +'''_13_mp2_vqz.fchk



# ''')

			fw.close()
			os.system("D:\\hetanjin\\smallSoftware\\dos2unix-6.0.6-win64\\bin\dos2unix.exe " + fw.name)

print 'cbs-qb3 scripts generated successfully!'

# THE END


