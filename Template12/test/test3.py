row_index = 3
while sh.cell_value(row_index,0) != '':
	reacs_line += 1

	if int(sh.cell_value(row_index,0)) != 0:

		############################
		##need to update for multi-reacs later
		############################
		
		name_R.append(sh.cell_value(row_index,1))
		filename_R.append(sh.cell_value(row_index,2))
		#corresponding to the similar sentense above
		energy_R.append(sh.cell_value(row_index,7))
		formula_R.append(sh.cell_value(row_index,10))
		if abs(float(sh.cell_value(row_index, 11)))>1e-2:
			rotConsts_R.append([float(sh.cell_value(row_index,11)),float(sh.cell_value(row_index,12)),float(sh.cell_value(row_index,13))])
		else:
			rotConsts_R.append([float(sh.cell_value(row_index,12))])
		rotConsts_R[-1] = phys1.GHZTocmm1(np.array(rotConsts_R[-1]))
		RSN_R.append(int(sh.cell_value(row_index,15)))
		multi_R.append(int(sh.cell_value(row_index,16)))
		num_freq_R.append(int(sh.cell_value(row_index,19)))

		tmp_freq = []
		for col_num in range(num_freq_R[-1]): 
			tmp_freq.append(sh.cell_value(row_index,21+col_num))
		freq_R.append(tmp_freq)

		tmp_geom = []
		tmp_num = int(sh2.cell_value(2, row_index-2))
		for tmp_row in range(tmp_num):
			tmp_geom.append(sh2.cell_value(tmp_row+3, row_index-2))
		geom_R.append(tmp_geom)

		tmp_hessian = []
		tmp_num = int(sh3.cell_value(2, row_index-2))
		for tmp_row in range(tmp_num):
			tmp_hessian.append(sh3.cell_value(tmp_row+3, row_index-2))
		hessian_R.append(tmp_hessian)

	row_index += 1

row_index += 1
while sh.cell_value(row_index,0) != '':
	prods_line += 1
	row_index += 1