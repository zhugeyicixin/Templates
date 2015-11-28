# READING--------------------------------------------------------------------------------------
# Read from specifically formatted excel sheet and store them as data arrays
from numpy import *
from xlrd import *
from re import *

# from xlrd import open_workbook,cellname
wb=open_workbook('2a_1st_oxidation.xls')
sh=wb.sheet_by_index(0)

# Define variables

total=int(sh.cell_value(1,0)) 		# Total number of reactions

# max_freq=75

# parameters of R 
name_R=[]						# name abbreviation
energy_R=[]						# enthalpy of formation at 0 K in kcal/mol
K_rotor_R=[]					# K-rotor of the rotational constants in GHZ
TwoD_rotor_R=[]					# 2D-rotor of the rotational constants in GHZ
freq_R=[]						# frequency array 
num_freq_R=[]					# Frequency counter
formula_R=[]					# chemical formula 

# parameters of TS
name_TS=[]						# name abbreviation
energy_TS=[]					# enthalpy of formation at 0 K in kcal/mol
reverse_barrier=[]				# reverse barrier energy
K_rotor_TS=[]					# K-rotor of the rotational constants in GHZ
TwoD_rotor_TS=[]				# 2D-rotor of the rotational constants in GHZ
i_freq_TS=[]					# imaginary frequency array
freq_TS=[]						# frequency array 
num_freq_TS=[]					# Frequency counter
formula_TS=[]					# chemical formula 

#temporary variables
tmp_freq=[]

# Read the information about TS
for row_index in range(3,3+total):
	if sh.cell_type(row_index,0) > 0.1:
		name_TS.append(sh.cell_value(row_index,1))

		# using barrier or formation energy?	
		energy_TS.append(sh.cell_value(row_index,7))
		
		reverse_barrier.append(sh.cell_value(row_index,8))
		formula_TS.append(sh.cell_value(row_index,10))
		K_rotor_TS.append(sh.cell_value(row_index,11))
		TwoD_rotor_TS.append(sh.cell_value(row_index,14))
		i_freq_TS.append(sh.cell_value(row_index,17))	
		num_freq_TS.append(int(sh.cell_value(row_index,18)))

		tmp_freq = []
		for col_num in range(num_freq_TS[-1]): 
			tmp_freq.append(sh.cell_value(row_index,20+col_num))
		freq_TS.append(tmp_freq)			
	else:
		continue

# Read the information about R
for row_index in range(3+(total+1),3+(total+1)+total):
	if sh.cell_type(row_index,0) > 0.1:
		name_R.append(sh.cell_value(row_index,1))

		#corresponding to the similar sentense above
		energy_R.append(sh.cell_value(row_index,7))

		formula_R.append(sh.cell_value(row_index,10))
		K_rotor_R.append(sh.cell_value(row_index,11))
		TwoD_rotor_R.append(sh.cell_value(row_index,14))
		num_freq_R.append(int(sh.cell_value(row_index,18)))

		tmp_freq = []
		for col_num in range(num_freq_R[-1]): 
			tmp_freq.append(sh.cell_value(row_index,20+col_num))
		freq_R.append(tmp_freq)			
	else:
		continue	
			

# WRITING --------------------------------------------------------------------------------------

total = len(name_TS)
for k in range(total):

	# Read from the existing template file
	
	# Open the new .dat file and append the remaining changes to the file
	#with open('thermo_{0}.dat'.format((bond_length[k])*100),'a') as h:
	h=open('thermo_' + name_TS[k]+'.dat','w')

	#write information about R
	h.write(
'''KCAL  MCC
9
400	450	500	550	600	650	700	750	800
2
reac  ''' + name_R[k] + "  " + str(energy_R[k]) + "\n" + \
formula_R[k] + '''
1. (blank comment line)
2. (blank comment line)
3. (blank comment line)
1   1   1
0.0   2
''' + str(num_freq_R[k]+2) + "\tHAR\tGHZ\n")

	for m in range(num_freq_R[k]):
		h.write(str(m+1) + "\tvib\t" + str(freq_R[k][m]) + "\t\t0\t1\n")
			
	#why not use kro but qro here
	h.write(str(m+2) + "\tqro\t" + str(K_rotor_R[k]) + "\t\t1\t1\t!	K-rotor\n")
	h.write(str(m+3) + "\tqro\t" + str(TwoD_rotor_R[k]) + "\t\t1\t2\t!	2D\n\n")

	#write information about TS
	h.write("ctst\t" + name_TS[k]  + "  " + str(energy_TS[k]) + "  " + str(i_freq_TS[k]) + "  " + str(reverse_barrier[k]) + '''\t!!!!!!!!!!!    <= TS
''' + formula_TS[k] + '''
1. (blank comment line)
2. (blank comment line)
3. (blank comment line)
1   1   1
0.0   2
''' + str(num_freq_TS[k]+2) + "\tHAR GHZ\n")

	for m in range(num_freq_TS[k]):
		h.write(str(m+1) + "\tvib\t" + str(freq_TS[k][m]) + "\t\t0\t1\n")
			
	#why not use kro but qro here
	h.write(str(m+2) + "\tqro\t" + str(K_rotor_TS[k]) + "\t\t1\t1\t!	K-rotor\n")
	h.write(str(m+3) + "\tqro\t" + str(TwoD_rotor_TS[k]) + "\t\t1\t2\t!	2D\n\n")		

# for loops of all reactions ended

print '\nEnded successfully!\n'		


# THE END


