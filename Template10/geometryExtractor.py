# constants
elementDict={1:'H',6:'C',7:'N',8:'O',
'1':'H','6':'C','7':'N','8':'O'
}

def geometryExtractor(lines):
	geom = ''
	for tmp_line in lines:
		tmp_line.strip()
		tmp_line = tmp_line.split()
		geom += elementDict[tmp_line[1]] + '\t' + tmp_line[3] + '\t' + tmp_line[4] + '\t' + tmp_line[5]+'\n'
	return geom

def molproGeometryExtractor(lines):
	geom = ''
	for tmp_line in lines:
		tmp_line.strip()
		tmp_line = tmp_line.split()
		geom += elementDict[tmp_line[1]] + ',\t' + tmp_line[3] + ',\t' + tmp_line[4] + ',\t' + tmp_line[5]+'\n'
	return geom

