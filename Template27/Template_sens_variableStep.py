"""
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
f0= open('DMH_750K_10atm_phi1_01.csv','w')
csvfile_ign = csv.writer(f0, delimiter=',', lineterminator='\n')
csvfile_ign.writerow(['RXN','RXN_INDEX','P','T','A-MULTI','IDT_MAX_DP/DT'])
tmp_fig = plt.figure(figsize=(22,12))


factor = 0.5
P_eff = 10*1.013E5
T_eff = 750
gas = ct.Solution('reactions_myb1st2nd_gold2nd_3rdooqooh_test3.xml')
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

index_list = list(range(1,3))
P_list = [10*1.013E5]
T_list = [750]
for P_eff in P_list:
	for T_eff in T_list:
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
				print('oriIgn', oriIgn)
			else:
				print('Error! Temperature is no higher than T_eff + 200!')


f0.close()
plt.close(tmp_fig)	
