import shutil
import os

# input parameters
factor = 2
# unit : K
temperature = 650
# unit : atm
pressure = 10
phi = 1

xmlFile = 'reactions_myb1st2nd_gold2nd_3rdooqooh_test3.xml'
workName = 'Factor_' + str(temperature) + 'K_%0.1f'%factor
workPath = '/home/hetanjin/Cantera/' + workName

reactionNum = 6423
increment = 10
fileNuminDir = 20


# temporary variables
dirNum = 0
fileNum = 0
dirName = ''
fileName = ''

reactionSplit=range(1, reactionNum+2, increment)
if reactionSplit[-1] != reactionNum+1:
	reactionSplit.append(reactionNum+1)
# print reactionSplit

if os.path.exists(workName):
	shutil.rmtree(workName)
os.mkdir(workName)
if fileNuminDir > 12:
	shutil.copy('submit24.sh', workName)
else:
	shutil.copy('submit12.sh', workName)

for i in xrange(0, len(reactionSplit)-1):
	if (fileNum%fileNuminDir) == 0:
		dirNum += 1
		dirName = 'Factor' + '%0.1f'%factor + '_' + '%03d'%(dirNum)
		if os.path.exists(os.path.join(workName, dirName)):
			shutil.rmtree(os.path.join(workName, dirName))
		os.mkdir(os.path.join(workName, dirName))
		fw = file(os.path.join(workName, dirName, dirName + '.job'), 'w')
		fw.write(
'''#!/bin/sh

source /home/hetanjin/apps/cantera-2.2.0/cantera/bin/setup_cantera

cd ''' + workPath + '/' + dirName + '''
echo '---------------Start!----------------- ' >> log.txt
date >> log.txt
echo '   ' >> log.txt
python --version &>> log.txt
echo '   ' >> log.txt
for entry in `ls *.py`
do
	echo $entry >> log.txt
	tmp_var=log_${entry%.py}
	echo '   ' >> ${tmp_var}.txt
	echo "${entry}" >> ${tmp_var}.txt
	echo begin >> ${tmp_var}.txt
	date >> ${tmp_var}.txt
	echo '   ' >> ${tmp_var}.txt
	python ${entry} &>> ${tmp_var}.txt &
done

jobs -l >> log.txt
wait
echo '   ' >> log.txt
echo '----------------End!------------------ ' >> log.txt
date >> log.txt
echo allJobsFinished >> log.txt



''')
		fw.close()
		os.system("E:\\hetanjin\\GithubFiles\\Templates\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
		shutil.copy(xmlFile, os.path.join(workName, dirName))

	fileNum += 1
	fileName = 'DMH_X' + '%0.1f'%factor + '_' + '%04d'%fileNum + '.py'
	reactionListStart = reactionSplit[i]
	reactionListEnd = reactionSplit[i+1]
	fw = file(os.path.join(workName, dirName, fileName), 'w')
	fw.write(
'''"""
Constant-pressure, adiabatic kinetics simulation.
"""

import sys
import os
import csv
import numpy as np
import cantera as ct
import matplotlib.pyplot as plt

# os.system('cheminp2xml.bat')
plot_bool = 0
bool_diagram = 0
f0= open('DMH_''' + str(temperature) + 'K_' + str(pressure) + 'atm_phi' + str(phi) + '_' + '%04d'%fileNum + '''.csv','w')
csvfile_ign = csv.writer(f0, delimiter=',', lineterminator='\\n')
csvfile_ign.writerow(['RXN','RXN_INDEX','P','T','A-MULTI','IDT_MAX_DP/DT'])
tmp_fig = plt.figure(figsize=(22,12))

factor = ''' + '%0.1f'%factor + '''
P_eff = ''' + str(pressure) + '''*1.013E5
T_eff = ''' + str(temperature) + '''
gas = ct.Solution(\'''' + xmlFile + '''\')
air = ct.Solution('air.xml')
gas.TPX = T_eff, P_eff, 'c9h20_26:1,o2:14,n2:52.64'
r = ct.IdealGasReactor(gas)
env = ct.Reservoir(air)

w = ct.Wall(r, env)
w.expansion_rate_coeff = 0.0  # set expansion parameter. dV/dt = KA(P_1 - P_2)
w.area = 1.0

t_end = 0.3
dt = 1.e-5
n_steps = int(t_end/dt)
sim = ct.ReactorNet([r])

index = 0
oriIgn = 0.0
time = 0.0
n_species = 4
time = []
temp = []
pres = []
while sim.time < t_end and r.T < T_eff + 1500:
	sim.step(t_end)
	time.append(sim.time)
	temp.append(r.T)
	pres.append(r.thermo.P)
diff_temp = np.diff(temp)/np.diff(time)
index = np.argmax(diff_temp)
ignition = time[index]*1000	

if r.T > T_eff+200:
	csvfile_ign.writerow(['original ignition delay','   ',P_eff/1E5,T_eff,factor,ignition])
	oriIgn = ignition
	print('oriIgn', oriIgn)
else:
	print('Error! Temperature is no higher than T_eff + 200!')

index_list = list(range(''' + str(reactionListStart) + ',' + str(reactionListEnd) + '''))
for index_reaction in index_list:
	gas = ct.Solution('reactions_myb1st2nd_gold2nd_3rdooqooh_test3.xml')
	air = ct.Solution('air.xml')
	gas.TPX = T_eff, P_eff, 'c9h20_26:1,o2:14,n2:52.64'
	r = ct.IdealGasReactor(gas)
	env = ct.Reservoir(air)
	
	print(index_reaction)
	rxn = gas.reaction(index_reaction-1)
	if isinstance(rxn, ct.ElementaryReaction):
		tmp_num = abs(rxn.rate.pre_exponential_factor) + abs(rxn.rate.temperature_exponent) + abs(rxn.rate.activation_energy)
		if tmp_num < 1e-10:
			ignition = oriIgn
			csvfile_ign.writerow([gas.reaction_equation(index_reaction-1),index_reaction,P_eff/1E5,T_eff,factor,ignition,'Note: rate 0.0'])
			continue
	gas.set_multiplier(factor,index_reaction-1)

	w = ct.Wall(r, env)
	w.expansion_rate_coeff = 0.0  # set expansion parameter. dV/dt = KA(P_1 - P_2)
	w.area = 1.0

	t_end = 0.3
	dt = 1.e-5
	n_steps = int(t_end/dt)
	sim = ct.ReactorNet([r])
	time = 0.0
	n_species = 4
	time = []
	temp = []
	pres = []
	while sim.time < t_end and r.T < T_eff + 1500:
		sim.step(t_end)
		time.append(sim.time)
		temp.append(r.T)
		pres.append(r.thermo.P)
	diff_temp = np.diff(temp)/np.diff(time)
	index = np.argmax(diff_temp)
	ignition = time[index]*1000	

	plt.plot(time, temp)
	tmp_fig.savefig('reaction_'+'%05d'%index_reaction+'.png', dpi=100)
	tmp_fig.clf()

	if r.T > T_eff+200:
		csvfile_ign.writerow(['original ignition delay','   ',P_eff/1E5,T_eff,factor,ignition])
		oriIgn = ignition
		print('ignition', ignition)
	else:
		print('Error! Temperature is no higher than T_eff + 200!')


f0.close()
plt.close(tmp_fig)	


''')
	fw.close()
	os.system("E:\\hetanjin\\GithubFiles\\Templates\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
	

