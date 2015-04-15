import subprocess
import sys
import os

if os.path.exists('c2h6.lst'):
	os.remove('c2h6.lst')
if os.path.exists('c2h6.doc'):
	os.remove('c2h6.doc')

endLine=chr(32)+chr(13)+chr(10)

cmd = ['therm.exe']
p = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print p.poll()
# (out,err) = p.communicate(input = '\n\nc2h6\nc2h6\n\n\n\n1\nc/c/h3 2\n18\n\nf\nc2h6\n\n\nc2h6\n')
# p.stdin.write('\n\nc2h6\nc2h6\n\n2\n1\n1\nc/c/h3 2\n18\n\nf\nc2h6\n\n\nc2h6\n')
step=0

#step 0
print '\nhi\t' + str(step)
i=0
sum_i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<3:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n'
step += 1

#step 1
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<3:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n'
step += 1

#step 2
print '\nhi\t' + str(step)
i=0
while True:
	break
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('c2h6\n')
print 'input: c2h6\\n' 
step += 1

#step 3
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<6:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('c2h6\n') 
print 'input: c2h6\\n'
step += 1

# step 4
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<6:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n'
step += 1

# step 5
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<4:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('2\n')
print 'input: 2\\n'
step += 1

# step 6
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('1\n')
print 'input: 1\\n'
step += 1

# step 7
print '\nhi\t' + str(step)
i=0
while True:
	break
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('1\n')
print 'input: 1\\n'
step += 1

# step 8
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<3:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('c/c/h3 2\n')
print 'input: c/c/h3 2\\n'
step += 1


# step 9
print '\nhi\t' + str(step)
i=0
while True:
	break
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('18\n')
print 'input: 18\\n' 
step += 1

# step 10
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<2:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n'  
step += 1

# step 11
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<2:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('f\n')
print 'input: f\\n'   
step += 1

# step 12
print '\nhi\t' + str(step)
i=0
while True:
	break
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('c2h6\n')
print 'input: c2h6\\n' 
step += 1

# step 13
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<2:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n' 
step += 1

# step 14
print '\nhi\t' + str(step)
i=0
while True:
	break
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('\n')
print 'input: \\n' 
step += 1

# step 15
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<2:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
p.stdin.write('c2h6\n')
print 'input: c2h6\\n' 
step += 1

# step 16
print '\nhi\t' + str(step)
i=0
while True:
	out = p.stdout.readline()
	print out[0:-2]+'---'
	if out==endLine:
		print '*****************' + str(i) + '\t' + str(sum_i)
		sum_i += 1
		if not (i+1)<1:
			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
			break
		else:
			i += 1
# p.stdin.write('c2h6\n')
print 'c2h6 calculated successfully!' 

# print '\nhi\t' + str(step)
# i=0
# while True:
# 	out = p.stdout.readline()
# 	print out[0:-2]+'---'
# 	if out==endLine:
# 		print '*****************' + str(i) + '\t' + str(sum_i)
# 		if not (i+1)<1:
# 			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
# 			break
# 		else:
# 			i += 1
# p.stdin.write('c2h6\n') 
# step += 1

# i=0
# while True:
# 	out = p.stdout.readline()
# 	print out[0:-2]
# 	if out[-2:]==endLine[-2:]:
# 		print '---'
# 	if out==endLine:
# 		print '*****************' + str(i) + '\t' + str(sum_i)
# 		i += 1
# 		if not (i+1)<1:
# 			print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
# 			break 

# for i in range(1,49):
# 	out = p.stdout.readline()
# 	print out


# print p.returncode
# print 'hi3'
# p.stdin.write('c2h6\n')
# while True:
# 	out = p.stdout.readline()
# 	print out
# 	if out==endLine:
# 		print '*****************' + str(i) + '\t' + str(sum_i)
# 		break

# for line in iter(p.stdout.readline, ''):
#     print line

# i = 0
# while i < 17:
# 	out = p.stdout.readline()
# 	# p.stdout.flush()
# 	print out + 'a'
# 	print 'length' + str(len(out))
# 	print out==endLine
# 	print str(ord(out[0])) + str(ord(out[1])) + str(ord(out[2]))
# 	i += 1


# while True:
# 	out=p.stdout.readline()
# 	print out
# 	if out=='':
# 		break

# (out,err) = p.communicate(input = '\n\nc2h6\nc2h6\n\n2\n1\n1\nc/c/h3 2\n18\n\nf\nc2h6\n\n\nc2h6\n')
# print out
# print err
# fw=file('log.txt','w')
# fw.write(out)
# fw.close()
# (out,err) = p.communicate(input = '\nc2h6\nc2h6\n\n2\n1\n1\nc/c/h3 2\n18\n\nf\n')
# fw=file('log.txt','w+')
# fw.write(out)
# fw.close()
print p.poll()
p.kill()
print 'end'