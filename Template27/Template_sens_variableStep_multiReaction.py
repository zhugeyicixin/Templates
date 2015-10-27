"""
Constant-pressure, adiabatic kinetics simulation.
"""

import sys
import os
import csv
import numpy as np
import cantera as ct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# os.system('cheminp2xml.bat')
plot_bool = 0
bool_diagram = 0
f0= open('DMH_650K_10atm_phi1_0001.csv','w')
csvfile_ign = csv.writer(f0, delimiter=',', lineterminator='\n')
csvfile_ign.writerow(['RXN','RXN_INDEX','P','T','A-MULTI','IDT_MAX_DP/DT'])
tmp_fig = plt.figure(figsize=(22,12))

factor = 0.5
P_eff = 10*1.013E5
T_eff = 650
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

'''
reaction classification
Fuel decomposition,4801,4802,4803,4804,4805,4806,4807,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Fuel + OH,4906,4907,4908,4909,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
R beta-scission,5000,5001,5002,5003,5004,5005,5006,5007,5008,5009,5010,5011,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
R+O2=RO2,5182,5183,5184,5185,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
RO2 concerted elimination,5266,5267,5268,5269,5270,5271,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
RO2=QOOH,5240,5241,5242,5243,5244,5245,5246,5247,5248,5249,5250,5251,5252,5253,5254,5255,5256,5257,5258,5259,5260,,,,,,,,,,,,,,,,,,,,,
QOOH=cyclic ether+OH,5376,5377,5378,5379,5380,5381,5382,5383,5384,5385,5386,5387,5388,5389,5390,5391,5392,5393,5394,5395,5396,5397,5398,5399,5400,5401,5402,5403,5404,5405,5406,5407,5408,5409,5410,5411,5412,5413,5414,5415,5416,5417
QOOH=olefin+HO2,5423,5424,5425,5426,5427,5428,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
QOOH beta-scission,5439,5440,5441,5442,5443,5444,5445,5446,5447,5448,5449,5450,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
QOOH+O2,5466,5467,5468,5469,5470,5471,5472,5473,5474,5475,5476,5477,5478,5479,5480,5481,5482,5483,5484,5485,5486,,,,,,,,,,,,,,,,,,,,,
OOQOOH decomposition,5497,5498,5499,5500,5501,5502,5503,5504,5505,5506,5507,5508,5509,5510,5511,6410,6411,6412,6413,6414,6415,6416,6417,6418,6419,6420,6421,,,,,,,,,,,,,,,
keto decomposition,5532,5533,5534,5535,5536,5537,5538,5539,5540,5541,5542,5543,5544,5545,5546,5547,5548,5549,5550,5551,5552,5553,5554,5555,5556,5557,5558,5559,5560,5561,745,1442,6408,6409,6422,6243,,,,,,
'''
reactionClass = [
'Fuel decomposition',
'Fuel + OH',
'R beta-scission',
'R+O2=RO2',
'RO2 concerted elimination',
'RO2=QOOH',
'QOOH=cyclic ether+OH',
'QOOH=olefin+HO2',
'QOOH beta-scission',
'QOOH+O2',
'OOQOOH decomposition',
'keto decomposition'
]
# the number is same as the reaction ID in .xml
index_list = [
[4801,4802,4803,4804,4805,4806,4807],
[4906,4907,4908,4909],
[5000,5001,5002,5003,5004,5005,5006,5007,5008,5009,5010,5011],
[5182,5183,5184,5185],
[5266,5267,5268,5269,5270,5271],
[5240,5241,5242,5243,5244,5245,5246,5247,5248,5249,5250,5251,5252,5253,5254,5255,5256,5257,5258,5259,5260],
[5376,5377,5378,5379,5380,5381,5382,5383,5384,5385,5386,5387,5388,5389,5390,5391,5392,5393,5394,5395,5396,5397,5398,5399,5400,5401,5402,5403,5404,5405,5406,5407,5408,5409,5410,5411,5412,5413,5414,5415,5416,5417],
[5423,5424,5425,5426,5427,5428],
[5439,5440,5441,5442,5443,5444,5445,5446,5447,5448,5449,5450],
[5466,5467,5468,5469,5470,5471,5472,5473,5474,5475,5476,5477,5478,5479,5480,5481,5482,5483,5484,5485,5486],
[5497,5498,5499,5500,5501,5502,5503,5504,5505,5506,5507,5508,5509,5510,5511,6410,6411,6412,6413,6414,6415,6416,6417,6418,6419,6420,6421],
[5532,5533,5534,5535,5536,5537,5538,5539,5540,5541,5542,5543,5544,5545,5546,5547,5548,5549,5550,5551,5552,5553,5554,5555,5556,5557,5558,5559,5560,5561,745,1442,6408,6409,6422,6243]
]
for (index_class, tmp_reactions) in enumerate(index_list):
	gas = ct.Solution('reactions_myb1st2nd_gold2nd_3rdooqooh_test3.xml')
	air = ct.Solution('air.xml')
	gas.TPX = T_eff, P_eff, 'c9h20_26:1,o2:14,n2:52.64'
	r = ct.IdealGasReactor(gas)
	env = ct.Reservoir(air)
	
	print(reactionClass[index_class])
	# rxn = gas.reaction(index_reaction-1)
	# if isinstance(rxn, ct.ElementaryReaction):
	# 	tmp_num = abs(rxn.rate.pre_exponential_factor) + abs(rxn.rate.temperature_exponent) + abs(rxn.rate.activation_energy)
	# 	if tmp_num < 1e-10:
	# 		ignition = oriIgn
	# 		csvfile_ign.writerow([gas.reaction_equation(index_reaction-1),index_reaction,P_eff/1E5,T_eff,factor,ignition,'Note: rate 0.0'])
	# 		continue
	for tmp_reaction in tmp_reactions:
		gas.set_multiplier(factor, tmp_reaction-1)

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
	tmp_fig.savefig('reaction_'+'%05d'%index_class+'.png', dpi=100)
	tmp_fig.clf()

	if r.T > T_eff+200:
		csvfile_ign.writerow([reactionClass[index_class],index_class,P_eff/1E5,T_eff,factor,ignition])
		print('ignition', ignition)
	else:
		print('Error! Temperature is no higher than T_eff + 200!')


f0.close()
plt.close(tmp_fig)	


