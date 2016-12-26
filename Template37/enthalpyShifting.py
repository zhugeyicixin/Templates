import re
import phys

# constants
phys1 = phys.phys()
pattern_carbonNumber=re.compile('.* +C +([0-9]+)[HO].*')

fr=file('test.txt', 'r')
tmp_lines = fr.readlines()
fr.close()
for i in xrange(len(tmp_lines)):
	if i%4 == 0:
		tmp_m = pattern_carbonNumber.match(tmp_lines[i])
		if tmp_m:
			print tmp_lines[i]
			print float(tmp_m.group(1))
			print tmp_lines[i+2]
			tmp_num = float(tmp_lines[i+2][0:15]) + 932.2973087*int(tmp_m.group(1))/phys1.JoulTocal(phys1.R)
			tmp_num = '%.7e' % tmp_num
			tmp_num = ' '*(15-len(tmp_num)) + tmp_num
			tmp_lines[i+2] = tmp_num+tmp_lines[i+2][15:]
			print tmp_lines[i+2]

			print tmp_lines[i+3]
			tmp_num = float(tmp_lines[i+3][30:45]) + 932.2973087*int(tmp_m.group(1))/phys1.JoulTocal(phys1.R)
			tmp_num = '%.7e' % tmp_num
			tmp_num = ' '*(15-len(tmp_num)) + tmp_num
			tmp_lines[i+3] = ''.join([tmp_lines[i+3][0:30], tmp_num, tmp_lines[i+3][45:]]) 
			print tmp_lines[i+3]

fw = file('test_out.txt', 'w')
fw.writelines(tmp_lines)
fw.close()
# print tmp_lines