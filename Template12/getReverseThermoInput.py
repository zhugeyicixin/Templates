# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from xlrd import *
import os
import re
import shutil

__barrier__ = True

# from xlrd import open_workbook,cellname
name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[1].strip(' \n')
		if tmp_line == 'barrier':
			__barrier__ = True
			print '\n-------------------------------------\nbarrier reactions\n-------------------------------------\n'
		elif tmp_line == 'barrierless':
			__barrier__ = False
			print '\n-------------------------------------\nbarrierless reaction\n-------------------------------------\n'
		else:
			print '\n-------------------------------------\nWarning! Barrier or barrierless is not announced! Barrier is used as default!\n-------------------------------------\n'
		tmp_line = tmp_lines[5].strip(' \n')
		temperature = map(float, tmp_line.split())			
		fr.close()	

wb=open_workbook(name + '.xls')
sh=wb.sheet_by_name('SpeciesInfo')

# Define variables

total=int(sh.cell_value(1,0)) 		# Total number of activated reactions
reacs_line = 0  					# Total number of reactants line in excel, not equal to those in activated reactions, would changed while reading, it's used to count lines
prods_line = 0 						# Total number of products line in excel, not equal to those in activated reactions, would changed while reading, it's used to count lines
# max_freq=75

# parameters of R 
name_R=[]						# name abbreviation
energy_R=[]						# enthalpy of formation at 0 K in kcal/mol
K_rotor_R=[]					# K-rotor of the rotational constants in GHZ
TwoD_rotor_R=[]					# 2D-rotor of the rotational constants in GHZ
RSN_R = []						# rotational symmetry number of R
multi_R = []					# multiplicity of R in ground sate
freq_R=[]						# frequency array 
num_freq_R=[]					# Frequency counter
formula_R=[]					# chemical formula 

# parameters of TS
name_TS=[]						# name abbreviation
energy_TS=[]					# enthalpy of formation at 0 K in kcal/mol
reverse_barrier=[]				# reverse barrier energy
K_rotor_TS=[]					# K-rotor of the rotational constants in GHZ
TwoD_rotor_TS=[]				# 2D-rotor of the rotational constants in GHZ
RSN_TS = []						# rotational symmetry number of TS
multi_TS = []					# multiplicity of TS in ground sate
i_freq_TS=[]					# imaginary frequency array
freq_TS=[]						# frequency array 
num_freq_TS=[]					# Frequency counter
formula_TS=[]					# chemical formula 

#temporary variables
tmp_name = []
tmp_energy = []
tmp_reverse_barrier = []
tmp_formula = []
tmp_K_rotor = []
tmp_TwoD_rotor = []
tmp_RSN = []
tmp_multi = []
tmp_num_freq = []
tmp_i_freq = []
tmp_freq=[]
tmp_row = 3

num_rows = sh.nrows
num_cols = sh.ncols
num_reac = 1
num_TS = 1
num_prod = 1




while sh.cell_value(tmp_row,0) != '':
	tmp_row += 1

tmp_row += 1
while sh.cell_value(tmp_row,0) != '':
	if int(sh.cell_value(tmp_row,0)) != 0:
		tmp_name = []
		tmp_energy = []
		tmp_formula = []
		tmp_K_rotor = []
		tmp_TwoD_rotor = []
		tmp_RSN = []
		tmp_multi = []
		tmp_num_freq = []
		tmp_freq=[]

		num_reac = int(int(sh.cell_value(tmp_row,0))/10);
		num_prod = int(sh.cell_value(tmp_row,0))%10;

		for i in range(num_prod):
			tmp_name.append(sh.cell_value(tmp_row,1))
			tmp_energy.append(float(sh.cell_value(tmp_row,8)))
			tmp_formula.append(sh.cell_value(tmp_row,10))
			tmp_K_rotor.append(float(sh.cell_value(tmp_row,11)))
			tmp_TwoD_rotor.append(float(sh.cell_value(tmp_row,14)))
			tmp_RSN.append(int(sh.cell_value(tmp_row,15)))
			tmp_multi.append(int(sh.cell_value(tmp_row,16)))
			tmp_num_freq.append(int(sh.cell_value(tmp_row,19)))
			tmp2_freq = []
			for col_num in range(tmp_num_freq[-1]): 
				tmp2_freq.append(float(sh.cell_value(tmp_row,21+col_num)))
			tmp_freq.append(tmp2_freq)
			tmp_row += 1

		name_R.append(tmp_name)
		energy_R.append(tmp_energy)
		formula_R.append(tmp_formula)
		K_rotor_R.append(tmp_K_rotor)
		TwoD_rotor_R.append(tmp_TwoD_rotor)
		RSN_R.append(tmp_RSN)
		multi_R.append(tmp_multi)
		num_freq_R.append(tmp_num_freq)
		freq_R.append(tmp_freq)

	else:
		tmp_row += 1

tmp_row += 1
while sh.cell_value(tmp_row,0) != '':
	if int(sh.cell_value(tmp_row,0)) != 0:
		tmp_name = []
		tmp_energy = []
		tmp_reverse_barrier = []
		tmp_formula = []
		tmp_K_rotor = []
		tmp_TwoD_rotor = []
		tmp_RSN = []
		tmp_multi = []
		tmp_num_freq = []
		tmp_freq=[]
		tmp_i_freq = []

		for i in range(num_TS):
			tmp_name.append(sh.cell_value(tmp_row,1))
			tmp_energy.append(float(sh.cell_value(tmp_row,8)))
			tmp_reverse_barrier.append(float(sh.cell_value(tmp_row,7)))
			tmp_formula.append(sh.cell_value(tmp_row,10))
			tmp_K_rotor.append(float(sh.cell_value(tmp_row,11)))
			tmp_TwoD_rotor.append(float(sh.cell_value(tmp_row,14)))
			tmp_RSN.append(int(sh.cell_value(tmp_row,15)))
			tmp_multi.append(int(sh.cell_value(tmp_row,16)))
			tmp_i_freq.append(float(sh.cell_value(tmp_row,18)))
			if not tmp_i_freq[-1] > 0:
				print 'Error! There is some problem with the imaginary frequency of ' + tmp_name[-1]	
			tmp_num_freq.append(int(sh.cell_value(tmp_row,19)))

			tmp2_freq = []
			for col_num in range(tmp_num_freq[-1]): 
				tmp2_freq.append(float(sh.cell_value(tmp_row,21+col_num)))
			tmp_freq.append(tmp2_freq)
			tmp_row += 1

		name_TS.append(tmp_name)
		energy_TS.append(tmp_energy)
		reverse_barrier.append(tmp_reverse_barrier)
		formula_TS.append(tmp_formula)
		K_rotor_TS.append(tmp_K_rotor)
		TwoD_rotor_TS.append(tmp_TwoD_rotor)
		RSN_TS.append(tmp_RSN)
		multi_TS.append(tmp_multi)
		i_freq_TS.append(tmp_i_freq)
		num_freq_TS.append(tmp_num_freq)
		freq_TS.append(tmp_freq)	
	else:
		tmp_row += 1
	if tmp_row >= sh.nrows:
		break

print 'get reverse reactions successfully!'


# WRITING --------------------------------------------------------------------------------------

total = len(name_TS)
if os.path.exists(os.getcwd()+'/thermoReverseInput'):
	shutil.rmtree(os.getcwd()+'/thermoReverseInput')
os.mkdir('thermoReverseInput')

for k in range(total):
	fw = file('thermoReverseInput/' + name_TS[k][0] +'.dat','w')
	#write information about R
	fw.write('KCAL  MCC\n' + str(len(temperature)) + '\n' + ''.join(str(x) + ' ' for x in temperature) + '\n' + str(len(name_R[k])+len(name_TS[k])))

	for i in range(len(name_R[k])):
		fw.write('''
reac  ''' + name_R[k][i] + "  " + str(energy_R[k][i]) + "\n" + \
formula_R[k][i] + '''
1. (blank comment line)
2. (blank comment line)
3. (blank comment line)
''' + str(RSN_R[k][i]) +'''   1   1
0.0   ''' + str(multi_R[k][i]) + '\n')

		if abs(K_rotor_R[k][i]) > 0.001:
			fw.write(str(num_freq_R[k][i] + 2) + "\tHAR\tGHZ\n")
		else:
			fw.write(str(num_freq_R[k][i] + 1) + "\tHAR\tGHZ\n")

		for m in range(num_freq_R[k][i]):
			fw.write(str(m+1) + "\tvib\t" + str(freq_R[k][i][m]) + "\t\t0\t1\n")
				
		#why not use kro but qro here
		if abs(K_rotor_R[k][i]) > 0.001:
			fw.write(str(m+2) + "\tqro\t" + str(K_rotor_R[k][i]) + "\t\t1\t1\t!	K-rotor\n")
			fw.write(str(m+3) + "\tqro\t" + str(TwoD_rotor_R[k][i]) + "\t\t1\t2\t!	2D\n\n")
		else:
			fw.write(str(m+2) + "\tqro\t" + str(TwoD_rotor_R[k][i]) + "\t\t1\t2\t!	2D\n\n")

	#write information about TS
	if __barrier__ == True:
		fw.write("ctst\t" + name_TS[k][0]  + "\t" + str(energy_TS[k][0]) + "  " + str(i_freq_TS[k][0]) + "  " + str(reverse_barrier[k][0]) + '''\t!!!!!!!!!!!    <= TS
''' + formula_TS[k][0] + '''
1. (blank comment line)
2. (blank comment line)
3. (blank comment line)
''' + str(RSN_TS[k][0]) + '''   1   1
0.0   ''' + str(multi_TS[k][0]) + '\n' + str(num_freq_TS[k][0] + 2) + "\tHAR GHZ\n")
	else:
		fw.write("ctst\t" + name_TS[k][0]  + "\t" + str(energy_TS[k][0]) + "  0.0" + "  0.0" + '''\t!!!!!!!!!!!    <= loose TS
''' + formula_TS[k][0] + '''
1. (blank comment line)
2. (blank comment line)
3. (blank comment line)
''' + str(RSN_TS[k][0]) + '''   1   1
0.0   ''' + str(multi_TS[k][0]) + '\n' + str(num_freq_TS[k][0] + 2) + "\tHAR GHZ\n")

	for m in range(num_freq_TS[k][0]):
		fw.write(str(m+1) + "\tvib\t" + str(freq_TS[k][0][m]) + "\t\t0\t1\n")
			
	#why not use kro but qro here
	fw.write(str(m+2) + "\tqro\t" + str(K_rotor_TS[k][0]) + "\t\t1\t1\t!	K-rotor\n")
	fw.write(str(m+3) + "\tqro\t" + str(TwoD_rotor_TS[k][0]) + "\t\t1\t2\t!	2D\n\n")		
	fw.close()
# for loops of all reactions ended

print '\nThermo reverse input generated successfully!\n'		

# THE END


