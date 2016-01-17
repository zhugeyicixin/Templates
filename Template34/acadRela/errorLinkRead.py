import re 

errorLinks = []
errorLinks2 = []
errorLinks3 = []

fr = file('errorLink.txt', 'r')
tmp_lines = fr.readlines()
for (index, tmp_line) in enumerate(tmp_lines):
	if re.match('.*parse_paper	stage:	1|parse_paper	stage:	3', tmp_line):
		errorLinks.append(tmp_lines[index-1].strip())

	elif re.match('.*stage', tmp_line):
		if re.match('.*parse_paper2	stage:	0', tmp_line):
			if tmp_lines[index-1].strip() not in errorLinks:
				errorLinks2.append(tmp_lines[index-1].strip())
				# print '(parse_paper2	stage:	0) not in (parse_paper stage 1 | 3) error'
				# print tmp_lines[index-1].strip() 
		else:
			errorLinks3.append(tmp_lines[index-1].strip())
			print tmp_line

# print errorLinks
fw = file('linkToVisit.txt', 'w')
fw.write('''
-------------------------------------------
	errorLinks in parse_paper
-------------------------------------------

''')
for tmp_link in errorLinks:
	fw.write('\"'+tmp_link+'\",'+'\n')

fw.write('''

-------------------------------------------
	errorLinks2 in parse_paper2
-------------------------------------------

''')
for tmp_link in errorLinks2:
	fw.write('\"'+tmp_link+'\",'+'\n')

fw.write('''

-------------------------------------------
	errorLinks3 in parse_paper | parse_paper2
-------------------------------------------

''')
for tmp_link in errorLinks3:
	fw.write('\"'+tmp_link+'\",'+'\n')	

fw.close()
