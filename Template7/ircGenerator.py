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

#definition of parameters
mutil = 0

# symbol indicating the position
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$')
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_ts = re.compile('^.*[tT][sS].*$')

#flags
multi_done = 0
optimized_done = 0
Standard_done = 0
skip_line = 0
coordinate_done = 0

# temporary variables
tmp_m = []

pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	multi_done = 0
	optimized_done = 0
	Standard_done = 0
	skip_line = 0
	coordinate_done = 0

	if re.search('.log',tmp_file):
		tmp_m = pattern_ts.match(tmp_file[0:-4])
		if tmp_m:
			os.mkdir(tmp_file[0:-4] +'_4_irc')
			fr = file(tmp_file,'r')
			fw = file(tmp_file[0:-4] +'_4_irc/' + tmp_file[0:-4] +'.gjf','w')
			fw.write(
			'''%mem=30GB
%nprocshared=8
%chk=''' + tmp_file[0:-4] + '''.chk
#p ub3lyp/cbsb7 irc=calcfc

''' + tmp_file[0:-4] + ''' using b3lyp/cbsb7 to calculate irc

0 ''')
			for tmp_line in fr.readlines():
				if multi_done != 1:
					tmp_m = pattern_multi.match(tmp_line)
					if tmp_m:
						fw.write(tmp_m.group(1)+'\n')
						multi_done = 1
				elif optimized_done != 1:
					tmp_m = pattern_optimized.match(tmp_line)
					if tmp_m:
						optimized_done = 1
				elif Standard_done != 1:
					tmp_m = pattern_standard.match(tmp_line)
					if tmp_m:
						Standard_done = 1
				elif skip_line != 4:
					skip_line += 1
					continue
				elif coordinate_done != 1:
					tmp_m = pattern_endline.match(tmp_line)
					if tmp_m:
						fw.write('\n\n\n\n\n')
						coordinate_done = 1
						break
					else:
						tmp_line.rstrip()
						tmp_line = tmp_line.split()
						fw.write(tmp_line[1] + '\t' + tmp_line[3] + '\t' + tmp_line[4] + '\t' + tmp_line[5]+'\n')

			fr.close()
			fw.close()
			fw = file(tmp_file[0:-4] +'_4_irc/' + tmp_file[0:-4] +'.pbs','w')
			fw.write(
'''#PBS -N ''' + tmp_file[0:-4] +'''
#PBS -A avioli_flux
#PBS -l qos=flux
#PBS -l nodes=1:ppn=8,mem=30gb,walltime=36:00:00
#PBS -q flux
#PBS -V
#PBS -o /home/hetanjin/farnesane/dimethylheptane/opt_akbar/3_non_barrierless_freq/3-ts9/''' + tmp_file[0:-4] +'''_4_irc
#PBS -e /home/hetanjin/farnesane/dimethylheptane/opt_akbar/3_non_barrierless_freq/3-ts9/''' + tmp_file[0:-4] +'''_4_irc
#
echo "I ran on:"
cat $PBS_NODEFILE
#
mkdir -p /scratch/avioli_flux/hetanjin/scratch/

cd /home/hetanjin/farnesane/dimethylheptane/opt_akbar/3_non_barrierless_freq/3-ts9/''' + tmp_file[0:-4] +'''_4_irc

#
#
export GAUSS_SCRDIR=/scratch/avioli_flux/hetanjin/scratch/
g09 <''' + tmp_file[0:-4] + '''.gjf > ''' + tmp_file[0:-4] +'''.log
formchk ''' + tmp_file[0:-4] +'''.chk


''')

print 'irc scripts generated successfully!'

# THE END


